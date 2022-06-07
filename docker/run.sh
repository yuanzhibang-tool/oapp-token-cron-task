#! /bin/bash
# 请cd到本文件所在目录执行
# !第一种方式,先构建image
docker build -t oapp-token-cron-task:default -f Dockerfile ..
# 执行并配置参数
docker run -d --restart always \
-v /root/github/oapp-token-cron-task/docker/config.yaml:/scripts/config.yaml #! 挂载配置必须挂载
# -v /root/github/oapp-token-cron-task/docker/logs:/root/.pm2/logs # 挂载日志方便查阅
oapp-token-cron-task:default \

# !第二种方式,直接通过打包好的公开镜像执行
docker run -d --restart always \
-v /root/github/oapp-token-cron-task/docker/config.yaml:/scripts/config.yaml  #! 挂载配置必须挂载
# -v /root/github/oapp-token-cron-task/docker/logs:/root/.pm2/logs # 挂载日志方便查阅
yuanzhibang/oapp-token-cron-task:default \