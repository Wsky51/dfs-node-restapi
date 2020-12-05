from flask import Flask, request, jsonify
from watchdog import WatchDogOptions, WatchDog
from type import DataNode, DataNodeStatus
from config import options, data_nodes, db
from db import DB, FileDB, MemoryDB

app = Flask(__name__)


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
    node_status = db.get(node_id)
    return data(node_status)


@app.route('/all_status', methods=['GET'])
def get_all_node_status():
    status = db.get_all()
    return data(status)


@app.route('/login', methods=['POST'])
def login():
    form_data = request.get_json()
    # TODO: should validation from the database later
    if form_data['username'] == 'admin':
        return success('登录成功')
    return error('登录失败')


if __name__ == '__main__':
    # 开始运行整体程序
    watch_dog = WatchDog(
        options=options,
        data_nodes=data_nodes
    )
    watch_dog.start()
    app.run()
