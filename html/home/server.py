#!/usr/bin/env python3
"""Servidor local para o Home Dashboard — lê e escreve tarefas."""

import json
import os
import subprocess
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))
LISTA = os.path.join(BASE, "tarefas", "lista.txt")
CONCLUIDAS = os.path.join(BASE, "tarefas", "concluidas.txt")
PORT = 7878


def ler_tarefas():
    if not os.path.exists(LISTA):
        return []
    with open(LISTA, "r", encoding="utf-8") as f:
        linhas = f.read().splitlines()
    return [l.strip() for l in linhas if l.strip()]


def salvar_tarefas(lista):
    with open(LISTA, "w", encoding="utf-8") as f:
        f.write("\n".join(lista) + "\n" if lista else "")


def concluir_tarefa(idx):
    tarefas = ler_tarefas()
    if idx < 0 or idx >= len(tarefas):
        return False, "Índice inválido"
    tarefa = tarefas.pop(idx)
    salvar_tarefas(tarefas)
    hoje = date.today().strftime("%Y.%m.%d")
    # extrai só o texto da tarefa (sem prioridade)
    texto = tarefa.split("|")[0].strip()
    linha = f"{hoje}. {texto}"
    with open(CONCLUIDAS, "a", encoding="utf-8") as f:
        f.write(linha + "\n")
    return True, linha


def tocar_som():
    som = os.path.join(BASE, "sound", "luna.tarefa.concluida.mp3")
    subprocess.Popen(["afplay", som])


def nova_tarefa(texto, prioridade="🟡 Média"):
    linha = f"{texto} | {prioridade}"
    tarefas = ler_tarefas()
    tarefas.append(linha)
    salvar_tarefas(tarefas)
    return linha


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silencia logs

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/tarefas":
            self._json({"tarefas": ler_tarefas()})
        elif parsed.path == "/ping":
            self._json({"ok": True})
        else:
            self._json({"erro": "rota não encontrada"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if parsed.path == "/tarefas/nova":
            texto = body.get("texto", "").strip()
            prioridade = body.get("prioridade", "🟡 Média")
            if not texto:
                self._json({"erro": "texto vazio"}, 400)
                return
            linha = nova_tarefa(texto, prioridade)
            self._json({"ok": True, "linha": linha})

        elif parsed.path == "/tarefas/concluir":
            idx = body.get("idx")
            if idx is None:
                self._json({"erro": "idx obrigatório"}, 400)
                return
            ok, msg = concluir_tarefa(int(idx))
            if ok:
                tocar_som()
            self._json({"ok": ok, "msg": msg})

        else:
            self._json({"erro": "rota não encontrada"}, 404)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Home server rodando em http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
