from typing import List, Optional
from type import DataNode, DataNodeStatus
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dataclasses import dataclass


@dataclass
class WatchDogOptions:
    hunger_time: int
    food_path: Optional[str] = None


class WatchDog:
    """watch the node health of the cluster"""
    def __init__(self, options: WatchDogOptions,  data_nodes: List[DataNode]):
        if not data_nodes:
            raise ValueError('data_nodes is none')
        self.data_nodes = data_nodes

        self.hunger_time = options.hunger_time
        self.food_path = options.food_path

        # block scheduler
        self.scheduler = BlockingScheduler()

    def get_node_status(self, node: DataNode):
        """获取对应的数据，并存储到本地

        获取出来的数据先存储到food_path中去
        """

    def start(self):
        """start to watch the data nodes"""
        for data_node in self.data_nodes:
            self.scheduler.add_job(
                self.get_node_status,
                trigger=IntervalTrigger(seconds=self.hunger_time),
                args=(data_node,)
            )
        self.scheduler.start()

