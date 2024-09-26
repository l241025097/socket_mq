# docker build -t python_socket:3.10.15 .
FROM python:3.10.15
RUN apt-get clean && apt-get install -y apt-transport-https
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y iputils-ping
RUN apt-get install -y telnet
RUN apt-get install -y traceroute
RUN apt-get install -y libterm-readkey-perl
RUN apt-get install -y locales
RUN apt-get install -y locales-all
RUN locale-gen en_US.UTF-8
RUN echo ":set mouse-=a" > ~/.vimrc
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN apt-get install -y tzdata && dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get install cron rsyslog -y
RUN mkdir -p /root/socket_mq
RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install pika==1.3.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD src.tar /root/socket_mq
WORKDIR /root/socket_mq/src
CMD /usr/local/bin/python3 udp_server.py
