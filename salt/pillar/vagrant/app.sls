app:
  path: /srv/app
  app_path: /srv/app/wed
  uwsgi_module: wed.wsgi:application
  uwsgi_logs: /var/log/uwsgi/app.log
