include:
  - pkgs.postgres

django:
  postgres_user.present:
    - superuser: True
    - inherit: True

django_db:
  postgres_database.present:
    - owner: django
