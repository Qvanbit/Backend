from fastapi import APIRouter, HTTPException, Response


from src.repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Автроизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password =  AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "Success"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    async with async_session_maker() as session:
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(
                email=data.email
            )
        except:
            raise HTTPException(status_code=401, detail="Incorrect username")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}
    
    
@router.get("/me")
async def get_me(
    user_id: UserIdDep,
        ):
    async with async_session_maker() as session:
        user = await UsersRepository(session=session).get_one_or_none(id=user_id)
        return user