import http.server
import json
import os
#Reordering tasks
class TaskReorderHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/reorder-task":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                todo_path = data.get('todoPath')
                current_priority = data.get('currentPriority')
                new_priority = data.get('newPriority')

                if not all([todo_path, current_priority, new_priority]):
                    self.send_error(400, "Missing required fields in request.")
                    return

                # Check if file exists
                if not os.path.exists(todo_path):
                    self.send_error(404, "ToDo file not found.")
                    return

                # Read all tasks
                with open(todo_path, 'r') as file:
                    lines = [line.strip() for line in file.readlines() if line.strip()]

                # Validate priorities
                total_tasks = len(lines)
                if current_priority < 1 or current_priority > total_tasks:
                    self.send_error(400, f"Current priority must be between 1 and {total_tasks}")
                    return
                if new_priority < 1 or new_priority > total_tasks:
                    self.send_error(400, f"New priority must be between 1 and {total_tasks}")
                    return

                # Find the task to move
                task_to_move = None
                remaining_tasks = []

                for line in lines:
                    priority = int(line.split('-')[0].strip())
                    if priority == current_priority:
                        task_to_move = line.split('-', 1)[1].strip()
                    else:
                        remaining_tasks.append(line.split('-', 1)[1].strip())

                if not task_to_move:
                    self.send_error(404, f"Task with priority {current_priority} not found")
                    return

                # Insert task at new position and adjust other priorities
                final_tasks = []
                inserted = False
                current_pos = 1

                for task in remaining_tasks:
                    if current_pos == new_priority:
                        final_tasks.append(f"{current_pos} - {task_to_move}")
                        inserted = True
                        current_pos += 1
                    final_tasks.append(f"{current_pos} - {task}")
                    current_pos += 1

                # Handle case where new position is last
                if not inserted:
                    final_tasks.append(f"{new_priority} - {task_to_move}")

                # Write updated tasks back to file
                with open(todo_path, 'w') as file:
                    file.write('\n'.join(final_tasks))
                    file.write('\n')

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "message": "Task reordered successfully",
                    "newPosition": new_priority
                }).encode())

            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found.")

if __name__ == "__main__":
    server_address = ('', 8083)  # Using port 8083 to avoid conflict with other services
    httpd = http.server.HTTPServer(server_address, TaskReorderHandler)
    print("Task Reordering Microservice is running on port 8083...")
    httpd.serve_forever()