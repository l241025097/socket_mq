# socket_mq
可以通过socket服务端接收任何信息，并将信息发送至RabbitMQ队列，提供给客户端实时消费。场景：手机安装SmsForwarder（短信转发器），配置转发通道，可将手机中的短信通过一个socket服务端转发至消息队列，其他客户端可消费队列获取短信信息。

条件：
（1）具备公有云环境（公网地址，并暴露访问端口）；
（2）安装docker。

## 1、切换至项目路径，例如：
cd /home/l241025097/socket_mq

## 2、docker build rabbitmq镜像
docker build -t rabbitmq:3.12.14-management-plugins -f Dockerfile.mq .

## 3、docker build socker服务端镜像
docker build -t python_socket:3.10.15 .

## 4、docker run rabbitmq容器
（1）15672端口为消息队列网页端访问端口；
（2）5672端口为消息队列发送消息和接收消息的端口；
（3）RABBITMQ_DEFAULT_USER和RABBITMQ_DEFAULT_PASS是登录消息队列网页端，以及发送和接收消息时鉴权的用户名和密码。

docker run -d --restart=always \
--hostname internet_mq_server \
--name internet_mq_server \
-p 60003:15672 \
-p 60004:5671 \
-p 60005:5672 \
-e RABBITMQ_DEFAULT_USER=lyn \
-e RABBITMQ_DEFAULT_PASS=123 \
rabbitmq:3.12.14-management-plugins

## 5、docker run socket服务端容器
（1）12345端口为socket服务端接收tcp消息端口；
（2）通过MQ_ADDR、MQ_PORT、MQ_USER、MQ_PASS指定发送的消息队列；
（3）容器/root/socket_mq/src/logs路径为socket服务端日志输出路径。

docker run -d \
--restart=always \
--name internet_socket_server \
-p 60002:12345 \
-e MQ_ADDR=公有云IP \
-e MQ_PORT=rabbitmq容器5672端口的映射端口，例60005 \
-e MQ_USER=同RABBITMQ_DEFAULT_USER \
-e MQ_PASS=同RABBITMQ_DEFAULT_PASS \
-v /home/l241025097/socket_mq/src/logs:/root/socket_mq/src/logs \
python_socket:3.10.15

## 6、进入socket服务端容器
docker exec -it internet_socket_server /bin/bash

## 7、在socket服务端容器中操作：发送测试消息
/usr/local/bin/python3 /root/socket_mq/src/test_socket_server.py

## 8、在socket服务端容器中操作：接收测试消息
/usr/local/bin/python3 /root/socket_mq/src/test_mq_client.py
