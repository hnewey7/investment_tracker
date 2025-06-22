from fastapi import APIRouter

# - - - - - - - - - - - - - - - - - - -

router = APIRouter(tags=["login"])

# - - - - - - - - - - - - - - - - - - -

@router.get("/login")
def login():
    return {"Login":True}