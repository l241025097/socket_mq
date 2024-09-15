import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipv4=socket.gethostbyname_ex(socket.gethostname())[2][0]
sock.connect((ipv4, 12345))

send_msg = b"test massage"
sock.send(send_msg, )
print(send_msg.decode())
receive_msg = sock.recv(1024).decode()
print(receive_msg)
sock.close()
