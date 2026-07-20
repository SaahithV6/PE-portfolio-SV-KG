#!/bin/bash

set -e

cd /root/PE-portfolio-SV-KG

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build
