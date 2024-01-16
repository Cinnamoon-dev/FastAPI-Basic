#!/usr/bin/env bash

readonly database="fastdb"
readonly test_database="test_fastdb"

psql -U postgres -lqt | grep $database &> /dev/null || sudo -u postgres psql -lqt | grep $database &> /dev/null
if [ $? -eq 0 ]; then
    psql -U postgres -c "DROP DATABASE ${database}" || sudo -u postgres psql -c "DROP DATABASE ${database}"
fi

psql -U postgres -c "CREATE DATABASE ${database}" || sudo -u postgres psql -c "CREATE DATABASE ${database}"

psql -U postgres -lqt | grep $test_database &> /dev/null || sudo -u postgres psql -lqt | grep $test_database &> /dev/null
if [ $? -eq 0 ]; then
    psql -U postgres -c "DROP DATABASE ${test_database}" || sudo -u postgres psql -c "DROP DATABASE ${test_database}"
fi

psql -U postgres -c "CREATE DATABASE ${test_database}" || sudo -u postgres psql -c "CREATE DATABASE ${test_database}"