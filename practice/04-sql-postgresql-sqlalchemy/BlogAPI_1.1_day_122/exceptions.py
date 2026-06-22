from fastapi import status


class AppException(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


class EntityNotFound(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code = status.HTTP_404_NOT_FOUND, detail=detail)


class UniqueError(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code = status.HTTP_400_BAD_REQUEST, detail=detail)