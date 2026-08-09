"""
Zero-dependency Python standard library HTTP Web Server.
Serves static frontend interface and exposes REST API endpoints for resume analysis.
"""
import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

# Import backend analyzer engine
from app.analyzer import ResumeAnalyzer

PORT = 8000
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class ResumeAnalyzerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == "/api/samples":
            self.handle_api_samples()
        else:
            # Serve static files from frontend directory
            super().do_GET()

    def do_POST(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/api/analyze":
            self.handle_api_analyze()
        else:
            self.send_error(404, "Endpoint not found")

    def handle_api_analyze(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode("utf-8"))

            jd_text = payload.get("job_description", "")
            resumes = payload.get("resumes", [])
            custom_weights = payload.get("custom_weights", None)

            # Execute rule-based analysis engine
            analyzer = ResumeAnalyzer(custom_weights=custom_weights)
            results = analyzer.analyze(jd_text, resumes)

            self._send_json_response(results, status=200 if results.get("success") else 400)

        except Exception as e:
            self._send_json_response({
                "success": False,
                "error": f"Server processing error: {str(e)}",
                "rankings": []
            }, status=500)

    def handle_api_samples(self):
        try:
            samples = {
                "jds": {},
                "resumes": []
            }

            # Load sample JDs
            sample_jd_dir = os.path.join(DATA_DIR, "sample_jd")
            if os.path.exists(sample_jd_dir):
                for fname in os.listdir(sample_jd_dir):
                    if fname.endswith(".txt"):
                        key = fname.replace(".txt", "")
                        with open(os.path.join(sample_jd_dir, fname), "r", encoding="utf-8") as f:
                            samples["jds"][key] = f.read()

            # Load sample Resumes
            sample_res_dir = os.path.join(DATA_DIR, "sample_resumes")
            if os.path.exists(sample_res_dir):
                for fname in sorted(os.listdir(sample_res_dir)):
                    if fname.endswith(".txt"):
                        name = fname.replace(".txt", "").replace("_", " ").title()
                        with open(os.path.join(sample_res_dir, fname), "r", encoding="utf-8") as f:
                            samples["resumes"].append({"name": name, "text": f.read()})

            self._send_json_response(samples, status=200)

        except Exception as e:
            self._send_json_response({"error": str(e)}, status=500)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _send_json_response(self, data: dict, status: int = 200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)


def run_server():
    global PORT
    handler = ResumeAnalyzerHandler
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True

    for port_attempt in range(PORT, PORT + 10):
        try:
            with socketserver.TCPServer(("", port_attempt), handler) as httpd:
                print("=" * 70)
                print("        INTELLIGENT RESUME ANALYZER WEB SERVER")
                print("=" * 70)
                print(f" Server running at: http://localhost:{port_attempt}")
                print(f" Web Dashboard:    http://localhost:{port_attempt}/index.html")
                print(" Zero external dependencies / 100% Python Standard Library")
                print(" Press Ctrl+C to stop the server.")
                print("=" * 70)
                httpd.serve_forever()
                break
        except OSError:
            print(f"Port {port_attempt} is in use, trying port {port_attempt + 1}...")


if __name__ == "__main__":
    run_server()
