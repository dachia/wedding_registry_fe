include:
  - pkgs.nginx

/etc/nginx/nginx.conf:
  file.managed:
    - template: 'jinja'
    - source: salt://server/templates/nginx.conf
    - defaults:
        pid: '/var/run/nginx.pid'
        worker_connections: '4096'
        server_names_hash_bucket_size: '64'
        client_max_body_size: '10M'
        sendfile: 'on'
        keepalive_timeout: '65'
        tcp_nodelay: 'on'
        server_tokens: 'off'
        access_log: '/var/log/nginx/access.log'
        log_format: |
            '{ "timestamp": "$time_iso8601", '
              '"nginx_be": { "remote_addr": "$remote_addr",'
                            '"remote_user": "$remote_user", '
                            '"body_bytes_sent": "$body_bytes_sent", '
                            '"request_time": "$request_time", '
                            '"status": "$status", '
                            '"request": "$request", '
                            '"request_method": "$request_method", '
                            '"http_referrer": "$http_referer", '
                            '"http_user_agent": "$http_user_agent" } }'
        gzip: 'on'
        gzip_disable: '"MSIE [1-6]\.(?!.*SV1)"'
        gzip_types: 'application/x-javascript text/css'
        ssl_session_cache: 'shared:SSL:100m'
        ssl_session_timeout: '10m'
    - require:
        - pkg: nginx

/etc/nginx/sites-available/app.conf:
  file.managed:
    - user: 'root'
    - group: 'root'
    - mode: '644'
    - template: 'jinja'
    - source: salt://server/templates/nginx_vhost.conf
    - require:
      - file: /etc/nginx/nginx.conf

/etc/nginx/sites-enabled/app.conf:
  file.symlink:
    - target: /etc/nginx/sites-available/app.conf
    - require:
      - file: /etc/nginx/sites-available/app.conf
      - pkg: nginx

/etc/nginx/sites-available/default:
  file.absent:
    - require:
      - pkg: nginx

/etc/nginx/sites-enabled/default:
  file.absent:
    - require:
      - pkg: nginx

nginx running:
  service.running:
    - name: nginx
    - reload: True
    - watch:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf
