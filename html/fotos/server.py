#!/usr/bin/env python3
"""
Servidor local de conversão HEIC → JPEG
Usa o 'sips' nativo do macOS — suporta todos os formatos iPhone.
Uso: python3 server.py
Depois abra: http://localhost:8765/fotos.html
"""
import os, subprocess, tempfile, mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path

PORT = 8765
BASE_DIR = Path(__file__).parent.resolve()


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {args[0]} {args[1]}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path.lstrip("/")

        # Ping de health-check
        if path == "ping":
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return

        # Servir ficheiros estáticos da pasta
        file_path = BASE_DIR / path if path else BASE_DIR / "fotos.html"
        if not file_path.exists() or not file_path.is_file():
            self.send_response(404)
            self.end_headers()
            return

        mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        data = file_path.read_bytes()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/convert":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        data   = self.rfile.read(length)

        tmp_heic = tmp_jpg = None
        try:
            # Gravar HEIC temporário
            with tempfile.NamedTemporaryFile(suffix=".heic", delete=False) as f:
                f.write(data)
                tmp_heic = f.name

            tmp_jpg = tmp_heic.replace(".heic", ".jpg")

            # Converter com sips (nativo macOS — suporta todos os iPhones)
            result = subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
                 tmp_heic, "--out", tmp_jpg],
                capture_output=True, timeout=30
            )

            if result.returncode != 0 or not os.path.exists(tmp_jpg):
                raise RuntimeError(result.stderr.decode() or "sips falhou")

            jpg_data = Path(tmp_jpg).read_bytes()
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(jpg_data)))
            self.end_headers()
            self.wfile.write(jpg_data)

        except Exception as e:
            print(f"  [ERRO] {e}")
            msg = str(e).encode()
            self.send_response(500)
            self._cors()
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
        finally:
            for p in [tmp_heic, tmp_jpg]:
                try:
                    if p and os.path.exists(p): os.unlink(p)
                except: pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"\n✅  Servidor a correr em http://localhost:{PORT}/fotos.html")
    print(f"   Pasta: {BASE_DIR}")
    print(f"   Pressione Ctrl+C para parar\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor parado.")
