from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("""
            <html>
                <head>
                    <title>Subir Archivo</title>
                </head>
                <body>
                    <form method="post" enctype="multipart/form-data">
                        File: <input name="file" type="file">
                        <input type="submit" value="Subir">
                    </form>
                </body>
            </html>
        """.encode('utf-8'))

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        # Recibe el archivo subido y lo guarda en el directorio actual
        field_item = form['file']
        if field_item.filename:
            file_data = field_item.file.read()
            file_name = field_item.filename
            with open(file_name, "wb") as f:
                f.write(file_data)
            self._set_response()
            self.wfile.write("Archivo {} subido exitosamente\n".format(file_name).encode('utf-8'))
        else:
            self._set_response()
            self.wfile.write("No se subio ningun archivo\n".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()



