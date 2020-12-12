from dataclasses import dataclass
from typing import List, Optional
from db import JsonDB
from type import DataNode
from datetime import datetime
import struct


@dataclass
class WatchDogOptions:
    hunger_time: int
    food_path: Optional[str] = None

name_node_ip="10.103.9.11"
name_node_port = 24269  # NameNode监听端口

PACK_SIZE = 1024
PACK_SIZE_FMT = str(PACK_SIZE) + 's'

# 每10秒钟获取一次数据
options = WatchDogOptions(
    hunger_time=10,
)

datetime_format = "%Y-%m-%d %H:%M:%S"

data_nodes: List[DataNode] = [
    DataNode(endpoint='thumm02', port=5000, node_id='thumm02'),
    DataNode(endpoint='thumm03', port=5000, node_id='thumm03'),
    DataNode(endpoint='thumm04', port=5000, node_id='thumm04'),
]


def get_db() -> JsonDB:
    # save data to the json file
    # cwd = os.getcwd()
    # file_path = os.path.join(cwd, 'db.json')
    # file_db = FileDB(file=file_path)
    return JsonDB()


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


def strong_sck_send(socket, data):
    size = len(data)
    idx = 0

    # 先告知对端目前要发送的数据量大小是多少
    socket.send(struct.pack('L', size))
    while idx < size - PACK_SIZE:
        unpack = struct.unpack_from(PACK_SIZE_FMT, data, idx)[0]
        idx += PACK_SIZE

        # 依次发送数据

        socket.sendall(unpack)
    # 解析最后的不到PACK_SIZE的数据并发送
    last = size - idx
    unpack = struct.unpack_from(str(last) + 's', data, idx)[0]
    socket.sendall(unpack)


# 返回未经编码的比特流
def strong_sck_recv(socket):
    data_info_size = struct.calcsize('L')
    # 接收大小信息
    buf = socket.recv(data_info_size)

    print("common.py接收的buf:", buf)
    # while buf==b'':
    #     time.sleep(0.1)
    #     buf = socket.recv(data_info_size)

    # 接收端接受数据大小信息
    data_size = struct.unpack('L', buf)[0]
    recvd_size = 0  # 定义已接收文件的大小

    res = b''
    while not recvd_size == data_size:
        if data_size - recvd_size > PACK_SIZE:
            data = socket.recv(PACK_SIZE)
            recvd_size += len(data)
            res += data
        else:
            data = socket.recv(data_size - recvd_size)
            recvd_size = data_size
            res += data
    return res


def str_encode_utf8(strdata):
    return bytes(strdata, encoding='utf-8')


def utf8_decode_str(data):
    return str(data, encoding='utf-8')

db = get_db()
