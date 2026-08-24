# Main API

This service defines TaskIQ workers for managing VPN subscriptions, client balances, and transactions. It integrates with a `peerhub` service (e.g., WireGuard) to manage VPN connections.

# Usage example on client

```python
from pydantic import AmqpDsn
from taskiq_redis import RedisAsyncResultBackend

from main_api.broker import (
    BrokerConfigForClient,
    create_broker_for_client,
    define_broker,
)

broker_config = BrokerConfigForClient(
    broker_url=AmqpDsn("amqp://user:password@localhost:5672"),
    exchange_name="kiwi",
)

broker = create_broker_for_client(broker_config).with_result_backend(
    RedisAsyncResultBackend("redis://localhost:6379/0"),
)

define_broker(broker)

# after define_broker was called

from main_api.models import ClientGet
from main_api.workers import get_client


async def main():
    task = await get_client.kiq(ClientGet(telegram_id=0))
    result = await task.wait_result()
    print(result.return_value)


if __name__ == "__main__":
    print("Success!")
```

# Usage example on worker

```python
from pydantic import AmqpDsn

from main_api.broker import (
    BrokerConfigForWorker,
    create_broker_for_worker,
    define_broker,
)

broker_config = BrokerConfigForWorker(
    broker_url=AmqpDsn("amqp://user:password@localhost:5672"),
    exchange_name="kiwi",
    queue_name="q",
)

broker = create_broker_for_worker(broker_config)

define_broker(broker)

# after define_broker was called

from main_api.models import Client, ClientGet
from main_api.util import define_task
from main_api.workers import get_client

from .dependencies import db_dependency


# method 1
@define_task(get_client)
async def get_client_impl(
    client_data: ClientGet, db: db_dependency
) -> Client: ...


# method 2
@broker.task(task_name=get_client.task_name)
async def get_client_impl(
    client_data: ClientGet, db: db_dependency
) -> Client: ...


# method 3
_ = broker.register_task(get_client_impl, get_client.task_name)


if __name__ == "__main__":
    print("Success!")
```

# Models

All models are defined as Pydantic schemas.

| Name                   | Fields                                                       |
| ---------------------- | ------------------------------------------------------------ |
| `Client`               | `telegram_id: int`<br/>`balance: Decimal`<br/>`activated_trial: bool`<br/>`autoupdate_subscriptions: bool`<br/>`created_at: datetime_utc`<br/>`updated_at: datetime_utc` |
| `ClientGet`            | `telegram_id: int` ($\ge 0$, $\lt 2^{63}$)                   |
| `ClientPost`           | inherits `ClientGet`.                                        |
| `TransactionPost`      | inherits `ClientGet`<br/>`delta: Decimal`                    |
| `Transaction`          | `old_balance: Decimal`<br/>`new_balance: Decimal`<br/>`delta: Decimal` |
| `SubscriptionConfig`   | `name: str`<br/>`cost: Decimal` ($\ge 0$)<br/>`timedelta_in_seconds: int` (> 0) |
| `Subscription`         | `subscription_config: SubscriptionConfig`<br/>`enabled: bool`<br/>`autoupdate: bool`<br/>`expired_at: datetime_utc`<br/>`created_at: datetime_utc` |
| `SubscriptionPost`     | inherits `ClientGet`<br/>`subscription_option_name: str`     |
| `PeerHubHeartbeatData` | `hub_id: UUID`<br/>`server_name: str`<br/>`connection_type: str`<br/>`country: str`<br/>`last_seen_at: datetime_utc` |
| `Success`              | `ok: bool = True`                                            |

# Workers

All workers are exposed via TaskIQ.

- Queue: `BROKER_BLOOM_QUEUE_NAME` (default: `bloom_queue`)
- Exchange: `BROKER_BLOOM_EXCHANGE_NAME` (default: `bloom_exchange`)

| Name                                                         | Arguments              | Returns                                                      | Business errors                                              |
| ------------------------------------------------------------ | ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `main_api.get_client`                                        | `ClientGet`            | `Client`                                                     | `client_not_found`                                           |
| `main_api.post_client`                                       | `ClientPost`           | `Client`                                                     | `client_exists`                                              |
| `main_api.post_transaction`                                  | `TransactionPost`      | `Transaction`                                                | `client_not_found`, `balance_will_be_negative`               |
| `main_api.get_subscription`                                  | `ClientGet`            | `Subscription`                                               | `client_not_found`, `subscription_not_found`                 |
| `main_api.get_subscription_options`<br />Call this to select a subscription and add it with `main_api.post_new_subscription`. | (none)                 | `list[SubscriptionConfig]`<br />All options with positive cost. Does not include trial. | –                                                            |
| `main_api.post_trial_subscription`                           | `ClientGet`            | `Subscription`                                               | `client_not_found`, `client_already_activated_trial`, `subscription_exists`, `alive_peerhub_not_found`, `trial_subscription_is_not_free` |
| `main_api.post_new_subscription`                             | `SubscriptionPost`     | `Subscription`                                               | `client_not_found`, `subscription_not_found`, `client_did_not_activate_trial`, `subscription_option_not_found`, `balance_will_be_negative` |
| `main_api.renew_subscription`                                | `ClientGet`            | `Subscription`                                               | `client_not_found`, `subscription_not_found`, `subscription_option_not_found`, `balance_will_be_negative` |
| `main_api.update_subscription`                               | `ClientGet`            | `Subscription`                                               | `client_not_found`, `subscription_not_found`, `subscription_is_not_expired` |
| `main_api.get_connection_config`                             | `ClientGet`            | `str` (WireGuard config)                                     | `client_not_found`, `subscription_not_found`                 |
| `main_api.notify_client`                                     | `ClientGet`            | `Success`                                                    | –                                                            |
| `main_api.update_peerhub_heartbeat`                          | `PeerHubHeartbeatData` | `Success`                                                    | –                                                            |

# Exceptions

Custom business exceptions raised by workers. All inherit from `AppException`.

| Name                                 | Description                                                  | Error code                           | Status code | How and where can rise?                                      |
| ------------------------------------ | ------------------------------------------------------------ | ------------------------------------ | ----------- | ------------------------------------------------------------ |
| `client_exists`                      | Client with given Telegram ID already exists.                | `CLIENT_EXISTS`                      | 499         | `main_api.post_client`                                       |
| `client_not_found`                   | Client with given Telegram ID does not exist.                | `CLIENT_NOT_FOUND`                   | 498         | Almost every task.                                           |
| `client_already_activated_trial`     |                                                              | `CLIENT_ALREADY_ACTIVATED_TRIAL`     | 497         | `main_api.post_trial_subscription`                           |
| `client_did_not_activate_trial`      |                                                              | `CLIENT_DID_NOT_ACTIVATE_TRIAL`      | 496         | `main_api.post_new_subscription`                             |
| `subscription_exists`                | Client has a subscription (sub is not marked deleted in DB). | `SUBSCRIPTION_EXISTS`                | 495         | `main_api.post_trial_subscription`                           |
| `subscription_not_found`             | Client has no subscription.                                  | `SUBSCRIPTION_NOT_FOUND`             | 494         | `main_api.post_new_subscription`, `main_api.renew_subscription`, `main_api.update_subscription`, `main_api.get_connection_config` |
| `balance_is_negative`                | Balance cannot be negative.                                  | `BALANCE_IS_NEGATIVE`                | 493         | Should not rise (logic prevents negative balance).           |
| `balance_will_be_negative`           | Operation would result in negative balance.                  | `BALANCE_WILL_BE_NEGATIVE`           | 492         | `main_api.post_transaction`, `main_api.post_new_subscription`, `main_api.renew_subscription` |
| `subscription_option_not_found`      | `SubscriptionConfig` with given name is not in `Config`.     | `SUBSCRIPTION_OPTION_NOT_FOUND`      | 491         | `main_api.post_new_subscription`, `main_api.renew_subscription` |
| `subscription_option_exists`         |                                                              | `SUBSCRIPTION_OPTION_EXISTS`         | 483         | Should not rise.                                             |
| `trial_subscription_is_not_free`     | Trial subscription cost must be zero.                        | `TRIAL_SUBSCRIPTION_IS_NOT_FREE`     | 490         | `main_api.post_trial_subscription` (should not rise).        |
| `subscription_is_expired`            |                                                              | `SUBSCRIPTION_IS_EXPIRED`            | 489         | Should not rise.                                             |
| `subscription_is_not_expired`        |                                                              | `SUBSCRIPTION_IS_NOT_EXPIRED`        | 488         | `main_api.update_subscription`                               |
| `subscription_config_changed`        | Subscription configuration has changed with time. F.e. client added this option when it cost 100, but now it costs 200. | `SUBSCRIPTION_CONFIG_CHANGED`        | 485         | Not raised in any task (policy unused).                      |
| `subscription_config_did_not_change` |                                                              | `SUBSCRIPTION_CONFIG_DID_NOT_CHANGE` | 484         | Should not rise.                                             |
| `alive_peerhub_not_found`            | No active (alive) PeerHub instance available.                | `ALIVE_PEERHUB_NOT_FOUND`            | 599         | `main_api.post_trial_subscription`                           |
