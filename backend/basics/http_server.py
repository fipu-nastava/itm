from http.server import HTTPServer, BaseHTTPRequestHandler


class DemoHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):

        content = "<html><body><h1>{0}</h1></body></html>".format(message)
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()

        content = "Invalid Resource"

        if self.path == "/":
            content = "Home page!"

        elif self.path == "/test":
            content = "Test page!"

        elif self.path == "/test2":
            content = "Test page 2!"

        self.wfile.write(self._html(content))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write(self._html("POST!"))

    def do_PATCH(self):
        self._set_headers()
        self.wfile.write(self._html("PATCH!"))

    def do_DELETE(self):
        self._set_headers()
        self.wfile.write(self._html("PATCH!"))


def run(server_class=HTTPServer, handler_class=DemoHandler, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd server on {0}:{1}".format(addr, port))
    httpd.serve_forever()


if __name__ == "__main__":
    run(addr="localhost", port=8000)
