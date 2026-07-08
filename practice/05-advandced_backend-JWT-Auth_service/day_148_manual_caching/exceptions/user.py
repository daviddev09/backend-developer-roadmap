class BaseException(Exception):
    pass


class EmailExistsException(BaseException):
    pass


class UserNotFoundException(BaseException):
    pass