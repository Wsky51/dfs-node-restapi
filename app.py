from typing import List

from flask import Flask, request, jsonify
from watchdog import WatchDogOptions, WatchDog
from type import DataNode, DataNodeStatus
from config import *
from flask_cors import CORS
from datetime import datetime
import socket
from db import JsonDB

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


# test data
@app.route('/hello', methods=['GET'])
def hello():
    name_node_sock = socket.socket()
    name_node_sock.connect((name_node_ip, name_node_port))

    request = "getAllData"
    strong_sck_send(name_node_sock, str_encode_utf8(request))
    # fat_pd = self.name_node_sock.recv(BUF_SIZE)
    res = strong_sck_recv(name_node_sock)
    res = utf8_decode_str(res)
    return "res:" + res


@app.route('/all_status', methods=['GET'])
def get_all_node_status():
    db = JsonDB()
    status = db.get(show_data_num)

    nodes, time_lines, series = [], [], {}
    if status:
        nodes = status[0]['host_list']
        for item in status:
            time_lines.append(item['curr_time'])
            for data_node in item['data_node_info']:

                if data_node['host'] not in series:
                    series[data_node['host']] = {
                        "name": data_node['host'],
                        "type": "line",
                        "data": [],
                        "metadata": [],
                    }
                prop = data_node['mem_prop']
                prop = prop[:-1]
                series[data_node['host']]['data'].append(float(prop))
                series[data_node['host']]['metadata'].append(data_node)

    summary = status[0] if status else {}
    return data({
        "nodes": nodes,
        "time_lines": time_lines,
        "series": [value for key, value in series.items()],
        "summary": summary
    })


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
    )
    watch_dog.start()
    logger.info('server has been started ...')
    app.run(port=5000, host='0.0.0.0')
