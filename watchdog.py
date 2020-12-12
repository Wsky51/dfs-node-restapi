from typing import List, Optional
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dataclasses import dataclass
from threading import Thread
from wechaty_puppet import get_logger
from config import *
from db import JsonDB
import socket
import uuid

logger = get_logger(__name__)



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
        self.db = JsonDB()

    def get_node_status(self):
        """获取对应的数据，并存储到本地
        获取出来的数据先存储到food_path中去
        """

        name_node_sock = socket.socket()
        name_node_sock.connect((name_node_ip, name_node_port))

        request = "getAllData"
        strong_sck_send(name_node_sock, str_encode_utf8(request))
        # fat_pd = self.name_node_sock.recv(BUF_SIZE)
        data = strong_sck_recv(name_node_sock)
        data = utf8_decode_str(data)

        self.db.save(data)

    def start(self):
        """start to watch the data nodes"""
        logger.info('starting the watch-dog ...')
        self.scheduler.add_job(
            self.get_node_status,
            trigger=IntervalTrigger(seconds=self.hunger_time),
        )
        thread = Thread(target=self.scheduler.start,)
        thread.start()
