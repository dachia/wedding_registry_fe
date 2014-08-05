{% set app = salt['pillar.get']('app') %}

include:
  - pkgs.python-pip

pip install -r requirements.txt:
  cmd.run:
    - cwd: {{ app.path }}
    - require:
      - pkg: python-pip
