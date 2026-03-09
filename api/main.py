import json
from pathlib import Path
from fastapi import FastAPI
from router import yokais

app = FastAPI()
app.include_router(yokais.router)


@app.on_event("startup")
def load_yokai():
    json_path = Path(__file__).parent / "yokai.json"

    with open(json_path, "r") as file:
        data = json.load(file)

    for yokai in data:
        new_yokai = {
            "id": yokai["id"],
            "name": yokai["name"],
            "rank": yokai["rank"],
            "tribe": yokai["tribe"],
            "attribute": yokai["attribute"],
            "imageurl": yokai["imageurl"]
        }
        yokais.yokais_db[yokai["id"]] = new_yokai

    print(f"Loaded {len(data)} yokai")