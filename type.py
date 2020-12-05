from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataNode:
    # 子节点的ip地址
    endpoint: str
    # 子节点服务开启的端口
    port: int


@dataclass
class DataNodeStatus:
    # 是否已宕机
    dead: bool
    # 已分配的整体容量
    capacity: int
    # 已使用的容量
    used: int
    # 数据获取的时间
    datetime: datetime
