import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pika import ConnectionParameters, PlainCredentials, BlockingConnection
MQ_USER = os.environ.get("MQ_USER")
MQ_PASS = os.environ.get("MQ_PASS")

def current_path():
    now_path = os.path.dirname(os.path.abspath(__file__))
    if not now_path:
        return os.getcwd()
    return now_path

def get_log(mission_name):
    log_path = os.path.join(current_path(), "logs", f"{mission_name}.log")
    formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')
    file_handler = RotatingFileHandler(log_path, maxBytes=20971520, backupCount=7, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    log_obj = logging.getLogger(mission_name)
    log_obj.addHandler(file_handler)
    log_obj.addHandler(stdout_handler)
    log_obj.setLevel(logging.INFO)
    return log_obj

def connect_mq(host="10.0.12.17", port=60005, user=MQ_USER, passwd=MQ_PASS, queue="sms"):
    user_info = PlainCredentials(user, passwd) # 用户名和密码
    params = ConnectionParameters(host, port, '/', user_info)
    connection = BlockingConnection(params) # 连接服务器上的RabbitMQ服务
    # 创建一个channel
    channel = connection.channel()
    # 如果指定的queue不存在，则会创建一个queue，如果已经存在 则不会做其他动作，官方推荐，每次使用时都可以加上这句
    channel.queue_declare(queue=queue)
    return connection, channel
