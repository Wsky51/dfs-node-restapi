# wuyi-master-node

## Quick Start

- Installation

```shell script
pip install -r requirements.txt
```

- Configuration

在`config.py`文件中配置子节点的相关信息

1. DataNode: 包含`endpoint`(IP地址), `port`(端口号)
2. 多久刷新一次监控数据以及数据保存的未知


- Run Server

```shell script
chmod +x run.sh
./run.sh
```