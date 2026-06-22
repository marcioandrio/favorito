#!/bin/bash
# Inicia o servidor do Home Dashboard e abre no Brave

DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=7878

# Mata servidor anterior se estiver rodando
lsof -ti :$PORT | xargs kill -9 2>/dev/null

# Inicia servidor em background
python3 "$DIR/server.py" &
SERVER_PID=$!

sleep 0.8

# Abre no Brave
open -a "Brave Browser" "$DIR/home.html"

echo "Home Dashboard iniciado (PID $SERVER_PID)"
echo "Pressione Ctrl+C para encerrar o servidor."

wait $SERVER_PID
