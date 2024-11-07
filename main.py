import tkinter as tk
from tkinter import ttk
import os

class TodoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.root.geometry("800x600")
        self.create_files()
        self.task_update_id = None
        self.trash_update_id = None
        
        self.create_welcome_page()

    def create_files(self):
        if not os.path.exists("ToDo.txt"):
            with open("ToDo.txt", "w") as f:
                f.write("")
        
        if not os.path.exists("Trash.txt"):
            with open("Trash.txt", "w") as f:
                f.write("")

    def cancel_updates(self):
        if self.task_update_id:
            self.root.after_cancel(self.task_update_id)
            self.task_update_id = None
        if self.trash_update_id:
            self.root.after_cancel(self.trash_update_id)
            self.trash_update_id = None

    def create_add_task_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Task")
        popup.geometry("400x200")
        popup.transient(self.root)
        popup.grab_set()
        input_frame = ttk.Frame(popup, padding="20")
        input_frame.pack(fill=tk.BOTH, expand=True)

        priority_label = ttk.Label(input_frame, text="Optional Priority Number:")
        priority_label.pack(anchor=tk.W)
        priority_entry = ttk.Entry(input_frame, width=10)
        priority_entry.pack(anchor=tk.W, pady=(0, 10))
        title_label = ttk.Label(input_frame, text="Task Title:")
        title_label.pack(anchor=tk.W)
        title_entry = ttk.Entry(input_frame)
        title_entry.pack(fill=tk.X, pady=(0, 20))
        done_btn = ttk.Button(
            input_frame,
            text="Enter",
            command=popup.destroy
        )
        done_btn.pack()

    def create_change_order_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Change Order")
        popup.geometry("200x200")
        popup.transient(self.root)
        popup.grab_set()
        input_frame = ttk.Frame(popup, padding="20")
        input_frame.pack(fill=tk.BOTH, expand=True)
        priority_label = ttk.Label(input_frame, text="Current Task Priority:")
        priority_label.pack(anchor=tk.W)
        priority_entry = ttk.Entry(input_frame, width=10)
        priority_entry.pack(anchor=tk.W, pady=(0, 10))
        title_label = ttk.Label(input_frame, text="New Task Priority:")
        title_label.pack(anchor=tk.W)
        title_entry = ttk.Entry(input_frame, width=10)
        title_entry.pack(anchor=tk.W, pady=(0, 20))


        done_btn = ttk.Button(
            input_frame,
            text="Enter",
            command=popup.destroy
        )
        done_btn.pack()

    def create_remove_task_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Remove Task")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()

        frame = ttk.Frame(popup, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)


        label = ttk.Label(frame, text="Enter task number to remove:")
        label.pack(anchor=tk.W)
        entry = ttk.Entry(frame)
        entry.pack(fill=tk.X, pady=(5, 20))


        done_btn = ttk.Button(
            frame,
            text="Enter",
            command=popup.destroy
        )
        done_btn.pack()

    def create_restore_task_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Restore Task")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()


        frame = ttk.Frame(popup, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)


        label = ttk.Label(frame, text="Enter task number to restore:")
        label.pack(anchor=tk.W)
        entry = ttk.Entry(frame)
        entry.pack(fill=tk.X, pady=(5, 20))


        done_btn = ttk.Button(
            frame,
            text="Enter",
            command=popup.destroy
        )
        done_btn.pack()

    def create_clear_trash_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Clear Trash")
        popup.geometry("400x150")
        popup.transient(self.root)
        popup.grab_set()

   
        frame = ttk.Frame(popup, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)


        warning_label = ttk.Label(
            frame,
            text="Are you sure you want to permanently delete all items in trash?",
            wraplength=350
        )
        warning_label.pack(pady=(0, 20))


        button_frame = ttk.Frame(frame)
        button_frame.pack()


        yes_btn = ttk.Button(
            button_frame,
            text="Yes: Permanently Delete All Trash",
            style="Red.TButton"
        )
        yes_btn.pack(side=tk.LEFT, padx=5)


        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

        style = ttk.Style()
        style.configure("Red.TButton", foreground="red")

    def create_welcome_page(self):
        self.cancel_updates()
        for widget in self.root.winfo_children():
            widget.destroy()

        welcome_frame = ttk.Frame(self.root, padding="20")
        welcome_frame.place(relx=0.5, rely=0.4, anchor="center")

        welcome_label = ttk.Label(
            welcome_frame,
            text="Task Manager: Add and Manage Tasks to Aid Productivity",
            font=("Arial", 16)
        )
        welcome_label.pack(pady=20)

        continue_btn = ttk.Button(
            welcome_frame,
            text="Continue",
            command=self.create_main_page
        )
        continue_btn.pack()

    def update_task_list(self, text_widget):

        with open("ToDo.txt", "r") as f:
            content = f.read()
            text_widget.config(state='normal')
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state='disabled')
            self.task_update_id = self.root.after(1000, lambda: self.update_task_list(text_widget))


    def update_trash_list(self, text_widget):

        with open("Trash.txt", "r") as f:
            content = f.read()
            text_widget.config(state='normal')
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state='disabled')
            self.trash_update_id = self.root.after(1000, lambda: self.update_trash_list(text_widget))


    def create_main_page(self):
        self.cancel_updates()

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        option_buttons = [
            ("Add Task", self.create_add_task_popup),
            ("Remove Task", self.create_remove_task_popup),
            ("Change Task Order", self.create_change_order_popup),
            ("View Trash", self.view_trash)
        ]
        
        for button_text, command in option_buttons:
            button = ttk.Button(
                options_frame,
                text=button_text,
                width=20,
                command=command
            )
            button.pack(pady=5)

        ttk.Separator(options_frame, orient='horizontal').pack(fill='x', pady=15)
        help_btn = ttk.Button(
            options_frame,
            text="Help",
            width=20,
            command=self.create_help_page
        )
        help_btn.pack(side=tk.BOTTOM, pady=5)

        task_frame = ttk.Frame(main_frame, padding="10")
        task_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        todo_label = ttk.Label(
            task_frame,
            text="To-Do List",
            font=("Arial", 12, "bold")
        )
        todo_label.pack(anchor=tk.W, pady=(0, 5))

        task_text = tk.Text(
            task_frame,
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=1,
            state='disabled'
        )
        task_scrollbar = ttk.Scrollbar(task_frame, orient="vertical", command=task_text.yview)
        task_text.configure(yscrollcommand=task_scrollbar.set)
        
        task_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_task_list(task_text)

    def create_help_page(self):
        self.cancel_updates()

        for widget in self.root.winfo_children():
            widget.destroy()

        help_frame = ttk.Frame(self.root, padding="20")
        help_frame.pack(fill=tk.BOTH, expand=True)

        help_title = ttk.Label(
            help_frame,
            text="Task Manager Help Guide",
            font=("Arial", 16, "bold")
        )
        help_title.pack(pady=(0, 20))

        help_text = """
Main Page Options:
• Add Task: Allows you to create a new task with a title and optional priority level.
• Remove Task: Moves the selected task to the trash bin for potential recovery or deletion.
• Change Task Order: Enables reordering of tasks based on priority level
• View Trash: Opens the trash page where removed tasks are stored.

Trash Page Options:
• Restore Task: Moves the selected task back to the main To-Do list.
• Clear Trash: Permanently deletes all tasks in the trash.
• Done: Returns to the main To-Do list page.

Additional Features:
• Tasks can be prioritized and organized according to priority
• Removed tasks can be recovered from the trash if needed
• The program maintains a clean and efficient interface for easy task management
• Contents are saved to text files to prevent information loss on window closure
"""

        text_frame = ttk.Frame(help_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=10,
            pady=10,
            height=15
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget.insert(tk.END, help_text)
        text_widget.configure(state='disabled')

        back_btn = ttk.Button(
            help_frame,
            text="Back",
            command=self.create_main_page,
            width=20
        )
        back_btn.pack(pady=20)

    def view_trash(self):
        self.cancel_updates()

        for widget in self.root.winfo_children():
            widget.destroy()

        trash_frame = ttk.Frame(self.root, padding="10")
        trash_frame.pack(fill=tk.BOTH, expand=True)

        options_frame = ttk.LabelFrame(trash_frame, text="Options", padding="10")
        options_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))


        trash_buttons = [
            ("Restore Task", self.create_restore_task_popup),
            ("Clear Trash", self.create_clear_trash_popup)
        ]
        
        for button_text, command in trash_buttons:
            button = ttk.Button(
                options_frame,
                text=button_text,
                width=20,
                command=command
            )
            button.pack(pady=5)

        ttk.Separator(options_frame, orient='horizontal').pack(fill='x', pady=15)
        done_btn = ttk.Button(
            options_frame,
            text="Done",
            width=20,
            command=self.create_main_page
        )
        done_btn.pack(side=tk.BOTTOM, pady=5)

        trash_list_frame = ttk.Frame(trash_frame, padding="10")
        trash_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        trash_label = ttk.Label(
            trash_list_frame,
            text="Trash",
            font=("Arial", 12, "bold")
        )
        trash_label.pack(anchor=tk.W, pady=(0, 5))

        trash_text = tk.Text(
            trash_list_frame,
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=1,
            state='disabled'
        )
        trash_scrollbar = ttk.Scrollbar(trash_list_frame, orient="vertical", command=trash_text.yview)
        trash_text.configure(yscrollcommand=trash_scrollbar.set)
        
        trash_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        trash_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.update_trash_list(trash_text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoApp()
    app.run()



    ###############