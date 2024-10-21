import tkinter as tk
from tkinter import font
from datetime import datetime
import random
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import pysine

background = 'black'
window = tk.Tk()
window.title("Latency Test")
window.minsize(750, 500)
window.configure(background=background)

def title():
    title_label = tk.Label(window, text="Welcome to the Alarm Sound Trials!")
    title_label.config(font=("Times", 35, "bold"), background='black', fg='#69a8c9')

    Dscrp = tk.Label(window, text="In the boxes below, please input your full name and age")
    Dscrp.config(font=("Times", 20), background='black', fg='white', pady=10)

    box1_label = tk.Label(window, text="Full Name:")
    box1_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)

    name_entry = tk.Entry(window, font=("Arial", 14))

    box2_label = tk.Label(window, text="Age:")
    box2_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)

    age_entry = tk.Entry(window, font=("Arial", 14))

    txt = tk.Label(window, text="Click [CONTINUE] to proceed, or [EXIT] to quit")
    txt.config(font=("Times", 20), background='black', fg='white', pady=20)

    b1 = tk.Button(window, text="CONTINUE", font=('Times', 20, 'bold'), fg='blue', command=lambda: instructions(name_entry.get(), age_entry.get()))

    b3 = tk.Button(window, text='EXIT', font=('Times', 20, 'bold'), fg='red', command=window.destroy)

    title_label.pack()
    Dscrp.pack()
    box1_label.place(x=40, y=100)
    name_entry.place(x=40, y=150)
    box2_label.place(x=40, y=200)
    age_entry.place(x=40, y=250)
    txt.place(x=170, y=300)
    b1.place(x=200, y=360)
    b3.place(x=450, y=360)

    window.mainloop()





def play_alarm(alarm_name):
    if alarm_name == 'provided':
        alarm = AudioSegment.from_wav("alarm.wav")
        play(alarm)
    else:
        #i just made this up but we can add more
        pysine.sine(frequency=1000.0, duration=0.2)
        pysine.sine(frequency=500.0, duration=0.2)
        pysine.sine(frequency=1000.0, duration=0.2)
        pysine.sine(frequency=500.0, duration=0.2)
    
def instructions(name_text, age_text):
    for widget in window.winfo_children():
        widget.destroy()

    alert = tk.Label(window, text="READ CAREFULLY")
    alert.config(font=("Times", 35, "bold"), background='black', fg='red')
    
    Dscrp = tk.Label(window, text='You will hear two alarm sounds in order.\n\nEach sound will be played at a random time between 1 to 2 minutes \nfrom the moment you press [READY] or from the end of the first sound\n\nYou will then vote which sound startled you the most\n\n\nPress [READY] to begin')
    Dscrp.config(font=("Times", 20), background='black', fg='white', pady=10)

    b1 = tk.Button(window, text="READY", font=('Times', 40, 'bold'), pady=30, padx=40, fg='green', command=trial)

    alert.pack()
    Dscrp.pack()
    b1.pack()

def trial():
    for widget in window.winfo_children():
        widget.destroy()


title()
