from pydantic import AmqpDsn

from shiro_main_api.broker import (
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

from shiro_main_api.models import Client, ClientGet
from shiro_main_api.util import define_task
from shiro_main_api.workers import get_client

from .dependencies import db_dependency


# method 1
@define_task(get_client)
async def get_client_impl(
    client_data: ClientGet, db: db_dependency
) -> Client: ...


# method 2
@broker.task(task_name=get_client.task_name)
async def get_client_impl2(
    client_data: ClientGet, db: db_dependency
) -> Client: ...


# method 3
_ = broker.register_task(get_client_impl, get_client.task_name)


if __name__ == "__main__":
    print("Success!")
