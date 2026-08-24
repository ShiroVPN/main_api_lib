__all__ = [
    "SubscriptionConfig",
    "ClientGet",
    "ClientPost",
    "TransactionPost",
    "Transaction",
    "Subscription",
    "SubscriptionPost",
    "PeerHubHeartbeatData",
    "Success",
]

from decimal import Decimal
from uuid import UUID

from heliclockter import datetime_utc
from pydantic import BaseModel, Field


class SubscriptionConfig(BaseModel):
    name: str
    cost: Decimal = Field(ge=0)
    timedelta_in_seconds: int = Field(gt=0)


class Client(BaseModel):
    telegram_id: int
    balance: Decimal
    activated_trial: bool
    autoupdate_subscriptions: bool
    created_at: datetime_utc
    updated_at: datetime_utc


class ClientGet(BaseModel):
    telegram_id: int = Field(ge=0, lt=2**63)


class ClientPost(ClientGet):
    pass


class TransactionPost(ClientGet):
    delta: Decimal


class Transaction(BaseModel):
    old_balance: Decimal
    new_balance: Decimal
    delta: Decimal


class Subscription(BaseModel):
    subscription_config: SubscriptionConfig
    enabled: bool
    autoupdate: bool
    expired_at: datetime_utc
    created_at: datetime_utc


class SubscriptionPost(ClientGet):
    subscription_option_name: str


class PeerHubHeartbeatData(BaseModel):
    hub_id: UUID
    server_name: str
    connection_type: str
    country: str
    last_seen_at: datetime_utc


class Success(BaseModel):
    ok: bool = True
