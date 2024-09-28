class BaseException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args: object) -> None:
        super().__init__(self.detail, *args)
        


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"