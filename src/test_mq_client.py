from utils import connect_mq
from json import loads

connection, channel = connect_mq()

mail_list = []

# 回调函数
def callback(ch, method, properties, body):
    body_str = body.decode()
    msg_dict = loads(body_str)
    msg_list = msg_dict["msg"].split("\n")
    msg_content = msg_list[1]
    mail_list.append(msg_content)
    print(f'消费者收到: {body_str}')
    ch.stop_consuming()

# channel: 包含channel的一切属性和方法
# method: 包含 consumer_tag, delivery_tag, exchange, redelivered, routing_key
# properties: basic_publish 通过 properties 传入的参数
# body: basic_publish发送的消息


channel.basic_consume(
    queue='sms',  # 接收指定queue的消息
    auto_ack=True,  # 指定为True，表示消息接收到后自动给消息发送方回复确认，已收到消息
    on_message_callback=callback  # 设置收到消息的回调函数
)

print('Waiting for messages. To exit press CTRL+C')

# 一直处于等待接收消息的状态，如果没收到消息就一直处于阻塞状态，收到消息就调用上面的回调函数
channel.start_consuming()
