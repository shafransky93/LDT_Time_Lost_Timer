import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from datetime import datetime, timedelta

class Timer:
    def __init__(self, root, name, main_timer, reason_combobox):
        self.root = root
        self.name = name
        self.main_timer = main_timer
        self.reason_combobox = reason_combobox

        self.paused = False
        self.paused_time = timedelta()

        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.label = None

    def create(self, row_index):
        self.label = tk.Label(self.root, text=f"{self.name}: No time lost", font=("Helvetica", 24))
        self.label.grid(row=row_index, column=0, columnspan=3, padx=20, pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer, bg="green", fg="white")
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer, bg="red", fg="white")
        self.log_button = tk.Button(self.root, text="Log", command=self.log_time)

        self.start_button.grid(row=row_index, column=3, padx=10, pady=10)
        self.stop_button.grid(row=row_index, column=4, padx=10, pady=10)
        self.log_button.grid(row=row_index, column=5, padx=10, pady=10)

        self.reason_combobox = ttk.Combobox(self.root, values=['Reason1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])
        self.reason_combobox.grid(row=row_index, column=6, padx=10, pady=10)

    def stop_timer(self):
        if self.running:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            selected_reason = self.reason_combobox.get()
            if selected_reason:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          {self.name},  {elapsed_time.total_seconds() / 3600:.0f} hrs {elapsed_time.total_seconds() % 3600 / 60:.0f} min [{selected_reason}]"
            else:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          {self.name},  {elapsed_time.total_seconds() / 3600:.0f} hrs {elapsed_time.total_seconds() % 3600 / 60:.0f} min [None]"

            self.main_timer.log.append(log_entry)
            self.main_timer.log_text.insert(tk.END, log_entry + "\n")

            self.start_time = None
            self.running = False
            self.paused = True
            self.paused_time = elapsed_time

    def start_timer(self):
        if not self.running:
            if self.paused:
                self.start_time = datetime.now() - self.paused_time
                self.paused = False
            else:
                self.start_time = datetime.now()
            self.running = True
            self.update_timer()

    def update_timer(self):
        if self.running:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            elapsed_time_str = str(elapsed_time).split()[-1]

            total_elapsed_time = sum(timer.elapsed_time.total_seconds() for timer in self.main_timer.timers) + elapsed_time.total_seconds()
            total_elapsed_time_str = str(timedelta(seconds=total_elapsed_time)).split()[-1]

            self.label.config(text=total_elapsed_time_str)
            self.root.after(100, self.update_timer)

    def log_time(self):
        if self.start_time is not None:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            selected_reason = self.reason_combobox.get()
            if selected_reason:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          {self.name},  {elapsed_time.total_seconds() / 3600:.0f} hrs {elapsed_time.total_seconds() % 3600 / 60:.0f} min [{selected_reason}]"
            else:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          {self.name},  {elapsed_time.total_seconds() / 3600:.0f} hrs {elapsed_time.total_seconds() % 3600 / 60:.0f} min [None]"
            self.main_timer.log.append(log_entry)
            self.main_timer.log_text.insert(tk.END, log_entry + "\n")

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Observing Time Lost Timer")

        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.log = []

        self.timers = []

        self.reason_combobox = ttk.Combobox(root, values=['Reason1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])

        self.timers.append(Timer(root, "Weather", self, self.reason_combobox))
        self.timers.append(Timer(root, "Technical", self, self.reason_combobox))
        self.timers.append(Timer(root, "Observer", self, self.reason_combobox))
        self.timers.append(Timer(root, "Staff", self, self.reason_combobox))
        self.timers.append(Timer(root, "Other", self, self.reason_combobox))

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_help)

        self.label = tk.Label(root, text="No observing time lost", font=("Helvetica", 48))
        self.label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer, bg="green", fg="white")
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer, bg="red", fg="white")
        self.log_button = tk.Button(root, text="Log", command=self.log_time)

        self.log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.log_text.grid(row=2, column=0, columnspan=4, padx=0, pady=0, sticky="nsew")

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        for i, timer in enumerate(self.timers):
            timer.create(3 + i)

        self.reason_label = tk.Label(root, text="", font=("Helvetica", 12), justify=tk.LEFT)
        self.reason_label.grid(row=0, column=4, padx=10, pady=10)

        self.update_reason_label()
        self.root.after(30000, self.update_reason_label)

    def start_timer(self):
        if not self.running:
            self.start_time = datetime.now()
            self.running = True
            self.update_timer()

            for timer in self.timers:
                timer.start_timer()

    def stop_timer(self):
        if self.running:
            current_time = datetime.now()
            self.elapsed_time += current_time - self.start_time
            selected_reason = self.reason_combobox.get()
            if selected_reason:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          Observer,  {self.elapsed_time.total_seconds() / 3600:.0f} hrs {self.elapsed_time.total_seconds() % 3600 / 60:.0f} min [{selected_reason}]"
            else:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          Observer,  {self.elapsed_time.total_seconds() / 3600:.0f} hrs {self.elapsed_time.total_seconds() % 3600 / 60:.0f} min [None]"
            self.log.append(log_entry)
            self.start_time = None
            self.running = False
            self.log_text.insert(tk.END, log_entry + "\n")

    def update_timer(self):
        if self.running:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            elapsed_time_str = str(elapsed_time).split()[-1]

            total_elapsed_time = sum(timer.elapsed_time.total_seconds() for timer in self.timers) + elapsed_time.total_seconds()
            total_elapsed_time_str = str(timedelta(seconds=total_elapsed_time)).split()[-1]

            self.label.config(text=total_elapsed_time_str)
            self.root.after(100, self.update_timer)

    def log_time(self):
        if self.start_time is not None:
            current_time = datetime.now()
            elapsed_time = self.elapsed_time + (current_time - self.start_time)
            selected_reason = self.reason_combobox.get()
            if selected_reason:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          Observer,  {elapsed_time.total_seconds() / 3600:.0f} hrs {elapsed_time.total_seconds() % 3600 / 60:.0f} min [{selected_reason}]"
            else:
                log_entry = f"{current_time.strftime('%H:%M')}    TimeLost          Observer,  {elapsed_time.total_seconds() / 3600:.0f} hrs {elapsed_time.total_seconds() % 3600 / 60:.0f} min [None]"
            self.log.append(log_entry)
            self.log_text.insert(tk.END, log_entry + "\n")

    def update_reason_label(self):
        total_elapsed_time = sum(timer.elapsed_time.total_seconds() for timer in self.timers)
        weather_elapsed_time = self.timers[0].elapsed_time.total_seconds()
        technical_elapsed_time = self.timers[1].elapsed_time.total_seconds()
        observer_elapsed_time = self.timers[2].elapsed_time.total_seconds()
        staff_elapsed_time = self.timers[3].elapsed_time.total_seconds()
        other_elapsed_time = self.timers[4].elapsed_time.total_seconds()

        reason_label_text = f"---------------------------------------\n" \
                            f"Observing efficiency: (used_time/available_time) \n" \
                            f"Time used for observing:  (used_time) \n" \
                            f"Nominal time available for observing: (available_time) \n" \
                            f"---------------------------------------\n" \
                            f"Effective Time Lost: {total_elapsed_time / 3600:.0f} hrs {total_elapsed_time % 3600 / 60:.0f} min\n" \
                            f"Weather: {weather_elapsed_time / 3600:.0f} hrs {weather_elapsed_time % 3600 / 60:.0f} min\n" \
                            f"Technical: {technical_elapsed_time / 3600:.0f} hrs {technical_elapsed_time % 3600 / 60:.0f} min\n" \
                            f"Observer: {observer_elapsed_time / 3600:.0f} hrs {observer_elapsed_time % 3600 / 60:.0f} min\n" \
                            f"Staff: {staff_elapsed_time / 3600:.0f} hrs {staff_elapsed_time % 3600 / 60:.0f} min\n" \
                            f"Other: {other_elapsed_time / 3600:.0f} hrs {other_elapsed_time % 3600 / 60:.0f} min\n" \
                            f'---------------------------------------'

        self.reason_label.config(text=reason_label_text)
        self.root.after(30000, self.update_reason_label)

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
