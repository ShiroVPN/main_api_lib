__all__ = [
    "BrokerConfigForClient",
    "BrokerConfigForWorker",
    "create_broker_for_client",
    "create_broker_for_worker",
    "broker",
    "define_broker",
]

from aio_pika import ExchangeType
from pydantic import AmqpDsn, BaseModel
from taskiq_aio_pika import AioPikaBroker, Exchange, Queue


class BrokerConfigForClient(BaseModel):
    broker_url: AmqpDsn
    exchange_name: str


class BrokerConfigForWorker(BrokerConfigForClient):
    queue_name: str


def create_broker_for_client(config: BrokerConfigForClient) -> AioPikaBroker:
    exchange = Exchange(name=config.exchange_name, type=ExchangeType.HEADERS)
    broker = AioPikaBroker(url=str(config.broker_url), exchange=exchange)
    return broker


def create_broker_for_worker(config: BrokerConfigForWorker) -> AioPikaBroker:
    exchange = Exchange(name=config.exchange_name, type=ExchangeType.HEADERS)
    task_queues = [
        Queue(
            name=config.queue_name,
        )
    ]
    broker = AioPikaBroker(
        url=str(config.broker_url),
        exchange=exchange,
        task_queues=task_queues,
    )
    return broker


broker: AioPikaBroker | None = None


def define_broker(value: AioPikaBroker) -> None:
    global broker
    broker = value
