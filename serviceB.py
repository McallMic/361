import http.server
import json
import os
#Add task
class TaskAdditionHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/add-task":
            # Parse JSON body of the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                todo_path = data.get('todoPath')
                priority = data.get('priority')
                task_title = data.get('taskTitle')

                if not todo_path or not task_title:
                    self.send_error(400, "Missing required fields in request.")
                    return

                # Check if the todo file exists
                if not os.path.exists(todo_path):
                    self.send_error(404, f"File '{todo_path}' does not exist.")
                    return

                # Read existing tasks to determine new priority if none provided
                with open(todo_path, 'r') as file:
                    lines = file.readlines()
                    if not priority:
                        priority = len(lines) + 1 if lines else 1

                # Add the new task
                with open(todo_path, 'a') as file:
                    if lines and not lines[-1].endswith('\n'):
                        file.write('\n')
                    file.write(f"{priority} - {task_title}\n")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "message": "Task added successfully",
                    "priority": priority,
                    "taskTitle": task_title
                }).encode())

            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found.")

if __name__ == "__main__":
    server_address = ('', 8081)  # Using port 8081 to avoid conflict with trashcan service
    httpd = http.server.HTTPServer(server_address, TaskAdditionHandler)
    print("Task Addition Microservice is running on port 8081...")
    httpd.serve_forever()