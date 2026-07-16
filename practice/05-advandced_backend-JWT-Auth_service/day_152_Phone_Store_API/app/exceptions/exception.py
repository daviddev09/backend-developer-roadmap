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

    
class BadRequest(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code = status.HTTP_422_UNPROCESSABLE_CONTENT, detail=detail)


class AccessDenied(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail=detail)


class Unauthorized(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code = status.HTTP_401_UNAUTHORIZED, detail=detail)


class BalanceInsufficient(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code = status.HTTP_400_BAD_REQUEST, detail=detail)


class TokenTimeOut(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class CodeTimeOut(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

        
class InsufficientStock(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)