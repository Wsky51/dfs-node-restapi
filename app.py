from flask import Flask, request, jsonify
from watchdog import WatchDogOptions, WatchDog
from type import DataNode, DataNodeStatus

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


@app.route('/status', methods = ['GET'])
def health_status():
    # TODO: get the health status from the child node
    return data({})


@app.route('/login', methods=['POST'])
def login():
    form_data = request.get_json()
    # TODO: should validation from the database later
    if form_data['username'] == 'admin':
        return success('登录成功')
    return error('登录失败')


if __name__ == '__main__':
    # 配置所有的子节点
    data_nodes = [
        DataNode(endpoint='127.0.0.2', port=5000),
        DataNode(endpoint='127.0.0.3', port=5000),
        DataNode(endpoint='127.0.0.4', port=5000),
    ]
    # 开始运行整体程序
    watch_dog = WatchDog(
        options=WatchDogOptions(hunger_time=3000, food_path='./node_status.json'),
        data_nodes=data_nodes
    )
    watch_dog.start()
    app.run()
