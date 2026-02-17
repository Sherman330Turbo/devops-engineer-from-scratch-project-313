#!/usr/bin/env bash
set -e

python3 -m flask --app src/main.py run --host=127.0.0.1 --port=8080 &
BACK_PID=$!

term() { kill -TERM "$BACK_PID" 2>/dev/null || true; }
trap term SIGTERM SIGINT

nginx -g 'daemon off;' &
NGINX_PID=$!

wait -n "$BACK_PID" "$NGINX_PID"
term
kill -TERM "$NGINX_PID" 2>/dev/null || true
wait || true