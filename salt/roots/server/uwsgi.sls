{% set app = salt['pillar.get']('app') %}

include:
  - pkgs.uwsgi

/etc/uwsgi/uwsgi.ini:
  file.managed:
    - template: jinja
    - makedirs: True
    - source: 'salt://server/templates/uwsgi.ini'
    - defaults:
        socket: '127.0.0.1:9001'
        listen: '100'
        workers: '4'
        harakiri: '120'
        harakiri_verbose: 'true'
        master: 'true'
        memory_report: 'true'
        auto_procname: 'true'
        uid: 'root'
        gid: 'root'
        enable_threads: 'true'
        single_interpreter: 'true'
        need_app: 'true'
        die_on_term: 'true'
        no_orphans: 'true'
        no_default_app: 'true'
        log_date: 'true'
        logto: '{{ app.uwsgi_logs }}'
        chdir: '{{ app.app_path}}'
        module: '{{ app.uwsgi_module }}'
        buffer_size: '32768'
        py_autoreload: 1

    - require:
      - pip: uwsgi

/etc/init/uwsgi.conf:
  file.managed:
    - source: 'salt://server/templates/uwsgi_upstart.conf'
    - template: 'jinja'
    - defaults:
        uwsgi_env:
    - require:
      - file: /etc/uwsgi/uwsgi.ini

/var/log/uwsgi:
  file.directory

'run uwsgi':
  service.running:
    - name: uwsgi
    - require:
      - file: /etc/init/uwsgi.conf
      - file: /var/log/uwsgi
