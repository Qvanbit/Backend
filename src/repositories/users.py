from pydantic import EmailStr
from sqlalchemy import select
from schemas.users import User, UserWithHashedPassword
from src.repositories.base import BaseRepository
from src.models.users import UserORM

class UsersRepository(BaseRepository):
    model = UserORM
    schema = User
    
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)