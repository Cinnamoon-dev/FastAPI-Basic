#!/usr/bin/env bash

readonly database="fastdb"
readonly test_database="test_fastdb"
readonly database_list=$(psql -U postgres -lqt 2> /dev/null || sudo -u postgres psql -lqt 2> /dev/null)

echo $database_list | grep $database &> /dev/null
if [ $? -eq 0 ]; then
    psql -U postgres -c "DROP DATABASE ${database}" || sudo -u postgres psql -c "DROP DATABASE ${database}"
fi

psql -U postgres -c "CREATE DATABASE ${database}" || sudo -u postgres psql -c "CREATE DATABASE ${database}"

echo $database_list | grep $test_database &> /dev/null
if [ $? -eq 0 ]; then
    psql -U postgres -c "DROP DATABASE ${test_database}" || sudo -u postgres psql -c "DROP DATABASE ${test_database}"
fi

psql -U postgres -c "CREATE DATABASE ${test_database}" || sudo -u postgres psql -c "CREATE DATABASE ${test_database}"