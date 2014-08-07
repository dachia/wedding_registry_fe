{% set app = salt['pillar.get']('app') %}

include:
  - pkgs.postgres
  - pkgs.python-pip
  - pkgs.build-essential
  - pkgs.python-dev

pip install -r requirements.txt:
  cmd.run:
    - cwd: {{ app.path }}
    - require:
      - sls: pkgs.postgres
      - sls: pkgs.python-pip
      - sls: pkgs.build-essential
      - sls: pkgs.python-dev
