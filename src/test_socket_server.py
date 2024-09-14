import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 12345))

send_msg = b"test massage"
sock.send(send_msg)
print(send_msg.decode())
sock.close()
