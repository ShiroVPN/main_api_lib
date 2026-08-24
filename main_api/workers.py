# pyright: reportUnusedParameter=false

__all__ = [
    "get_client",
    "post_client",
    "post_transaction",
    "get_subscription",
    "get_subscription_options",
    "post_trial_subscription",
    "post_new_subscription",
    "renew_subscription",
    "update_subscription",
    "get_connection_config",
    "notify_client",
    "update_peerhub_heartbeat",
]

from .broker import broker

if broker is None:
    raise RuntimeError(
        """You can not use declared tasks before setting up broker. \
        Use 'broker.declare_broker' function."""
    )

from . import models as m


@broker.task(task_name="main_api.get_client")
async def get_client(client_data: m.ClientGet) -> m.Client: ...


@broker.task(task_name="main_api.post_client")
async def post_client(
    client_data: m.ClientPost,
) -> m.Client: ...


@broker.task(task_name="main_api.post_transaction")
async def post_transaction(
    transaction_data: m.TransactionPost,
) -> m.Transaction: ...


@broker.task(task_name="main_api.get_subscription")
async def get_subscription(client_data: m.ClientGet) -> m.Subscription: ...


@broker.task(task_name="main_api.get_subscription_options")
async def get_subscription_options() -> list[m.SubscriptionConfig]: ...


@broker.task(task_name="main_api.post_trial_subscription")
async def post_trial_subscription(
    client_data: m.ClientGet,
) -> m.Subscription: ...


@broker.task(task_name="main_api.post_new_subscription")
async def post_new_subscription(
    sub_data: m.SubscriptionPost,
) -> m.Subscription: ...


@broker.task(task_name="main_api.renew_subscription")
async def renew_subscription(
    client_data: m.ClientGet,
) -> m.Subscription: ...


@broker.task(task_name="main_api.update_subscription")
async def update_subscription(
    client_data: m.ClientGet,
) -> m.Subscription: ...


@broker.task(task_name="main_api.get_connection_config")
async def get_connection_config(
    client_data: m.ClientGet,
) -> str: ...


@broker.task(task_name="main_api.notify_client")
async def notify_client(
    client_data: m.ClientGet,
) -> m.Success: ...


@broker.task(task_name="main_api.update_peerhub_heartbeat")
async def update_peerhub_heartbeat(
    peerhub_heartbeat_data: m.PeerHubHeartbeatData,
) -> m.Success: ...
