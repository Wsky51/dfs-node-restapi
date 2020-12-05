from typing import List
from watchdog import WatchDogOptions

from db import DB, FileDB, MemoryDB
from type import DataNode
from datetime import datetime

# 每10秒钟获取一次数据
options = WatchDogOptions(
    hunger_time=10,
)

datetime_format = "%Y-%m-%d %H:%M:%S"

data_nodes: List[DataNode] = [
    DataNode(endpoint='127.0.0.2', port=5000, node_id='wuyi-1'),
    DataNode(endpoint='127.0.0.3', port=5000, node_id='wuyi-2'),
    DataNode(endpoint='127.0.0.4', port=5000, node_id='wuyi-3'),
]


def get_db() -> DB:
    # save data to the json file
    file_db = FileDB(file='./db.bin')
    return file_db


def get_second_datetime() -> datetime:
    now = datetime.now()
    return datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second
    )


db = get_db()
