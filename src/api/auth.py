from fastapi import APIRouter, HTTPException, Response

from schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/auth", tags=["Автроизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    return {"status": "Success"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except:
        raise HTTPException(status_code=401, detail="Incorrect username")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie(key="access_token")
    return {"status": "Success"}


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
        user = await db.users.get_one_or_none(id=user_id)
        return user
