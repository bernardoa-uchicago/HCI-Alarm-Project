import tkinter as tk
import pandas as pd
import random
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from pysinewave import SineWave
import threading
import math


background = 'black'
window = tk.Tk()
window.title("Beep Beep Trials")
window.minsize(750, 500)
window.configure(background=background)
global trial1_array
trial1_array = []
tones_heard_array = []

results_dataframe = pd.DataFrame(columns=["Name","Age","Condition","Neurodivergent","Musician","Frequencies Played","Prefered Frequency","Old Rating","New Rating"])


def title():
    for widget in window.winfo_children():
        widget.destroy()
    title_label = tk.Label(window, text="Welcome to the Beep Beep Trials!")
    title_label.config(font=("Times", 35, "bold"), background='black', fg='#69a8c9')

    Dscrp = tk.Label(window, text="Please fill out the boxes below to the best of your knowledge")
    Dscrp.config(font=("Times", 20), background='black', fg='white', pady=10)

    #name collection 
    box1_label = tk.Label(window, text="Full Name:")
    box1_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    name_entry = tk.Entry(window, font=("Arial", 14))

    #age collection
    box2_label = tk.Label(window, text="Age:")
    box2_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    age_entry = tk.Entry(window, font=("Arial", 14))

    #hearing impairment collection 
    box3_label = tk.Label(window, text="Do you have a hearing-impairing condition (y/n):")
    box3_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    condition_entry = tk.Entry(window, font=("Arial", 14))

    #neurodivergent collection
    box4_label = tk.Label(window, text="Are you neurodivergent (y/n):")
    box4_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    neurodivergent_entry = tk.Entry(window, font=("Arial", 14))

    #muscian collection
    box5_label = tk.Label(window, text="Are you a musician (y/n):")
    box5_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    musician_entry = tk.Entry(window, font=("Arial", 14))

    txt = tk.Label(window, text="Click [CONTINUE] to proceed, or [EXIT] to quit")
    txt.config(font=("Times", 20), background='black', fg='white', pady=20)


    b1 = tk.Button(window, text="CONTINUE", font=('Times', 20, 'bold'), fg='blue', command=lambda: instructions(name_entry.get(), age_entry.get(), condition_entry.get(), neurodivergent_entry.get(), musician_entry.get()))
    b3 = tk.Button(window, text='EXIT', font=('Times', 20, 'bold'), fg='red', command=window.destroy)

    title_label.pack()
    Dscrp.pack()
    box1_label.place(x=40, y=100)
    name_entry.place(x=40, y=150)

    box2_label.place(x=40, y=200)
    age_entry.place(x=40, y=250)

    box3_label.place(x=300, y=100)
    condition_entry.place(x=300, y=150)

    box4_label.place(x=300, y=200)
    neurodivergent_entry.place(x=300, y=250)

    box5_label.place(x=300, y=300)
    musician_entry.place(x=300, y=350)
   
   
    txt.place(x=170, y=400)

    b1.place(x=200, y=450)
    b3.place(x=450, y=450)

    window.mainloop()


def frequency_to_pitch_helper(frequency):
    #the only reason this exists is because the pysinewave library doesnt include an easy way to play one frequency and uses its own pitch unit
    pitch = 12 * math.log2(frequency / 440) + 9
    return pitch

def rate_frequencies_results_helper(tones_heard, option_chosen):
    global trial1_array
    print(f"pitches played: {tones_heard}")
    print(f"option chosen: {option_chosen}")
    if option_chosen == 'A':
        tone_chosen = tones_heard[0]
    elif option_chosen == 'B':
        tone_chosen = tones_heard[1]
    else:
        tone_chosen = 0
        
    trial1_array.append(tuple(tones_heard))
    trial1_array.append(tone_chosen)
    trial1_array.append(0)
    trial1_array.append(0)
    print(trial1_array)
    results_dataframe.loc[len(results_dataframe)] = trial1_array
    trial1_array = trial1_array[:5]

    frequency_intensity_trials('')
    

def rate_frequencies_helper(tones_heard):
    print("\n\nNEXT TRIAL\n\n")
    for widget in window.winfo_children():
        widget.destroy()
    window.update()  
    
    tone_selection_label = tk.Label(window, text=f'Which tone sounded louder?\nA, B, or were they the same volume?', font=("Times", 70), background='black', fg='white', pady=10)

    option_1 = tk.Button(window, text="Tone A", font=('Times', 40, 'bold'), pady=30, padx=40, fg='green', command=lambda: rate_frequencies_results_helper(tones_heard, 'A'))
    option_2 = tk.Button(window, text="Tone B", font=('Times', 40, 'bold'), pady=30, padx=40, fg='green', command=lambda: rate_frequencies_results_helper(tones_heard, 'B'))
    option_3 = tk.Button(window, text="They sounded the same", font=('Times', 40, 'bold'), pady=30, padx=40, fg='green', command=lambda: rate_frequencies_results_helper(tones_heard, 'X'))
    option_4 = tk.Button(window, text="Redo Last Trial", font=('Times', 40, 'bold'), pady=30, padx=40, fg='green', command=lambda:frequency_intensity_trials(tones_heard))
    tone_selection_label.pack()

    option_1.pack()
    option_2.pack()
    option_3.pack()
    option_4.pack()

def frequency_intensity_trials(previous_tones):
    if len(results_dataframe) < 2:
        j = 0
        tones_heard = []
        if previous_tones =='':
            while j < 2: 
                for widget in window.winfo_children():
                    widget.destroy()

                #Display the trial number as a letter for easier distinction
                if j == 0:
                    tone_letter = 'A'
                else: 
                    tone_letter = 'B'

                trial_number_label = tk.Label(window, text=f'Trial: {len(results_dataframe) + 1} of 20', font=("Times", 70), background='black', fg='white', pady=10)
                trial_number_label.pack()

                audio_number_label = tk.Label(window, text=f'Tone: {tone_letter}', font=("Times", 70), background='black', fg='white', pady=10)
                audio_number_label.pack()

                window.update()   

                #actual logic of the pitch selection 
                pitch = round(random.randint(40,12040))
                tones_heard.append(pitch)
                sinewave = SineWave(pitch = frequency_to_pitch_helper(pitch))
                sinewave.play()
                sleep(3)
                sinewave.stop()
                sleep(3)
                j += 1
        else:
            for widget in window.winfo_children():
                    widget.destroy()
            #Display the trial number as a letter for easier distinction
            if j == 0:
                tone_letter = 'A'
            else: 
                tone_letter = 'B'
            trial_number_label = tk.Label(window, text=f'Trial: {len(results_dataframe) + 1} of 20', font=("Times", 70), background='black', fg='white', pady=10)
            trial_number_label.pack()
            audio_number_label = tk.Label(window, text=f'Tone: {tone_letter}', font=("Times", 70), background='black', fg='white', pady=10)
            audio_number_label.pack()

            window.update()   

            #play first previous tone
            sinewave = SineWave(pitch = frequency_to_pitch_helper(previous_tones[0]))
            sinewave.play()
            sleep(3)
            sinewave.stop()
            sleep(3)

            #play second previous tone 
            sinewave = SineWave(pitch = frequency_to_pitch_helper(previous_tones[1]))
            sinewave.play()
            sleep(3)
            sinewave.stop()
            sleep(3)

            tones_heard = previous_tones


        rate_frequencies_helper(tones_heard)

       
    else:
       instructions2()


def generate_sinewave(direction):
    if direction == 'rise':
        sinewave = SineWave(pitch=35, pitch_per_second=50)
        sinewave.set_pitch(55)
    elif direction == 'fall':
        sinewave = SineWave(pitch=55, pitch_per_second=50)
        sinewave.set_pitch(35)
    sinewave.play()  
    sleep(0.7)
    sinewave.stop()
      
def play_alarm(alarm_name):
    #logic to set alarm 
    if alarm_name == 'provided':
        alarm = AudioSegment.from_wav("alarm.wav")
        play(alarm)
        sleep(5)
    elif alarm_name == 'new':
        rising_thread = threading.Thread(target=generate_sinewave, args=('rise', ))
        falling_thread = threading.Thread(target=generate_sinewave, args=('fall', ))

        rising_thread.start()
        falling_thread.start()

        rising_thread.join()
        falling_thread.join()
        sleep(5)

def alarm_randomizer():
    alarm_order = []
    while len(alarm_order) < 2:  
        number = random.randint(1, 2)  
        if number not in alarm_order:  
            alarm_order.append(number) 
    return alarm_order
    
def instructions(name_text, age_text, condition_text, neurodivergent_text, musician_text):
    global trial1_array
    print(trial1_array)
    trial1_array.append(str(name_text))
    trial1_array.append(str(age_text))
    trial1_array.append(str(condition_text))
    trial1_array.append(str(neurodivergent_text))
    trial1_array.append(str(musician_text))
    print(trial1_array)

    for widget in window.winfo_children():
        widget.destroy()

    alert = tk.Label(window, text="READ CAREFULLY")
    alert.config(font=("Times", 35, "bold"), background='black', fg='red')
    
    Dscrp = tk.Label(window, text='You will hear two different tones, 3 seconds apart.\nYour task will be to select the tone sounded louder,\nor "same" if they sounded the same volume\nThe trial will repeat 20 times.\n Press [READY] to begin')
    Dscrp.config(font=("Times", 20), background='black', fg='white', pady=10)

    b1 = tk.Button(window, text="READY", font=('Times', 40, 'bold'), pady=30, padx=40, fg='green', command=lambda: frequency_intensity_trials(''))

    alert.pack()
    Dscrp.pack()
    b1.pack()

def instructions2():
    print(results_dataframe)
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
    window.update()
    order = alarm_randomizer()
    order_copy = order.copy()
    while len(order):
        warn = tk.Label(window, text="IN PROGRESS")
        warn.config(font=("Times", 50, "bold"), background=background, fg='#69a8c9', pady=5)
        warn.place(x=220,y=230)
        window.update()
        sleep(random.randint(5,10))
        if order.pop() == 1:
            print("old")
            play_alarm("provided")
        else:
            print("new")
            play_alarm('new')

    for widget in window.winfo_children():
        widget.destroy()
   
    rating1_label = tk.Label(window, text="Rate the first sound from 1 to 7 on how startling it was.")
    rating1_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    rating1_entry = tk.Entry(window, font=("Arial", 14))

    rating2_label = tk.Label(window, text="Rate the second sound from 1 to 7 on how startling it was.")
    rating2_label.config(font=("Times", 20), background=background, fg='#D3D3D3', pady=5)
    rating2_entry = tk.Entry(window, font=("Arial", 14))

    replay = tk.Button(window, text="RETRY", font=('Times', 20, 'bold'), fg='red', command=trial)
    ret = tk.Button(window, text="Submit Results and Finish Trial", font=('Times', 20, 'bold'), fg='black', command=lambda: save(order_copy, rating1_entry.get(), rating2_entry.get()))

    rating1_label.pack()
    rating1_entry.pack()
    rating2_label.pack()
    rating2_entry.pack()
    replay.pack()
    ret.pack()
    window.update()

def save(order_copy, rating1_entry, rating2_entry):
    print("trial 2: ")
    print(f"order: {order_copy}, alarm1 rating: {rating1_entry}, alarm2 rating: {rating2_entry}\n\n")
    if order_copy.pop() == 1:
        for i in range(len(results_dataframe)-2, len(results_dataframe)):
            results_dataframe.loc[i, "Old Rating"] = rating1_entry
            results_dataframe.loc[i, "New Rating"] = rating2_entry
    else:
        for i in range(len(results_dataframe)-2, len(results_dataframe)):
            results_dataframe.loc[i, "Old Rating"] = rating2_entry
            results_dataframe.loc[i, "New Rating"] = rating1_entry

    results_dataframe.to_csv("results.csv", mode='a', index=True, header=False)
    title()

title()