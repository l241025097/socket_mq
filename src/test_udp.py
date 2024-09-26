import socket

ipv4 = socket.gethostbyname_ex(socket.gethostname())[2][0]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = b"".join([b"Michael", b"Tracy", b"Sarah"] * 1000)
s.sendto(data, (ipv4, 12345))
s.close()
