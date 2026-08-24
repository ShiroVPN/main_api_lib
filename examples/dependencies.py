from typing import Annotated

from taskiq import TaskiqDepends


class Database:
    pass


def get_database():
    yield Database()


db_dependency = Annotated[Database, TaskiqDepends(get_database)]
