# wuyi-master-node

## Quick Start

- Installation

```shell script
pip install -r requirements.txt
```

- Configuration

在`config.py`文件中配置子节点的相关信息

1. DataNode: 包含`endpoint`(IP地址), `port`(端口号)
2. 多久刷新一次监控数据以及数据保存
3. 配置每次展示数据的条数



- Run Server

```shell script
chmod +x run.sh
./run.sh
```
## 说明
主要配合MyDFS和dfs-node-web项目使用，本项目主要实现restful api，作为前端页面展示的数据源
## 其他信息
主要贡献者：
- https://github.com/wj-Mcat  wj-Mcat(骑马小猫)
- https://github.com/Wsky51 