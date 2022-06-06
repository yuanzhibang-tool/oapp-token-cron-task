# oapp-token-cron-task

猿之棒开放平台 OAuth2.0 相关`token`自动更新任务,可以通过阿里云函数计算或者类似服务,`docker`,`pm2` 进行部署,在 `config.yaml` 中配置好后,一键可用.

注意: 1.使用前请务必在 `open.yuanzhibang.com` 应用里将当前服务器的`外网 ip` 设置为服务器白名单,推荐通过在`config.yaml`中配置代理服务器来获取该操作,以实现一台服务器白名单,处处可用的方案,下方可通过`docker`一键部署代理服务器
