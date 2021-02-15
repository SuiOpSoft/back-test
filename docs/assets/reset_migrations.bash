rm -R -f ./migrations &&
pipenv run init &&
psql -U gitpod -c 'DROP DATABASE suiopsoft;' || true &&
psql -U gitpod -c 'CREATE DATABASE suiopsoft;' &&
psql -U gitpod -c 'CREATE EXTENSION unaccent;' -d suiopsoft &&
pipenv run migrate &&
pipenv run upgrade