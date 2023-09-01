import tkinter as tk
from tkinter import ttk  # Import ttk for the Combobox
from tkinter import scrolledtext
from tkinter import messagebox
from datetime import datetime, timedelta

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Observing Time Lost Timer")
        
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.log = []

        # Menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_help)

        # Reason tab
        reason_label = tk.Label(root, text="Reason for Closure:")
        reason_label.grid(row=0, column=3, padx=10, pady=10)
        
        self.reason_combobox = ttk.Combobox(root, values=['weather', 'dome', 'mount', 'AOS', 'TCS', 'instrument', 'software', 'network'])
        self.reason_combobox.grid(row=1, column=3, padx=10, pady=10)

        # Labels and buttons
        self.label = tk.Label(root, text="No observing time lost", font=("Helvetica", 48))
        self.label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer, bg="green", fg="white")
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer, bg="red", fg="white")
        self.log_button = tk.Button(root, text="Log", command=self.log_time)

        self.start_button.grid(row=1, column=0, padx=10, pady=10)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)
        self.log_button.grid(row=1, column=2, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.log_text.grid(row=2, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")  # Make it stretch

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

    def start_timer(self):
        if not self.running:
            self.start_time = datetime.now()
            self.running = True
            self.update_timer()

    def stop_timer(self):
        if self.running:
            current_time = datetime.now()
            self.elapsed_time += current_time - self.start_time
            selected_reason = self.reason_combobox.get()
            if selected_reason:
                log_entry = f"Timer start: {self.start_time}, Timer stop: {current_time}, Observing time lost: {self.elapsed_time}, Reason: {selected_reason}"
            else:
                log_entry = f"Timer start: {self.start_time}, Timer stop: {current_time}, Observing time lost: {self.elapsed_time}, Reason: None"
            self.log.append(log_entry)
            self.start_time = None
            self.running = False
            self.log_text.insert(tk.END, log_entry + "\n")

    def update_timer(self):
        if self.running:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            elapsed_time_str = str(elapsed_time).split()[-1]
            self.label.config(text=elapsed_time_str)
            self.root.after(100, self.update_timer)  # Reduced the interval to 100 milliseconds

    def log_time(self):
        if self.start_time is not None:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            selected_reason = self.reason_combobox.get() 

            if selected_reason:
                log_entry = f"Current start: {self.start_time}, Current stop: {current_time}, Observing time lost: {elapsed_time}, Reason: {selected_reason}"
            else:
                log_entry = f"Current start: {self.start_time}, Current stop: {current_time}, Observing time lost: {elapsed_time}, Reason: None"
            
            self.log.append(log_entry)
            self.log_text.insert(tk.END, log_entry + "\n")
            
        else:
            selected_reason = self.reason_combobox.get() 
            if selected_reason:
                current_time_entry = f"Current Time: {datetime.now()}, Observing time lost: {self.elapsed_time}, Reason: {selected_reason}"
            else:
                current_time_entry = f"Current Time: {datetime.now()}, Observing time lost: {self.elapsed_time}, Reason: None"
            self.log_text.insert(tk.END, current_time_entry + "\n")

    def show_help(self):
        help_text = "LDT Observing Time Lost Timer\n\n" \
                    "This application allows you to track time lost during LDT observing runs.\n\n" \
                    "To use the timer, click the 'Start' button when you start closing up, " \
                    "click the 'Stop' button when you begin reopening. You can also log the current time " \
                    "at any time without stopping the timer by clicking the 'Log' button.\n\n" \
                    "The logged times will be displayed in the text box below.\n\n" \
                    "Enjoy your observing run!\n"
        messagebox.showinfo("About", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
