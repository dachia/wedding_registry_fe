include:
  - .python-pip
  - .build-essential
  - .python-dev

uwsgi:
  pip.installed:
    - require:
      - pkg: python-pip
      - pkg: build-essential
      - pkg: python-dev
