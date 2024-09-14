import os
import time
import schedule
import threading
import customtkinter as ctk

def validate_entry(entry):
    if entry == '':
        return True
    if entry.isdigit():
        if int(entry) > 59:
            return False
        return True
    return False

shutdown_task = None
confirm_button = None
cancel_button = None

def close_apps():
    os.system("taskkill /F /FI \"STATUS eq RUNNING\" /FI \"USERNAME eq %USERNAME%\" /T")

def shutdown():
    if os.name == 'nt':
        os.system("shutdown /s /t 1")
    elif os.name == 'posix':
        os.system("sudo shutdown now")

def timer(hours, minutes, seconds):
        global shutdown_task
        
        def update_timer_display():
            hours_input.delete(0, ctk.END)
            hours_input.insert(0, f'{hours:02d}')
            minutes_input.delete(0, ctk.END)
            minutes_input.insert(0, f'{minutes:02d}')
            seconds_input.delete(0, ctk.END)
            seconds_input.insert(0, f'{seconds:02d}')
        
        if type(hours) == int and type(minutes) == int and type(seconds) == int:
            app.after(0, update_timer_display)

            if seconds == 0:
                if minutes > 0:
                    minutes = minutes-1
                    seconds = 59
                elif hours > 0:
                    hours = hours-1
                    minutes = 59
                    seconds = 59
            else:
                seconds = seconds-1

            if hours > 0 or minutes > 0 or seconds > 0:
                shutdown_task = app.after(1000, timer, hours, minutes, seconds)
            else:
                shutdown()

            print(f"{hours}:{minutes}:{seconds}")

# def schedule_tasks(hours, minutes, seconds):
#     global shutdown_task
#     time_in_seconds= hours*3600+minutes*60+seconds

#     timer(hours, minutes, seconds)
     
#     shutdown_task = schedule.every(time_in_seconds).seconds.do(close_apps).do(shutdown)

#     while True:
#         schedule.run_pending()

def start_shutdown():
    try:
        if hours_input.get() == '':
            hours_input.delete(0, ctk.END)
            hours_input.insert(0, 00)
        if minutes_input.get() == '':
            minutes_input.delete(0, ctk.END)
            minutes_input.insert(0, 00)
        if seconds_input.get() == '':
            seconds_input.delete(0, ctk.END)
            seconds_input.insert(0, 00)

        hours = int(hours_input.get())
        minutes = int(minutes_input.get())
        seconds = int(seconds_input.get())
        print(f'{hours}:{minutes}:{seconds}')

        app.after(0, timer, hours, minutes, seconds)
        
        change_buttons(confirmed=True)

        # tasks_thread = threading.Thread(target=timer, args=(hours, minutes, seconds))
        # tasks_thread.start()

    except ValueError:
        message_label.configure(text="Por favor, insira valores válidos para horas, minutos e segundos.")
        
def cancel_shutdown():
    global shutdown_task
    
    app.after_cancel(shutdown_task)
    
    hours_input.delete(0, ctk.END)
    hours_input.insert(0, '')

    minutes_input.delete(0, ctk.END)
    minutes_input.insert(0, '')

    seconds_input.delete(0, ctk.END)
    seconds_input.insert(0, '')
    
    change_buttons(confirmed=False)

def change_buttons(confirmed):
    global confirm_button, cancel_button
     
    if confirmed:
        confirm_button.destroy()
        cancel_button = ctk.CTkButton(app, text="CANCEL", font=base_font, width=70, height=40, command=cancel_shutdown)
        cancel_button.grid(row=3, column=2)
    else:
        cancel_button.destroy()
        confirm_button = ctk.CTkButton(app, text="OK", font=base_font, width=70, height=40, command=start_shutdown)
        confirm_button.grid(row=3, column=2)
    
ctk.set_default_color_theme("dark-blue") 
app = ctk.CTk()
app.title("Time To Sleep")
# title_icon = PhotoImage()
# app.iconphoto(True, title_icon)
app.geometry("600x400")
timer_font = ("Arial", 60)
base_font = ("Arial", 20)
app.grid_columnconfigure((0,1,2,3,4), weight=1)
app.grid_rowconfigure((0,1,2,3,4), weight=1)

validate_command = (app.register(validate_entry), "%P")

text1 = ctk.CTkLabel(app, text="Desligar em:", font=base_font)
text1.grid(row=1, column=2, pady=(20, 10))

timer_frame = ctk.CTkFrame(app)
timer_frame.grid(row=2, column=2, padx=20, pady=10, sticky="ew")
timer_frame.grid_columnconfigure((0,2,4), weight=1)
hours_input = ctk.CTkEntry(timer_frame, width=100, height=90, placeholder_text="00", font=timer_font, justify="center", validate="key", validatecommand=validate_command)
hours_input.grid(row=0, column=0, padx=(5, 10), pady=10)
colon1 = ctk.CTkLabel(timer_frame, text=":", font=base_font)
colon1.grid(row=0, column=1)
minutes_input = ctk.CTkEntry(timer_frame, width=100, height=90, placeholder_text="00", font=timer_font, justify="center", validate="key", validatecommand=validate_command)
minutes_input.grid(row=0, column=2, padx=10, pady=10)
colon2 = ctk.CTkLabel(timer_frame, text=":", font=base_font)
colon2.grid(row=0, column=3)
seconds_input = ctk.CTkEntry(timer_frame, width=100, height=90, placeholder_text="00", font=timer_font, justify="center", validate="key", validatecommand=validate_command)
seconds_input.grid(row=0, column=4, padx=(10, 5), pady=10)

# cancel_button = ctk.CTkButton(app, text="CANCEL", font=base_font, width=70, height=40, command=cancel_shutdown)
# cancel_button.grid(row=3, column=2)

confirm_button = ctk.CTkButton(app, text="OK", font=base_font, width=70, height=40, command=start_shutdown)
confirm_button.grid(row=3, column=2)

message_label = ctk.CTkLabel(app, text="", font=base_font)
message_label.grid(row=4, column=2)

app.mainloop()