from typing import List
from watchdog import WatchDogOptions

from db import DB, FileDB, MemoryDB
from type import DataNode

options = WatchDogOptions(
    hunger_time=3000,
)

data_nodes: List[DataNode] = [
    DataNode(endpoint='127.0.0.2', port=5000),
    DataNode(endpoint='127.0.0.3', port=5000),
    DataNode(endpoint='127.0.0.4', port=5000),
]


def get_db() -> DB:
    return MemoryDB()
