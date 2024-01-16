#!/usr/bin/env bash

readonly database="fastdb"
readonly test_database="test_fastdb"

psql -U postgres -c "DROP DATABASE ${database}" || sudo -u postgres psql -c "DROP DATABASE ${database}"
psql -U postgres -c "CREATE DATABASE ${database}" || sudo -u postgres psql -c "CREATE DATABASE ${database}"

psql -U postgres -c "DROP DATABASE ${test_database}" || sudo -u postgres psql -c "DROP DATABASE ${test_database}"
psql -U postgres -c "CREATE DATABASE ${test_database}" || sudo -u postgres psql -c "CREATE DATABASE ${test_database}"