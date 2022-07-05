#!/bin/bash

set -e

TESTENV="$(mktemp -p . -d)"

if [ -d "sable_reader/dist" ]
then
    rm -r "sable_reader/dist"
fi

(cd sable_reader && python3 -m build)
PACKAGE=$(find sable_reader -name "*.tar.gz")
if [ $(echo "${PACKAGE}" | wc -l ) -ne 1 ]
then
    echo "FATAL - failed to get newly build package" >&2
    exit 1
fi

python3 -m venv "${TESTENV}"
. "${TESTENV}/bin/activate"
python3 -m pip install "${PACKAGE}"
python3 sable_reader/tests/test_sable_reader.py

echo "DONE"