FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
#! 使用阿里云源,不需要可以注掉
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bk; rm -rf /etc/apt/sources.list; touch /etc/apt/sources.list;
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\n\
    deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n\
    deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n'\
    > /etc/apt/sources.list

RUN echo 'start build'
RUN LC_ALL=C.UTF-8
#配置xdebug
RUN apt update
RUN apt -y upgrade
RUN apt install -y curl
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt install -y nodejs python3 python3-pip pipenv
RUN npm install -g npm
RUN npm install -g pm2
RUN pm2 startup
ADD scripts /scripts
RUN cd /scripts && pipenv install --system
ENTRYPOINT cd /scripts && ./run.sh
