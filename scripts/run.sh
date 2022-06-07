cd /scripts
pm2 start update_server_access_token.yaml
pm2 start update_js_ticket.yaml
pm2 save
tail -f /dev/null