import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from datetime import datetime, timedelta
import ephem

# Define latitude and longitude
observer = ephem.Observer()
observer.lat = '34.7444'
observer.long = '-111.4222'  

# Compute the 12-degree twilights for the next two days
today = ephem.now()
twilight_12_deg_morning = observer.next_rising(ephem.Sun(), use_center=True)
twilight_12_deg_evening = observer.next_setting(ephem.Sun(), use_center=True)

# Calculate the time duration between the twilights
duration = twilight_12_deg_morning - twilight_12_deg_evening

# Convert the duration to hours, minutes, and seconds
hours, remainder = divmod(duration * 24 * 3600, 3600)
minutes, seconds = divmod(remainder, 60)
duration = f"{int(hours)} h {int(minutes)} m {int(seconds)} s"

class BaseTimer:
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

        self.reason_label = tk.Label(root, text="", font=("Helvetica", 12), justify=tk.CENTER)
        self.reason_label.grid(row=0, column=4, padx=0, pady=0)

    def create(self, row_index):
        self.label = tk.Label(self.root, text=f"{self.name}: No time lost", font=("Helvetica", 24))
        self.label.grid(row=row_index, column=0, columnspan=1, padx=0, pady=0)

        self.start_button = tk.Button(self.root, text="Start Event", command=self.start_timer, bg="green", fg="white")
        self.stop_button = tk.Button(self.root, text="Stop Event", command=self.stop_timer, bg="red", fg="white")
        self.log_button = tk.Button(self.root, text="Log Event", command=self.log_time)

        self.start_button.grid(row=row_index, column=2, padx=5, pady=0)
        self.stop_button.grid(row=row_index, column=3, padx=5, pady=0)
        self.log_button.grid(row=row_index, column=5, padx=5, pady=0)


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

            # Format the elapsed_time_str to display in HH:MM:SS.SS format
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = elapsed_time.microseconds // 10000  # Two decimal places for milliseconds

            elapsed_time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:02d}"

            total_elapsed_time = sum(timer.elapsed_time.total_seconds() for timer in self.main_timer.timers) + elapsed_time.total_seconds()
            total_elapsed_time_str = str(timedelta(seconds=total_elapsed_time)).split()[-1]

            self.label.config(text=total_elapsed_time_str)
    
            # Example placeholders - replace these with actual logic
            available_time = 12.0  # Total available time for observing in hours
            used_time = 10.0       # Time used for observing in hours

            # Define a list to store total elapsed times for each category
            total_elapsed_times = ['','','','','']

            # Calculate elapsed time for each timer category
            weather_elapsed_time = "TBD"
            technical_elapsed_time = "TBD"
            observer_elapsed_time = "TBD"
            staff_elapsed_time = "TBD"
            other_elapsed_time = "TBD"

            if self.name == 'Weather':
                weather_elapsed_time = elapsed_time_str
                total_elapsed_times[0] = elapsed_time_str
            elif self.name == 'Technical':
                technical_elapsed_time = elapsed_time_str                
                total_elapsed_times[1] = elapsed_time_str
            elif self.name == 'Observer':
                observer_elapsed_time = elapsed_time_str
                total_elapsed_times[2] = elapsed_time_str
            elif self.name == 'Staff':
                staff_elapsed_time = elapsed_time_str
                total_elapsed_times[3] = elapsed_time_str
            elif self.name == 'Other':
                other_elapsed_time = elapsed_time_str
                total_elapsed_times[4] = elapsed_time_str

            reason_label_text = f"------------------------------------------------------------\n" \
                    f"Observing efficiency: {int(used_time/available_time *100)} % \n" \
                    f"Time used for observing:  {used_time} \n" \
                    f"Nominal time available for observing: {duration} \n" \
                    f"------------------------------------------------------------\n" \
                    f"Effective Time Lost:   {elapsed_time_str}s\n" \
                    f"Weather: {weather_elapsed_time}s\n" \
                    f"Technical: {technical_elapsed_time}s\n" \
                    f"Observer: {observer_elapsed_time}s\n" \
                    f"Staff: {staff_elapsed_time}s\n" \
                    f"Other: {other_elapsed_time}s\n" \
                    f'------------------------------------------------------------'

            self.root.after(100, self.update_timer)
            self.reason_label.config(text=reason_label_text)

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

class WeatherTimer(BaseTimer):
    def __init__(self, root, main_timer, reason_combobox):
        super().__init__(root, "Weather", main_timer, reason_combobox)

class TechnicalTimer(BaseTimer):
    def __init__(self, root, main_timer, reason_combobox):
        super().__init__(root, "Technical", main_timer, reason_combobox)

class ObserverTimer(BaseTimer):
    def __init__(self, root, main_timer, reason_combobox):
        super().__init__(root, "Observer", main_timer, reason_combobox)

class StaffTimer(BaseTimer):
    def __init__(self, root, main_timer, reason_combobox):
        super().__init__(root, "Staff", main_timer, reason_combobox)

class OtherTimer(BaseTimer):
    def __init__(self, root, main_timer, reason_combobox):
        super().__init__(root, "Other", main_timer, reason_combobox)

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Observing Time Lost Timer")

        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.log = []

        # Main timer
        self.label = tk.Label(root, text="TBD", font=("Helvetica", 48))
        self.label.grid(row=0, column=0, columnspan=3, padx=20, pady=75)

        self.timers = []
        # Dropdown menu
        self.reason_combobox0 = ttk.Combobox(root, values=['Weather1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])
        self.reason_combobox1 = ttk.Combobox(root, values=['Technical1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])
        self.reason_combobox2 = ttk.Combobox(root, values=['Observer1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])
        self.reason_combobox3 = ttk.Combobox(root, values=['Staff1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])
        self.reason_combobox4 = ttk.Combobox(root, values=['Other1', 'Reason2', 'Reason3', 'ReasonN-1', 'ReasonN'])

        self.reason_combobox0.grid(row=3, column=4, padx=82, pady=0)
        self.reason_combobox1.grid(row=4, column=4, padx=82, pady=0)
        self.reason_combobox2.grid(row=5, column=4, padx=82, pady=0)
        self.reason_combobox3.grid(row=6, column=4, padx=82, pady=0)
        self.reason_combobox4.grid(row=7, column=4, padx=82, pady=0)

        self.timers.append(WeatherTimer(root, self, self.reason_combobox0))
        self.timers.append(TechnicalTimer(root, self, self.reason_combobox1))
        self.timers.append(ObserverTimer(root, self, self.reason_combobox2))
        self.timers.append(StaffTimer(root, self, self.reason_combobox3))
        self.timers.append(OtherTimer(root, self, self.reason_combobox4))

        # Menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_help)

        # Timer buttons
        self.log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.log_text.grid(row=2, column=0, columnspan=6, padx=0, pady=0, sticky="nsew")

        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        for i, timer in enumerate(self.timers):
            timer.create(3 + i)


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
