"""create fake data to the db file"""
from config import data_nodes, get_db
from type import DataNodeStatus, DataNode
from datetime import timedelta
from config import get_second_datetime


def create_fake_data_status(data_node: DataNode):
    now = get_second_datetime()
    db = get_db()
    for i in range(100):
        status = DataNodeStatus(
            # 每十次宕机一次
            dead=i % 10 == 0,
            capacity=1000,
            used=100 + (i % 7),
            datetime=now + timedelta(minutes=i)
        )
        db.save(data_node.node_id, status)


def create_fake_data():
    for data_node in data_nodes:
        create_fake_data_status(data_node)


if __name__ == '__main__':
    create_fake_data()
