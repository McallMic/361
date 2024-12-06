import http.server
import json
import os

class TrashcanHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/empty-trashcan":
            #parse JSON body of the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                trashcan_path = data.get('trashcanPath')

                if not trashcan_path:
                    self.send_error(400, "Missing trashcanPath in request.")
                    return

                #check if the trashcan file exists
                if not os.path.exists(trashcan_path):
                    self.send_error(404, f"File '{trashcan_path}' does not exist.")
                    return

                #open the trashcan file and empty its contents
                with open(trashcan_path, 'r+') as file:
                    lines = file.readlines()
                    if lines and lines[0] != '':
                        file.seek(0)
                        file.write('0\n')  #reset the first line
                        file.truncate()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"message": "Trashcan emptied successfully. First line changed to '0'."}).encode())
                    else:
                        self.send_error(400, "The first line is not '1' or the file is empty.")
            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found.")

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, TrashcanHandler)
    print("Trashcan Emptying Microservice is running on port 8080...")
    httpd.serve_forever()