from pydantic import AmqpDsn
from taskiq_redis import RedisAsyncResultBackend

from shiro_main_api.broker import (
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

from shiro_main_api.models import ClientGet
from shiro_main_api.workers import get_client


async def main():
    task = await get_client.kiq(ClientGet(telegram_id=0))
    result = await task.wait_result()
    print(result.return_value)


if __name__ == "__main__":
    print("Success!")
