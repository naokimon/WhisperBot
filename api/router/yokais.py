from fastapi import APIRouter

router = APIRouter(prefix="/yokais", tags=["yokais"])

yokais_db = {}


@router.get("/")
def get_yokais():
    return yokais_db


@router.get("/{yokai_id}")
def get_yokai(yokai_id: int):
    return yokais_db[yokai_id]