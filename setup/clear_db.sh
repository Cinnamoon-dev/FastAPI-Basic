#!/usr/bin/env bash

declare database="fastdb"

psql -U postgres -c "DROP DATABASE ${database}" || sudo -u postgres psql -c "DROP DATABASE ${database}"
psql -U postgres -c "CREATE DATABASE ${database}" || sudo -u postgres psql -c "CREATE DATABASE ${database}"