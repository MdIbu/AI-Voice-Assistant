from tkinter import *
import random
import time
import datetime
import pyttsx3
import wikipedia
import speech_recognition as sr
from threading import Thread
import requests
import webbrowser
from urllib.request import urlopen
import os 
import pyautogui
import wolframalpha
from bs4 import BeautifulSoup 


def shut_down():
    p1=Thread(target=speak,args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()

def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in frames:
            if flag == False:
                canvas.create_image(0, 0, image=img1, anchor=NW)
                canvas.update()
                flag = True
                return
            else:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)
        
def news():
    """
    This method will tells top 15 current NEWS
    :return: list / bool
    """
    try:
        news_url = "https://news.google.com/news/rss"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup_page = BeautifulSoup(xml_page, "xml")
        news_list = soup_page.findAll("item")
        li = []
        for news in news_list[:5]:
            li.append(str(news.title.text.encode('utf-8'))[1:])
        return li
    except Exception as e:
        print(e)
        return False

def web_scraping(qs):
    global flag2
    global loading

    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.findAll("a")
    all_links = []
    for link in links:
       link_href = link.get('href')
       if "url?q=" in link_href and not "webcache" in link_href:
           all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))
           

    flag= False
    for link in all_links:
       if 'https://en.wikipedia.org/wiki/' in link:
           wiki = link
           flag = True
           break

    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
    elif len(div3)!=0:
        answer = div3[1].text
    elif flag==True:
       page2 = requests.get(wiki)
       soup = BeautifulSoup(page2.text, 'html.parser')
       title = soup.select("#firstHeading")[0].text
       
       paragraphs = soup.select("p")
       for para in paragraphs:
           if bool(para.text.strip()):
               answer = title + "\n" + para.text
               break
    else:
        answer = "Sorry. I could not find the desired results"
    return answer


def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag=False


def temptakecommand():
    global flag20
    global flag2
    global canvas2 
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")
    flag = True
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...") 
        print("Listening...")
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source,phrase_time_limit=5) 
    try:
        speak("I am Recognizing... ")
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"You said: {query}\n")
        query = query.lower()
     
    except Exception as e:
        print(e)
        speak("Say that again please")
        return "None"
        temptakecommand()
    return query


def wa(input):
    app_id = "9HRE5G-Y4V6Q43P6K"
    client = wolframalpha.Client(app_id)
    indx = input.lower().split().index('calculate')
    query = input.split()[indx + 1:]
    res = client.query(' '.join(query))
    try:
        wa_result = next(res.results).text
        output = wa_result
    except Exception as e:
        output = "No results"
    return output

def wa2(input):
    app_id = "9HRE5G-Y4V6Q43P6K"
    client = wolframalpha.Client(app_id)
    indx = input.lower().split().index('is')
    query = input.split()[indx + 1:]
    res = client.query(' '.join(query))
    try:
        wa_result = next(res.results).text
        output = wa_result
    except Exception as e:
        output = "No results"
    return output

def noteinput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...") 
        print("Listening...")
        r.adjust_for_ambient_noise(source) 
        audio = r.listen(source,phrase_time_limit=5) 
    try:
        speak("I am Recognizing... ")
        print("Recognizing...")
        note = r.recognize_google(audio)
        print(f"You said: {note}\n")
        note = note.lower()
     
    except Exception as e:
        print(e)
        speak("Say that again please")
        return "None"
        noteinput()
    return note

def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning... How may i help you?"
    elif 12 <= hour < 18:
        text = "Good Afternoon... How may i help you?"
    else:
        text = "Good Evening... How may i help you?"

    canvas2.create_text(10,10,anchor =NW , text=text,font=('Candara Light', -25,'bold italic'), fill="white",width=350)
    p1=Thread(target=speak,args=(text,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def getweather(city_name):
    api_key = "038ba22ab190db58ec1fa9acac5123a7"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = str(base_url) + "appid=" + str(api_key) + "&q=" + str(city_name)
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404": 
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        answer=("Temperature:"+ str(int(current_temperature - 272.15) )+"Degrees"+"\nAtmospheric pressure:"+ str(current_pressure)+"HPA" +
        "\nHumidity:" + str(current_humidiy) +"%"
        "\nDescription:"+ str(weather_description))

        print(" Current Temperature is " +
        str(int(current_temperature - 272.15) ) + "Degree Centigrades" +
        "\n atmospheric pressure is " +
        str(current_pressure) +"HPA" +
        "\n humidity is " +
        str(current_humidiy) + "percent"
        "\n description is " +
        str(weather_description))
        return answer
    else:
        answer = (" City Not Found!!!")
    return


def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")

    speak("I am listening.")
    flag= True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 3
        audio = r.listen(source,phrase_time_limit=5)

    try:
        print("Recognizing..")
        speak("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        query=query.lower()
        print(f"You Said :{query}\n")
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=query, font=('fixedsys', -30),fill="white", width=350)
        

    except Exception as e:
        print(e)
        speak("Say that again please")
        takecommand()

def main_window():
    global query
    global flag2
    wishme() 
    while True:
        if query != None:
            if 'shutdown ' in query or 'quit ' in query or 'stop ' in query or 'goodbye ' in query:
                shut_down()

            elif 'wikipedia' in query:
                speak('searching wikipedia...')
                query = query.replace("wikipedia","")
                answer = wikipedia.summary(query, sentences= 1)
                print(answer)

            elif 'open youtube' in query:
                print("OK opening youtube...")
                answer=("Opening youtube...")
                webbrowser.open("www.youtube.com")
 
            elif 'open chrome' in query or 'chrome' in query or 'google chrome' in query:
                answer=("opening Chrome...")
                webbrowser.open("www.google.com")
 
            elif 'who are you' in query: 
                answer=("I am IntellIbu the Intelligent Personal Assistant... I can search the web, calculate sums, open applications etcetra...")
 
            elif 'hai ' in query or 'hello ' in query or 'hay ' in query or 'hi ' in query:
                nouns = ("Hi!", "Hey!","What's up?","Hey you!","Hey there!","Hey buddy!")
                num = random.randrange(0,5)
                answer=nouns[num]

            elif 'open yahoo' in query or 'yahoo' in query:
                answer = ("opening yahoo...")
                webbrowser.open("www.yahoo.com") 

            elif "tell me news" in query or "show news" in query:
                news_result = news()
                answer=news_result
 
            elif 'open gmail' in query or 'gmail' in query or "send mail" in query or "open mail" in query:
                answer = ("opening gmail...")
                webbrowser.open("www.gmail.com") 

            elif "open" in query and ".com" in query:
                input = query
                indx = input.lower().split().index('open')
                query = input.split()[indx + 1:]
                res = ("http://www." + "+".join(query))
                print (res)
                webbrowser.open(res)
                answer=("Opening website")

            elif "wish me" in query:
                wishme()

            elif 'search google' in query or 'google' in query:
                indx = query.split().index('google')
                quer = query.split()[indx + 1:]
                webbrowser.open("https://www.google.com/search?q=" + '+'.join(quer))
                answer = ("searching google...")
 
            elif 'love you' in query:
                answer=("i love you too")

            elif "what is" in query or "who is" in query:
                answer = wa2(query)

            elif "calculate" in query:
                answer = wa(query)

            elif "lock my pc" in query or "lock mode" in query:
                os.system("rundll32.exe user32.dll,LockWorkStation")
                answer = ("Locking PC")

            elif "put my laptop in sleep mode" in query or "sleep mode" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                answer = ("Sleep Mode")

            elif "minimise window" in query or "minimize window" in query:
                os.system('''powershell -command "(new-object -com shell.application).minimizeall()"''')
                answer = ("Minimizing window")


            elif "task view" in query:
                pyautogui.keyDown("win")
                pyautogui.press("tab")
                pyautogui.keyUp("win")
                answer = ("Taskview")

            elif "close current window" in query:
                pyautogui.keyDown("alt")
                pyautogui.press("f4")
                pyautogui.keyUp("alt")
                answer = ("closing")

            elif "show start menu" in query or "start menu" in query:
                pyautogui.press("win")
                answer = ("Start Menu")

            elif "take screenshot" in query:
                pyautogui.screenshot('screenshot.png')
                answer=("taking screenshot...")

            elif "press enter" in query:
                pyautogui.press("enter") 
                answer = ("Enter")

            elif "how are you" in query:
                answer = ("I am fine, Hope... you too good")


            elif "what time is it" in query or "time please" in query:
                answer=(time.ctime())

            elif "why you came to world" in query:
                answer=("Thanks to ibrahim ajees. further It's a secret")

 
            elif 'empty recycle bin' in query:
                winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                answer=("Recycle Bin Recycled")

            elif "write a note" in query or "take a note" in query:
                speak("What should i write")
                notes = noteinput()
                file = open('intellibu.txt', 'w')
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(notes)
                file.close()
                answer = ("Note saved")
                 
             
            elif "show note" in query:
                speak("Showing Notes")
                file = open("intellibu.txt", "r")
                answer=file.readline()
                file.close()

            elif "open explorer" in query:
                pyautogui.keyDown("win")
                pyautogui.press("e")
                pyautogui.keyUp("win")
                answer = ("opening explorer...")
 
            elif "open settings" in query:
                pyautogui.keyDown("win")
                pyautogui.press("i")
                pyautogui.keyUp("win")
                answer = ("opening settings...")

            elif "open run" in query:
                pyautogui.keyDown("win")
                pyautogui.press("r")
                pyautogui.keyUp("win")
                answer = ("opening run...")

            elif "Heath mode" in query or "feeling sick" in query or "feeling ill" in query or "am sick" in query:
                speak("Activating Health mode...")
                os.system('QuestionDiagonosisTkinter.py 1')
                answer=("Closing health mode...")

            elif "open taskmanager" in query or "open task manager" in query:
                pyautogui.hotkey('ctrl', 'shift', 'esc')
                answer = ("opening task manager...")

            elif "check my internet connection" in query or "check internet connection" in query:
                hostname="google.co.in"
                response=os.system("ping -c 1"+hostname)
                if response==0:
                    answer=("I Think Internet is Disconnected")
                else: 
                    answer=("Internet Connection is fine")

            elif "where is" in query:
                query = query.split(" ")
                location = query[2]
                speak("Just A Second , I will show you where " + location + " is.")
                URL = "https://www.google.com/maps/place/" + location + "/&amp;"
                webbrowser.open(URL, new=2)
                answer=("Showing location")

            elif 'tell me weather' in query or 'weather' in query:
                speak('Of Which location?')
                city_name = temptakecommand()
                we_result = getweather(city_name)
                answer = we_result
            

            elif 'close chrome' in query:
                os.system("taskkill /f /im " + "chrome.exe")
                answer=("Closed Chrome Browser")

            else:
                speak("Showing results from the web")
                answer=web_scraping(query)
            canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Candara Light', -25,'bold italic'),fill="white", width=350)
            flag2 = False
            p1=Thread(target=speak,args=(answer,))
            p1.start()
            p2 = Thread(target=transition2)
            p2.start()
            query = None
       

    
def main_window2():
    global question
    global flag2
    query = question
    if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
        shut_down()

    elif 'wikipedia' in query:
        print('searching wikipedia...')
        query = query.replace("wikipedia","")
        answer = wikipedia.summary(query, sentences= 1)
        print(answer)

    elif 'open youtube' in query:
        print("OK opening youtube...")
        answer=("OK opening youtube...")
        webbrowser.open("www.youtube.com")

    elif 'open chrome' in query or 'chrome' in query or 'google chrome' in query:
        print("Opening chrome")
        answer=("opening Chrome...")
        webbrowser.open("www.google.com")

    elif "who are you" in query: 
        answer=("I am IntellIbu the Intelligent Personal Assistant... I can search the web, calculate sums, open applications etcetra...")

    elif 'hai ' in query or 'hello ' in query or 'hay ' in query or 'hi ' in query:
        nouns = ("Hi!", "Hey!","What's up?","Hey you!","Hey there!","Hey buddy!")
        num = random.randrange(0,5)
        answer=nouns[num]

    elif 'open yahoo' in query or 'yahoo' in query:
        print("opening yahoo")
        answer = ("Opening yahoo...")
        webbrowser.open("www.yahoo.com") 


    elif 'open gmail' in query or 'gmail' in query or "send mail" in query or "open mail" in query :
        print("Opening gmail")
        answer = ("Opening gmail...")
        webbrowser.open("www.gmail.com") 

    elif "open" in query and ".com" in query:
        input = query
        indx = input.lower().split().index('open')
        query = input.split()[indx + 1:]
        res = ("http://www." + "+".join(query))
        print (res)
        webbrowser.open(res)
        answer=("Opening website")

    elif "tell me news" in query or "show news" in query:
        news_result = news()
        answer=news_result

    elif "wish me" in query:
        wishme()
        answer=" "
 

    elif 'search google' in query or 'google'in query:
        indx = query.split().index('google')
        quer = query.split()[indx + 1:]
        webbrowser.open("https://www.google.com/search?q=" + '+'.join(quer))
        answer = ("searching google...")

    elif 'love you' in query:
        answer=("i love you too")


    elif "what is" in query or "who is" in query:
        answer = wa2(query)

    elif "calculate" in query:
        answer = wa(query)

    elif "lock my pc" in query or "lock mode" in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        answer = ("Locking PC")

    elif "put my laptop in sleep mode" in query or "sleep mode" in query:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        answer = ("Sleep Mode")

    elif "minimise window" in query or "minimize window" in query:
        os.system('''powershell -command "(new-object -com shell.application).minimizeall()"''')
        answer = ("Minimizing window")

    elif "task view" in query :
        pyautogui.keyDown("win")
        pyautogui.press("tab")
        pyautogui.keyUp("win")
        answer = ("Taskview")
    
    elif "close current window" in query :
        pyautogui.keyDown("alt")
        pyautogui.press("f4")
        pyautogui.keyUp("alt")
        answer = ("closing")

    elif "show start menu" in query or "start menu" in query :
        pyautogui.press("win")
        answer = ("Start Menu")

    elif "take screenshot" in query :
        pyautogui.screenshot('screenshot.png')
        answer=("taking screenshot...")

    elif "press enter" in query:
        pyautogui.press("enter") 
        answer = ("Enter")

    elif "how are you" in query:
        answer = ("I am fine, Hope... you too good")


    elif "why you came to world" in query:
        answer=("Thanks to ibrahim ajees. further It's a secret")

    elif "what time is it" in query or "time please" in query:
        answer=(ctime())

    elif 'empty recycle bin' in query:
        winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
        answer=("Recycle Bin Recycled")

    elif "write a note" in query or "take a note" in query:
        speak("What should i write")
        notes = noteinput()
        file = open('intellibu.txt', 'w')
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        file.write(strTime)
        file.write(" :- ")
        file.write(notes)
        answer = ("Note saved")
         
    elif "show note" in query:
        speak("Showing Notes")
        file = open("intellibu.txt", "r")
        answer=file.readline()
        file.close()

    elif "open explorer" in query:
        pyautogui.keyDown("win")
        pyautogui.press("e")
        pyautogui.keyUp("win")
        answer = ("opening explorer...")
 
    elif "open settings" in query:
        pyautogui.keyDown("win")
        pyautogui.press("i")
        pyautogui.keyUp("win")
        answer = ("opening settings...")

    elif "open run" in query:
        pyautogui.keyDown("win")
        pyautogui.press("r")
        pyautogui.keyUp("win")
        answer = ("opening run...")

    elif "Heath mode" in query or "feeling sick" in query or "feeling ill" in query or "am sick" in query:
        speak("Activating Health mode...")
        os.system('QuestionDiagonosisTkinter.py 1')
        answer=("Closing health mode...")

    elif "open taskmanager" in query or "open task manager" in query:
        pyautogui.hotkey('ctrl', 'shift', 'esc')
        answer = ("opening task manager...")


    elif "check my internet connection"in query or "check internet connection" in query:
        hostname="google.co.in"
        response=os.system("ping -c 1"+hostname)
        if response==0:
            answer=("I Think Internet is Disconnected")
        else:
            answer=("Internet Connection is fine")

    elif "where is" in query:
        query = query.split(" ")
        location = query[2]
        speak("Just A Second , I will show you where " + location + " is.")
        URL = "https://www.google.com/maps/place/" + location + "/&amp;"
        webbrowser.open(URL, new=2)
        answer=("Showing location")

    elif 'tell me weather' in query or 'weather' in query:
        speak('Of Which location?')
        city_name = temptakecommand()
        we_result = getweather(city_name)
        answer = we_result
        

    elif 'close chrome' in query:
        os.system("taskkill /f /im " + "chrome.exe")
        speak("Closed Chrome Browser")

    else:
        speak("Showing results from the web")
        answer=web_scraping(query)
        
    canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Candara Light', -25,'bold italic'),fill="white", width=350)
    flag2 = False
    p1=Thread(target=speak,args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    query = None
    

if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True

    engine = pyttsx3.init() # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)

    root=Tk()
    root.title("Intellibu")
    root.geometry('1360x720+-5+0')
    root.configure(background='white')
    root.iconbitmap('ilogo.ico')

    img1= PhotoImage(file='chatbot-image.png')
    img2= PhotoImage(file='button-green.png')
    img4= PhotoImage(file='terminal.png')
    img5= PhotoImage(file='rearrow.png')
    background_image=PhotoImage(file="last.png")

    f = Frame(root,width = 1360, height = 720)
    f.place(x=0,y=0)
    f.tkraise()
    front_image = PhotoImage(file="front2.png")
    okVar = IntVar()
    btnOK = Button(f, image=front_image,command=lambda: okVar.set(1))
    btnOK.place(x=0,y=0)
    speak("Click and wait")
    f.wait_variable(okVar)
    f.destroy()    

    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0)

    frames = [PhotoImage(file='chatgif.gif',format = 'gif -index %i' %(i)) for i in range(20)]
    canvas = Canvas(root, width = 800, height = 596)
    canvas.place(x=10,y=10)
    canvas.create_image(0, 0, image=img1, anchor=NW)
    question_button = Button(root,image=img2, bd=0, command=takecommand)
    question_button.place(x=200,y=635)
    variable1=StringVar() # Value saved here
    def search():
        flag2 =False
        global question
        question = (variable1.get())
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=question, 
        font=('Times new roman', -30),fill="white", width=350)
        p2 = Thread(target=transition2)
        p2.start()
        main_window2()
        return ''
    entry=Entry(root, width=17,bg="#00a86b",fg="white",font=("Times new roman",20),textvariable=variable1).place(x=800,y=655)
    label=Label(root,bg="white",font=("Times new roman",15),text="what do you want me to do?").place(x=800,y=620)
    entry_button = Button(root,image=img5, bd=0, command=search).place(x=1050,y=655)


    frame=Frame(root,width=500,height=596)
    frame.place(x=825,y=10)
    canvas2=Canvas(frame,bg='#FFFFFF',width=500,height=596,scrollregion=(0,0,500,900))
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas2.yview)
    canvas2.config(width=500,height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT,expand=True,fill=BOTH)
    canvas2.create_image(0,0, image=img4, anchor="nw")

    task = Thread(target=main_window)
    task.start()
    root.mainloop()
