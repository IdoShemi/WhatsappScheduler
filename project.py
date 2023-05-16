import tkinter as tk
import pywhatkit as kit
from tkinter import ttk
import pyautogui
import time
import datetime

class DateHandler: 
    def getDate(hour=0, minute=0, month=0, day=0): 
        #this function validates the time difference in seconds
        time_diff = 0
        if day == 0: 
            day, month = datetime.datetime.now().day, datetime.datetime.now().month
        if minute != -1:  # message is not instantly
            currentyear = datetime.datetime.now().year
            if(hour >= 0  and hour <=23 and day >=1 and day <=31):
                send_time = datetime.datetime(currentyear, month, day, hour, minute, 0)
                time_diff = (send_time - datetime.datetime.now()).total_seconds() 
            else: #date not valid, I know the error will be date passed it's ok
                time_diff = -1                    
        return time_diff
        

class WhatsappSender: 
    def wrapper(func): 
        def innerFunc(phonenumber, messagetext, hour=0, minute=0, month=0, day=0): 
            #checking date before sending message and then print error if exist
            time_diff = DateHandler.getDate(hour, minute, month, day)
            if(time_diff<0): 
                print("Error: The send time has already passed.")
            else: 
                print(f'send message in {time_diff} seconds')
                func(phonenumber, messagetext, hour, minute, month, day)
        return innerFunc

    @wrapper
    def send_message_scheduled(phonenumber, messagetext, hour=0, minute=0, month=0, day=0): 
        # Calculate the time difference between the current time and the send time using DateHandler class
        time_diff = DateHandler.getDate(hour, minute, month, day)
        # Pause the program for the time difference
        time.sleep(time_diff)

        # Send the message using pywhatkit
        kit.sendwhatmsg_instantly(phonenumber, messagetext)
        start = pyautogui.locateOnScreen('loaction.png')
        pyautogui.moveTo(start)
        pyautogui.leftClick()
        print('message sent succesfully')


def startup(): 
    color = 'cyan'
    root = tk.Tk()
    root.title("Send Message")
    root.configure(bg=color)
    # Set the window size and center it on the screen
    window_width = 400
    window_height = 360
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a style for the labels and textboxes
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))

    # Create the phone number label and entry widget
    phone_label = ttk.Label(root, text="Phone Number:", background=color)
    phone_label.pack(pady=10)
    phone_entry = ttk.Entry(root)
    phone_entry.pack(pady=5, padx=75, fill=tk.X)

    # Create the message label and entry widget
    msg_label = ttk.Label(root, text="Message:", background=color)
    msg_label.pack(pady=10)
    msg_entry = ttk.Entry(root)
    msg_entry.pack(pady=5, padx=75, fill=tk.X)

    # Create the date label and entry widget
    date_label = ttk.Label(root, text="Date:", background=color)
    date_label.pack(pady=10)
    date_entry = ttk.Entry(root)
    date_entry.pack(pady=5, padx=75, fill=tk.X)

    time_label = ttk.Label(root, text="Time:", background=color)
    time_label.pack(pady=10)
    time_entry = ttk.Entry(root)
    time_entry.pack(pady=5, padx=75, fill=tk.X)

    # Define a function to handle button clicks
    def send_message():
        phone_number = phone_entry.get()
        message = msg_entry.get()
        date = date_entry.get().replace("/", ".").split(".")
        if(len(date)< 2): 
            day, month = 0, 0
        else:
            day, month = date[0], date[1]
        
        daytime = time_entry.get().split(":")
        if(len(daytime) != 2): 
            hour, minute  = -1, -1
        else:
            hour, minute  = daytime[0], daytime[1]
        WhatsappSender.send_message_scheduled(phone_number, message, int(hour), int(minute), int(month), int(day))

    # Create the send button
    send_button = ttk.Button(root, text="Send", command=send_message)
    send_button.pack(pady=20)

    # Start the main loop
    root.mainloop()


startup()

