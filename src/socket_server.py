import os
import socket
from utils import get_log, connect_mq
from datetime import datetime

def create_server(port=12345):
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地机器的IP地址
    localhost = socket.gethostbyname(socket.gethostname())
    # 绑定socket到地址
    server_socket.bind((localhost, port))  # 端口号12345可以更改为其他未被占用的端口
    # 监听连接请求，最多同时连接5个
    server_socket.listen(5)
    return server_socket

def execute(socket_server, log_obj):

    while True:
        # 接受一个新的连接
        client_socket, _ = socket_server.accept()
        
        # 接收客户端发送的数据
        received_message = client_socket.recv(1024)  # 1024是接收数据的缓冲区大小
        received_message_str = received_message.decode('utf-8')
        connection, channel = connect_mq()
        try:
            channel.basic_publish(
                exchange='', # 当前是一个简单模式，所以这里设置为空字符串就可以了
                routing_key='sms', # 指定消息要发送到哪个queue
                body=received_message # 指定要发送的消息,
            )
        except Exception as err:
            log_obj.exception(err)
        finally:
            connection.close()
        # 打印从客户端接收到的消息
        log_obj.info("Received message: " + received_message_str)
        
        # 发送一个响应消息给客户端
        response_message = "Hello, Client! I received your message.".encode('utf-8')
        client_socket.send(response_message)
        
        # 关闭与客户端的连接
        client_socket.close()


if __name__ == "__main__":
    BEGIN = datetime.now()
    APP_NAME = f"internet_msg_project"
    log_obj = get_log(APP_NAME)
    log_obj.info(f"start: {BEGIN}".center(100, "-"))
    socket_server = create_server()
    try:
        execute(socket_server, log_obj)
    except KeyboardInterrupt:
        # 当用户按下Ctrl+C，服务器将优雅地关闭所有资源
        socket.close()
        print("Server closed.")
    except Exception as err:
        log_obj.exception(err)
    END = datetime.now()
    DURATION = (END - BEGIN).total_seconds()
    log_obj.info(f"end: {END}, duration: {DURATION:.2f} s".center(100, "-"))
