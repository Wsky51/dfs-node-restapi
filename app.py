from typing import List

from flask import Flask, request, jsonify
from watchdog import WatchDogOptions, WatchDog
from type import DataNode, DataNodeStatus
from config import options, data_nodes, get_db, datetime_format, get_second_datetime
from utils import sort_and_set_datetime
from db import DB, FileDB, MemoryDB
from flask_cors import CORS
from datetime import datetime

from wechaty_puppet import get_logger


logger = get_logger(__name__)

app = Flask(__name__)

CORS(app)

db = get_db()


def success(msg):
    return jsonify({"code": 200, "msg": msg})


def data(json_data):
    return jsonify({"code": 200, "data": json_data})


def error(msg):
    return jsonify({"code": 500, "msg": msg})


@app.route('/', methods=['GET'])
def site():
    """show the vue dist files"""
    return ''


@app.route('/status/<string:node_id>', methods=['GET'])
def health_status(node_id: str):
    # TODO: get the health status from the child node
    logger.info(f'health_status({node_id}) ')
    node_status = db.get(node_id)
    return data(node_status)


@app.route('/all_status', methods=['GET'])
def get_all_node_status():

    status = db.get_all()

    if not status:
        return []

    # 构造前端对应的数据
    node_ids = [data_node.node_id for data_node in data_nodes]
    series_data = []
    all_times: List[datetime] = []
    for node_id in node_ids:
        if node_id in status:
            node_status = status[node_id]
            used_data = {
                "name": node_id,
                "type": "line",
                "stack": "使用量",
                "data": [status.used for status in node_status]
            }
            series_data.append(used_data)
            all_times.extend([node.datetime for node in node_status])

    return data({'legend': node_ids, "series": series_data, "time": sort_and_set_datetime(all_times)})


@app.route('/login', methods=['POST'])
def login():
    form_data = request.get_json()
    # TODO: should validation from the database later
    if form_data['username'] == 'admin':
        return success('登录成功')
    return error('登录失败')


if __name__ == '__main__':
    # 开始运行整体程序
    logger.info('start the server ...')
    watch_dog = WatchDog(
        options=options,
        data_nodes=data_nodes,
        db=db
    )
    watch_dog.start()
    logger.info('server has been started ...')
    app.run(port=5000, host='0.0.0.0')
