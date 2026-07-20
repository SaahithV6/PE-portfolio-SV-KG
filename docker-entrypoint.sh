#!/bin/bash
set -e

echo "Waiting for MySQL at ${MYSQL_HOST:-mysql}..."
for i in $(seq 1 90); do
  if python - <<'PY'
import os
import sys
import pymysql

try:
    pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "mysql"),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        connect_timeout=3,
    ).close()
except Exception as exc:
    print(exc)
    sys.exit(1)
PY
  then
    echo "MySQL is ready."
    exec flask run --host=0.0.0.0
  fi
  sleep 2
done

echo "MySQL did not become ready in time."
exit 1
