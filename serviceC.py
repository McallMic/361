import http.server
import json
import os
#Restore and Remove tasks (I.E moving tasks between the two text files)
class TaskMovementHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/move-task":
            # Parse JSON body of the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                source_path = data.get('sourcePath')
                target_path = data.get('targetPath')
                task_number = data.get('taskNumber')
                direction = data.get('direction')  # 'toTrash' or 'fromTrash'

                if not all([source_path, target_path, task_number, direction]):
                    self.send_error(400, "Missing required fields in request.")
                    return

                # Check if files exist
                if not os.path.exists(source_path) or not os.path.exists(target_path):
                    self.send_error(404, "Required files do not exist.")
                    return

                # Read source file
                with open(source_path, 'r') as file:
                    source_lines = file.readlines()

                # Find and remove the task
                task_found = False
                moved_task = None
                remaining_lines = []
                new_number = 1

                for line in source_lines:
                    if line.strip():  # Skip empty lines
                        current_number = line.split('-')[0].strip()
                        if current_number == str(task_number):
                            task_found = True
                            moved_task = line.strip()
                        else:
                            # Renumber remaining tasks
                            remaining_lines.append(f"{new_number} -{line.split('-', 1)[1]}")
                            new_number += 1

                if not task_found:
                    self.send_error(404, f"Task number {task_number} not found.")
                    return

                # Write remaining tasks back to source file
                with open(source_path, 'w') as file:
                    file.write('\n'.join(remaining_lines))
                    if remaining_lines:
                        file.write('\n')

                # Read target file to determine new task number
                with open(target_path, 'r') as file:
                    target_lines = file.readlines()
                    new_task_number = len([l for l in target_lines if l.strip()]) + 1

                # Add moved task to target with new number
                task_content = moved_task.split('-', 1)[1].strip()
                new_task = f"{new_task_number} - {task_content}"
                
                with open(target_path, 'a') as file:
                    if os.path.getsize(target_path) > 0 and not target_path.endswith('\n'):
                        file.write('\n')
                    file.write(new_task + '\n')

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "message": "Task moved successfully",
                    "movedTask": new_task
                }).encode())

            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found.")

if __name__ == "__main__":
    server_address = ('', 8082)  # Using port 8082 to avoid conflict with other services
    httpd = http.server.HTTPServer(server_address, TaskMovementHandler)
    print("Task Movement Microservice is running on port 8082...")
    httpd.serve_forever()