import os
import time
import schedule
import threading
import customtkinter as ctk

# def timer(hours, minutes, seconds):
#     t=delay_input
#     hour=0
#     minutes=0
#     seconds=0
#     while t > 1:
        
def close_apps():
    os.system("taskkill /F /FI \"STATUS eq RUNNING\" /FI \"USERNAME eq %USERNAME%\" /T")

def shutdown():
    if os.name == 'nt':
        os.system("shutdown /s /t 1")
    elif os.name == 'posix':
        os.system("sudo shutdown now")

ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Time To Sleep")
app.geometry("600x400")
timer_font = ("Arial", 60)
base_font = ("Arial", 20)
app.grid_columnconfigure((0,1,2,3,4), weight=1)
app.grid_rowconfigure((0,1,2,3,4), weight=1)

text1 = ctk.CTkLabel(app, text="Desligar em:", font=base_font)
text1.grid(row=1, column=2, pady=(20, 10))
timer_frame = ctk.CTkFrame(app)
timer_frame.grid(row=2, column=2, padx=20, pady=10, sticky="ew")
timer_frame.grid_columnconfigure((0,2,4), weight=1)
hours_input = ctk.CTkEntry(timer_frame, width=100, height=90, placeholder_text="00", font=timer_font, justify="center")
hours_input.grid(row=0, column=0, padx=(5, 10), pady=10)
colon1 = ctk.CTkLabel(timer_frame, text=":", font=base_font)
colon1.grid(row=0, column=1)
minutes_input = ctk.CTkEntry(timer_frame, width=100, height=90, placeholder_text="00", font=timer_font, justify="center")
minutes_input.grid(row=0, column=2, padx=10, pady=10)
colon2 = ctk.CTkLabel(timer_frame, text=":", font=base_font)
colon2.grid(row=0, column=3)
seconds_input = ctk.CTkEntry(timer_frame, width=100, height=90, placeholder_text="00", font=timer_font, justify="center")
seconds_input.grid(row=0, column=4, padx=(10, 5), pady=10)
confirm_button = ctk.CTkButton(app, text="OK", font=base_font, width=70, height=40)
confirm_button.grid(row=3, column=2)

def schedule_tasks(delay_input):
    schedule.every(delay_input).minutes.do(close_apps).do(shutdown)
    timer=delay_input*60
    while True:
        schedule.run_pending()
        time.sleep(1)
        timer=timer-1
        print(timer)

def schedule_tasks_threads(delay_input):
    schedule_tasks(delay_input)

# tasks_thread = threading.Thread(target=schedule_tasks_threads, args=(delay))
# tasks_thread.start()
app.mainloop()