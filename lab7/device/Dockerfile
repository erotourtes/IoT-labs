FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
                      apt-get install -y \
                        vim iproute2 iputils-ping \
                        net-tools netcat tcpdump \
                        python3-pip openssh-server

RUN echo 'root:12345' | chpasswd

RUN pip3 install aiocoap==0.4.7

WORKDIR /app
COPY server.py .

ENTRYPOINT ["python3", "server.py"]
