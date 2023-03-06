from dataclasses import dataclass, field
from typing import Union


@dataclass
class DomainError:
    """
    All errors in application core, must be a type of this class.
    In the application core all errors must be wrapped inside an `result.Err` object.

    Attributes:
        message: Optional; A message describing what happened.
    """
    message: str = 'Unspecified error has occurred in the process.'
    status_code: int = 400
    errors = []

    def add_error(self, parameter, message):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        return len(self.errors) > 0


@dataclass
class ValidationErrors(DomainError):
    """"""
    message: str = field(default='Bad request error has occurred.')
    errors: Union[list, dict] = None
    status_code: int = 400


@dataclass
class CaptchaCodeError(DomainError):
    """"""
    message: str = field(default='Invalid captcha')
    errors = {'captcha_code': ['captcha_code is invalid or missing']}
    status_code: int = 400


@dataclass
class BadRequest(DomainError):
    """"""
    message: str = field(default='Bad request error has occurred.')
    errors: Union[list, dict] = None
    status_code: int = 400


@dataclass
class NotFoundError(DomainError):
    """"""
    message: str = field(default='NotFound error has occurred.')
    status_code: int = 404


@dataclass
class ServiceUnavailableError(DomainError):
    """"""
    message: str = field(default='Service Unavailable error has occurred.')
    status_code: int = 503


@dataclass
class AuthenticationError(DomainError):
    """"""
    message: str = field(default='Authentication error has occurred.')
    status_code: int = 401


@dataclass
class AuthorizationError(DomainError):
    """"""
    message: str = field(default='Permission denied')
    status_code: int = 403


@dataclass
class DataIntegrityError(DomainError):
    """"""
    message: str = field(default='The object is already exists')
    status_code: int = 409


@dataclass
class ServerError(DomainError):
    """"""
    message: str = field(default='Server has unexpected error')
    status_code: int = 500
