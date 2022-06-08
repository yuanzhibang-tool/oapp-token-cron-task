# oapp-token-cron-task

使用 `docker-compose` 一键部署,请参照:https://github.com/yuanzhibang-tool/docker/tree/main/oapp-code-docker-compose

猿之棒开放平台 OAuth2.0 相关`token`自动更新任务,可以通过阿里云函数计算或者类似服务,`docker`,`pm2` 进行部署,在 `config.yaml` 中配置好后,一键可用.

注意: 1.使用前请务必在 `open.yuanzhibang.com` 应用里将当前服务器的`外网 ip` 设置为服务器白名单,推荐通过在`config.yaml`中配置代理服务器来获取该操作,以实现一台服务器白名单,处处可用的方案,下方可通过`docker`一键部署代理服务器

_1.使用 docker 部署(推荐):_

请参照 `docker/run.sh`中备注使用

_2.使用阿里云函数计算处理(推荐)_

请参照 `scripts/index.py`中的说明使用

_3.在本机上直接运行(不推荐)_

请参照 `docker/Dockerfile`中的`RUN`命令来配置本机依赖环境

然后在`scripts`目录下运行

```
pm2 start update_server_access_token.yaml
pm2 start update_js_ticket.yaml
pm2 save
```

---

### REDIS 中缓存 token 内容格式

_js_ticket:_

| key                                         | value                                                                                                         |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `type/js_ticket_info/app_id/开放平台应用id` | `{"js_ticket": "082675bb1bcbdc3b824fb040abdfd4e4b5e36e422af60365949e17e372cbcd4c", "expires_in": 1654575742}` |

注意:`expires_in` 为过期的 `unix` 时间戳,后台无需关系该过期日期,该定时任务会更新,保证该 `code` 为最新可用的 `code`

---

_server_access_token:_

| key                                                    | value                                                                                                                   |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `ttype/server_access_token_info/app_id/开放平台应用id` | `{"server_access_token": "fa4d97f4872e8e2a39ba742ad6792f042dd825c76c85057808e1c68c17c31cdc", "expires_in": 1654576906}` |

注意:所有信息存于`REDIS DB0`,`expires_in` 为过期的 `unix` 时间戳,后台无需关系该过期日期,该定时任务会更新,保证该 `code` 为最新可用的 `code`
