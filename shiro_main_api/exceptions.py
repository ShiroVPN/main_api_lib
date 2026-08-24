__all__ = [
    "AppException",
    "client_exists",
    "client_not_found",
    "client_already_activated_trial",
    "client_did_not_activate_trial",
    "subscription_exists",
    "subscription_not_found",
    "balance_is_negative",
    "balance_will_be_negative",
    "subscription_option_not_found",
    "subscription_option_exists",
    "trial_subscription_is_not_free",
    "subscription_is_expired",
    "subscription_is_not_expired",
    "subscription_config_changed",
    "subscription_config_did_not_change",
    "alive_peerhub_not_found",
]


from typing import ClassVar

from pydantic import BaseModel


class ErrorMetadata(BaseModel):
    pass


class AppException(Exception):
    status_code: ClassVar[int]
    error_code: ClassVar[str]
    message: str | None = None
    metadata: ErrorMetadata | None = None

    def __init__(
        self, message: str | None = None, metadata: ErrorMetadata | None = None
    ):
        self.message = message
        self.metadata = metadata
        super().__init__(self.error_code)


class client_exists(AppException):
    status_code: ClassVar[int] = 499
    error_code: ClassVar[str] = "CLIENT_EXISTS"


class client_not_found(AppException):
    status_code: ClassVar[int] = 498
    error_code: ClassVar[str] = "CLIENT_NOT_FOUND"


class client_already_activated_trial(AppException):
    status_code: ClassVar[int] = 497
    error_code: ClassVar[str] = "CLIENT_ALREADY_ACTIVATED_TRIAL"


class client_did_not_activate_trial(AppException):
    status_code: ClassVar[int] = 496
    error_code: ClassVar[str] = "CLIENT_DID_NOT_ACTIVATE_TRIAL"


class subscription_exists(AppException):
    status_code: ClassVar[int] = 495
    error_code: ClassVar[str] = "SUBSCRIPTION_EXISTS"


class subscription_not_found(AppException):
    status_code: ClassVar[int] = 494
    error_code: ClassVar[str] = "SUBSCRIPTION_NOT_FOUND"


class balance_is_negative(AppException):
    status_code: ClassVar[int] = 493
    error_code: ClassVar[str] = "BALANCE_IS_NEGATIVE"


class balance_will_be_negative(AppException):
    status_code: ClassVar[int] = 492
    error_code: ClassVar[str] = "BALANCE_WILL_BE_NEGATIVE"


class subscription_option_not_found(AppException):
    status_code: ClassVar[int] = 491
    error_code: ClassVar[str] = "SUBSCRIPTION_OPTION_NOT_FOUND"


class subscription_option_exists(AppException):
    status_code: ClassVar[int] = 483
    error_code: ClassVar[str] = "SUBSCRIPTION_OPTION_EXISTS"


class trial_subscription_is_not_free(AppException):
    status_code: ClassVar[int] = 490
    error_code: ClassVar[str] = "TRIAL_SUBSCRIPTION_IS_NOT_FREE"


class subscription_is_expired(AppException):
    status_code: ClassVar[int] = 489
    error_code: ClassVar[str] = "SUBSCRIPTION_IS_EXPIRED"


class subscription_is_not_expired(AppException):
    status_code: ClassVar[int] = 488
    error_code: ClassVar[str] = "SUBSCRIPTION_IS_NOT_EXPIRED"


class subscription_config_changed(AppException):
    status_code: ClassVar[int] = 485
    error_code: ClassVar[str] = "SUBSCRIPTION_CONFIG_CHANGED"


class subscription_config_did_not_change(AppException):
    status_code: ClassVar[int] = 484
    error_code: ClassVar[str] = "SUBSCRIPTION_CONFIG_DID_NOT_CHANGE"


class alive_peerhub_not_found(AppException):
    status_code: ClassVar[int] = 599
    error_code: ClassVar[str] = "ALIVE_PEERHUB_NOT_FOUND"
