include:
  - pkgs.postgres

django:
  postgres_user.present:
    - password: django2235
    - superuser: True
    - inherit: True

django_db:
  postgres_database.present:
    - owner: django
