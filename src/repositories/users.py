from schemas.users import User
from src.repositories.base import BaseRepository
from src.models.users import UserORM

class UsersRepository(BaseRepository):
    model = UserORM
    schema = User