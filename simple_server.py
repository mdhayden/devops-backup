#!/usr/bin/env python3
"""
Simple test web server to debug issues
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Received request: {self.path}")
        
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK - Simple Server Running')
            
        elif self.path == '/' or self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Simple Test Dashboard</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                    .container { max-width: 800px; margin: 0 auto; text-align: center; }
                    .card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🤖 Trading Bot Dashboard - Test Version</h1>
                    <div class="card">
                        <h2>✅ Web Server is Working!</h2>
                        <p>This is a simplified version to test that the web server is running correctly.</p>
                        <p>If you can see this page, the deployment issue is not with the web server itself.</p>
                    </div>
                    <div class="card">
                        <h3>Test Endpoints:</h3>
                        <p><a href="/health" style="color: #ffd700;">/health</a> - Health check</p>
                        <p><a href="/api/test" style="color: #ffd700;">/api/test</a> - Test API</p>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/api/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = '{"status": "OK", "message": "Simple server API test successful", "timestamp": "' + str(__import__('datetime').datetime.now()) + '"}'
            self.wfile.write(response.encode('utf-8'))
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def log_message(self, format, *args):
        logger.info("%s - %s" % (self.address_string(), format % args))

def start_simple_server(port=8080):
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, SimpleHandler)
        logger.info(f"🚀 Simple test server starting on port {port}")
        logger.info("✅ Ready to accept HTTP traffic")
        logger.info(f"🌐 Visit: http://localhost:{port}")
        
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_simple_server()