


import threading
from time import sleep, time
import tkinter as tk 
from tkinter import ttk
from PIL import  Image, ImageTk, ImageEnhance
import os

import serial 
from Errors import Empty, NotNum, NumOfPlayers, Wrong_Input, MaxPlayers, NumberOfPlayers, ColorTaken, TakenNick, MissingCol, nickLen, Confidence, TooManyTags,UnsupportedChar
from screeninfo import get_monitors
import cv2
import re 
from PIL import Image, ImageTk 
import pygame
from ultralytics import YOLO
from arduino_connect import WritoToArduino, findArduinoPort
from test2 import Players, Settings, PlayerSettings,  Widget, WidgetFrame, Paths, Cleaner
from MakeAnReport import create_report
from math import ceil

import sounddevice as sd
import soundfile as sf
######################
### Used Functions ###
######################

        
def Check_NumberOfPlayer():
    input = players_entry.get()
    if input =="":
        Empty()
        return [False, False]
    if input.isnumeric():
        if 1 <= int(input) <= 5:
            newSettings.Set_MaxPlayers(int(input))
            return [True, int(input)]
        else:
            NumOfPlayers()
            return [False, False]
    else:
        NotNum()
        return [False, False]  
def resize_background(width, height):
    resized_image = Image.open(path_to_background_image).resize((width, height), Image.LANCZOS)
    global background_image
    background_image = ImageTk.PhotoImage(resized_image)
    background_image_label.config(image=background_image)
def MonitorSize(num):
    monitors = get_monitors()
    width, height  = [] ,[]
    for monitor in monitors:
        width.append(monitor.width)
        height.append(monitor.width)
    return width[num], height[num]
def Resolutions():
    monitors = get_monitors()
    resolution = []
    id = 0
    for monitor in monitors:
        id +=1
        resolution.append(f"Screen number:{id}, resolution {monitor.width} x {monitor.height}")
    return resolution
def changeResolution():
    str = screen_entry.get()
    pattern = r'(\d+) x (\d+)'
    matches = re.search(pattern, str)
    width = matches.group(1)
    height = matches.group(2)
    try: 
        resize_background(int(width), int(height))
    except:
        Wrong_Input()       
def add_player_nick():
    indx = nick_storage_Entry.size()
    select = nick_storage_Entry.curselection()
    try:
        row = int(select[0])
        clicked_name = nick_storage_Entry.get(row)
    except:
        row = False
    new_name = nick_Entry.get()
    if indx == newSettings.Get_MaxPlayers():
        MaxPlayers(newSettings.Get_MaxPlayers())
        return
    elif new_name == "":
        Wrong_Input()
        return
    elif len(new_name) < 2:
        nickLen()
        return
    elif "_" in new_name:
        UnsupportedChar("_")
        return
    elif row != False and clicked_name[0] == "_": 
        if PlayerSettings.checkForName(new_name) == False:
            founded_tag = ""
            for i in range(len(clicked_name) - 1, -1, -1):
                    if clicked_name[i] == ":":
                        colon_found = True
                        break
            if colon_found:
                founded_tag = clicked_name[i+1 + 1:]
            nick_storage_Entry.delete(nick_storage_Entry.curselection())
            nick_storage_Entry.delete(row)
            nick_storage_Entry.insert(indx, f"{nick_Entry.get()}___Tag: {founded_tag}")
            nick_Entry.delete(0,tk.END) 
    else:
        if PlayerSettings.checkForName(new_name) == False:
            PlayerSettings(nick=new_name)
            print(f"There should be a player with name {nick_Entry.get()}")   
            PlayerSettings.ShowAllPlayers()
            nick_storage_Entry.insert(indx, nick_Entry.get())
            nick_Entry.delete(0,tk.END)   
 
def Delete_player():
    select = nick_storage_Entry.curselection()
    try:
        row = int(select[0])
        clicked_name = nick_storage_Entry.get(row)
        founded_tag = ""
        
        if "_" not in clicked_name:
            #PlayerSettings.ShowAllPlayers()
            PlayerSettings.removeObjBy(val = clicked_name)
            nick_storage_Entry.delete(nick_storage_Entry.curselection())
            print(f"there should be no player with name {clicked_name}")
            PlayerSettings.ShowAllPlayers()
        else:
            for i in range(len(clicked_name) - 1, -1, -1):
                if clicked_name[i] == ":":
                    colon_found = True
                    break
            if colon_found:
                founded_tag = clicked_name[i+1 + 1:]
            #PlayerSettings.ShowAllPlayers()
            PlayerSettings.removeObjBy(val = founded_tag, name=False)
            print(f"there should be no player with tag {founded_tag}")
            PlayerSettings.ShowAllPlayers()
            nick_storage_Entry.delete(nick_storage_Entry.curselection())
        for widget in  Img_widget_container:
            if widget.cget("text") == founded_tag:
                widget.config(state= tk.ACTIVE)
                return
    except:
        pass
    
def Delete_tag():
    select = nick_storage_Entry.curselection()
    try:
        row = int(select[0])
        clicked_name = nick_storage_Entry.get(row)
        founded_tag = ""
        
        if "_" not in clicked_name:
            return
        else:
            for i in range(len(clicked_name) - 1, -1, -1):
                if clicked_name[i] == ":":
                    colon_found = True
                    break
            if colon_found:
                founded_tag = clicked_name[i+1 + 1:]
            founded_Nick = ""
            if clicked_name[0] =="_":
                nick_storage_Entry.delete(row)
                print(f"deleting tag {founded_tag}")
                PlayerSettings.removeObjBy(val=founded_tag, name=False)
                PlayerSettings.ShowAllPlayers()
            else:
                
                for i in range(len(clicked_name)):
                    if clicked_name[i] != "_":
                        founded_Nick += clicked_name[i]
                    if clicked_name[i] == "_":
                        break
                PlayerSettings.returnObjByTag(tag=founded_tag).Player_tag = None
                nick_storage_Entry.delete(nick_storage_Entry.curselection())
                nick_storage_Entry.insert(row, founded_Nick)
                print("There should be player witn tag = None")
                PlayerSettings.removeNoneObj()
                PlayerSettings.ShowAllPlayers()
            for widget in  Img_widget_container:
                if widget.cget("text") == founded_tag:
                    widget.config(state= tk.ACTIVE)
                    return
    except:
        pass
def TagFnc(txt):
    select = nick_storage_Entry.curselection()
    try:
        row = int(select[0])
        clicked_name = nick_storage_Entry.get(row)
        new_tag = txt
        if PlayerSettings.checkForTag(tag=new_tag) == False and PlayerSettings.returnObjByName(name= clicked_name).Player_tag == None: 
            PlayerSettings.setTagByName(desired_name=clicked_name, tag=txt)
            nick_storage_Entry.insert(row,f"{clicked_name}___Tag: {txt}")
            nick_storage_Entry.delete(row+1)
            for widget in  Img_widget_container:
                if widget.cget("text") == txt:
                    widget.config(state= tk.DISABLED )
                    return
    except:
        pass
def CheckBoxCamera():
    global cameraSett
    if var.get():
        checkbox.configure(text='external')
        newSettings.EditCamera(1)
    else:
        checkbox.configure(text='internal')
        newSettings.EditCamera(0)
def get_scale_value(event=None):
    scale_value = set_line_scale.get()
    return int(scale_value)
def Camera():
    cap = cv2.VideoCapture(newSettings.GetCamera())  
    try:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    except:
        pass


    if cap.isOpened():
        def cam():
            idx = 0
            while True:
                idx += 1 
                _ , frame = cap.read()
                if idx == 1:
                    height, width, _ = frame.shape
                y  = int(set_line_scale.get())
                y_position = height * y / 100
                cv2.line(frame, (0, int(y_position)), (width, int(y_position)), (0, 0, 255), 10)
                cv2.imshow("Line Settings, To quit press Q",frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    print("Q key pressed")
                    newSettings.EditLine(int(y_position))
                    cv2.destroyAllWindows()
                    break
                    

        line_thread = threading.Thread(target=cam)
        line_thread.start()          
def CheckSettings(): 
    try:
        Yolo_confidence = float(confidence_Entry.get())
    except:
        Confidence()
        return 
    if 0 < Yolo_confidence <= 1:
        newSettings.EditConfidence(Yolo_confidence)
    else:
        Confidence()
        return
    if var.get():
        newSettings.EditCamera(1)
    else:
        newSettings.EditCamera(0)

    maxLaps = MaxPlayers_widget.get()
    try:
       maxLaps =  int(maxLaps)
       newSettings.EditLaps(new=maxLaps)
    except:
        Wrong_Input()
        return
    Second_Layer()
def play_mp3(bool):
    if bool== True:
        path = os.path.join(os.path.abspath('Sound'),'music.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        
    else:
        try:
            pygame.mixer.music.stop()
            return
        except:
            return
    MaxPlayers_widget.get()
def play_finish_sound(bool):
    if bool== True:
        path = os.path.join(os.path.abspath('Sound'),'finish.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()     
def play_start_mp3(widget,layer):
    path = os.path.join(os.path.abspath('Sound'),'start_up.mp3')
    widget.insert(0, "Get Ready")
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play() 
    arduino_led = True
    try:
        port = findArduinoPort()
        ser = serial.Serial(port, baudrate=9600)
        if port is None:
            arduino_led = False
    except:
        arduino_led = False
    for i in range(1, 5):
        if i <= 3:
            widget.delete(0, tk.END)
            widget.insert(0, str(i))
            layer.update()
        if i == 4:
            widget.delete(0, tk.END)
            widget.insert(0,"GOOO !!!")
            layer.update()
        initTime = time()
        while True:
            T = time() -initTime 
            if arduino_led:
                WritoToArduino(str(i),ser= ser)
            sleep(0.05)
            if T > 1:
                break 
    widget.delete(0, tk.END)
    if arduino_led:
        ser.close()
        


def Reset():
    global stopOneRace
    #killRacingWidgets()
    stopOneRace = True
    Third_Layer()
def EndRace():
    global stopOneRace
    stopOneRace = True
    count_down.place_forget()
    Widget.dismissWidgets()
    Cleaner.ResetEverything()
    newSettings.Set_default()
    First_layer()
    play_finish_sound(False)
    play_mp3(True)
    try:
        port = findArduinoPort()
        ser = serial.Serial(port, baudrate=9600)
        WritoToArduino(num='5', ser= ser)
        sleep(5)
        ser.close()
    except:
        pass
    
    
def OneRaceStart():
    global StartOneRace
    StartOneRace = True
def Get_unique_race_ID():
    os.makedirs(os.path.abspath('Reports'), exist_ok= True)
    if len(os.listdir(os.path.abspath('Reports'))) == 0:
        race_id = 0
        return race_id
    else:
        race_id = []
        for race in os.listdir(os.path.abspath('Reports')):
            parts = race.split('_')
            # Check if the last part of the split is a number
            if parts[-1].isdigit():
                race_id.append(int(parts[-1]))
        race_id = max(race_id) +1
        return race_id 


############################################################################################################################################
### MAIN LAYER/ FRAME FUNCTIONS ############################################################################################################
############################################################################################################################################

def Settings_layer():
    global ThirdLayer 
    ThirdLayer = False
    layer1.place_forget()
    layerSettings.place(anchor='center', relx=0.5 ,rely=0.3)
    screen_label.pack(padx=10, pady=10)
    screen_entry.pack(padx=10, pady=10)  
    screen_confirm.pack(padx=10, pady=10) 
    back_to_first.pack(padx=10, pady=10) 
    
def First_layer(): 
    global ThirdLayer 
    ThirdLayer = False
    global firstLayer
    firstLayer = True 
    nick_storage_Entry.delete(0, tk.END)
    Cleaner.ResetEverything()
    newSettings.Set_MaxPlayers(None)
    print("Printing Obj .. hope there is none ")
    PlayerSettings.ShowAllPlayers()
    for widget in  Img_widget_container:
        widget.config(state= tk.ACTIVE)
    
    layer2.place_forget()
    layer24.pack_forget()
    layerSettings.place_forget()
    layer1.place(anchor='center', relx=0.5 ,rely=0.3)

    players_label.pack(padx=10, pady= 10)
    players_entry.pack(padx=10, pady= 10) 
    
    players_confirm_normal.pack(padx=10, pady= 10) 
    players_confirm_special.pack(padx=10, pady= 10) 
    profile_label.pack(padx=10, pady= 10)
    profile_entry.pack(padx=10, pady= 10)
    profile_confirm.pack(padx=10, pady= 10)
    Go_to_settings.pack(padx=10, pady= 10)




    

def Second_Layer():
    global ThirdLayer 
    ThirdLayer = False
    if newSettings.Get_MaxPlayers()==None:
        if newSettings.Set_MaxPlayers(val=players_entry.get()):
            newSettings.Set_MaxPlayers(int(players_entry.get()))
        else:
            return
    
    layer1.place_forget()
    layer24.place_forget()
    players_entry.delete(0,tk.END)
    
    # Place main layer 
    layer2.place(anchor='center', relx=0.5 ,rely=0.4)
    
    # First button layer on Main layer of second part mode One race 
    layer21.place(anchor='center', relx=0.2 ,rely=0.55)
    nick_label.pack(padx=10, pady= 10)
    nick_Entry.pack(padx=10, pady= 10)
    nick_confirm.pack(padx=10, pady= 10)
    colors_label.pack(padx=10, pady= 10)

    
    layer22.pack(padx= 10 , pady= 10)
    lenght = len(Img_widget_container) 
    if lenght==0:
        Img_widget_container[0].grid(row= 0, column=1,padx=1) 
    elif lenght <= 9:
        for i,tag in enumerate(Img_widget_container):
            if   i <3:
                tag.grid(row= 0, column=i+1,padx=1) 
            elif i <6:
                tag.grid(row= 1, column=(i+1)-3,padx=1) 
            elif i <9:
                tag.grid(row= 2, column=(i+1)-6,padx=1) 
    else:
        for i,tag in enumerate(Img_widget_container):
            if   i <=3:
                tag.grid(row= 0, column=i+1,padx=1) 
            elif i <=7:
                tag.grid(row= 1, column=(i+1)-4,padx=1) 
            elif i <=11:
                tag.grid(row= 2, column=(i+1)-8,padx=1) 
            elif i <=15:
                tag.grid(row= 3, column=(i+1)-12,padx=1) 
            elif i <=19:
                tag.grid(row= 4, column=(i+1)-16,padx=1) 
            else:
                TooManyTags()
        
    Button_settings_YOLO.pack(padx=10, pady=15)
    back_to_first_layer.pack(padx=10, pady=15)
    
    layer23.place(anchor='center', relx=0.7 ,rely=0.5)
    nick_storage_label.pack(padx=10, pady= 10)
    nick_storage_Entry.pack(padx=10, pady= 10) 
   
    layer231.pack(padx= 10 , pady= 10)
    Delete_tag_button.grid(row= 0, column=0,padx=1)
    nick_storage_confirm.grid(row= 0, column=2,padx=1)
    
    Race_Button.pack(padx=10, pady= 10)
    print("there should be no players from the start")
    PlayerSettings.ShowAllPlayers()
    

    
def Second_Layer_Settings():
    global ThirdLayer 
    ThirdLayer = False
    layer2.place_forget()
    layer24.place(relx=0.1, rely=0.1)
    confidence_label.pack(padx=10,  pady=10)
    confidence_Entry.pack(padx=10,  pady=10)
    checkbox_label.pack(padx=10,  pady=10)
    checkbox.pack(padx=10,  pady=10)
    set_line_label.pack(padx=10,  pady=10)
    set_line_start.pack(padx=10,  pady=10)
    set_line_scale.pack(padx=10,  pady=10)
    MaxPlayers_widget_label.pack(padx=10,  pady=10)
    MaxPlayers_widget.pack(padx=10,  pady=10)
    Back_to_main_frame_2.pack(padx=10,  pady=100)

######################
### ONE RACE FUNCTION
######################

def Third_Layer():
    global stopOneRace
    global StartOneRace
    global OnePlayerFinish
    global ThirdLayer 
    global firstLayer
    firstLayer = False
    ThirdLayer = True
    OnePlayerFinish = False 
    stopOneRace  = False
    start = True

    if PlayerSettings.ReturnNumberOfObj() != newSettings.Get_MaxPlayers():
        NumberOfPlayers(num=newSettings.Get_MaxPlayers(), num2= PlayerSettings.ReturnNumberOfObj() )
        start = False  
    elif PlayerSettings.CheckIfThereIsNone():
        start = False 
    else:
        print("Game started with these folks")
        PlayerSettings.ShowAllPlayers()


###################################################################
####        ONE RACE GAME LOGIC
###################################################################

    if start:
        layer2.place_forget()
        play_mp3(False)
        for obj in PlayerSettings.ReturnList():    
            for img in Img_widget_container:
                if img.cget("text") == obj.Player_tag: 
                    WidgetFrame(tag=obj.Player_tag, frame=tk.Frame(master=window, bg= '#333333', width=100, height=150, relief='raised', borderwidth=10))
                    Widget(nick=obj.Player_nick, 
                           PlayerTag = obj.Player_tag,
                           frame=WidgetFrame.GetFrameBytag(obj.Player_tag), 
                           widget_text=tk.Text(master= WidgetFrame.GetFrameBytag(obj.Player_tag), width=15, height=10, font=  my_font_Racing_text), 
                           widget_label=tk.Label(master=WidgetFrame.GetFrameBytag(obj.Player_tag), text=obj.Player_nick, font=my_font_Racing_text, background='#40E0D0', foreground="black", width=15),
                           widget_tag= tk.Label(master=WidgetFrame.GetFrameBytag(obj.Player_tag),image=img.image, font=my_font_text, background='#40E0D0', foreground="black"),
                           lapsCounter_text= tk.Text(master= WidgetFrame.GetFrameBytag(obj.Player_tag),  width=15, height=1, font=  my_font_Racing_text),
                           position_text= tk.Text(master= WidgetFrame.GetFrameBytag(obj.Player_tag), width=15, height=1, font=  my_font_Racing_text))
                            
        Widget.placeWidgets()
        count_down.place(relx=0.35, rely = 0.8)
        count_down_underline.pack()
        count_down_widget.grid(row=0, column=0,padx=5)
        End_race.grid(row=0, column=1,padx=5)
        Reset_race.grid(row=0, column=2,padx=5)
        Start_race.grid(row=0, column=3,padx=5)

        
        def OneRace(cameraSett, Yolo_confidence, finish_line, maxLaps): 
            global stopOneRace, StartOneRace, OnePlayerFinish
            global finish_thread 
            finish_thread  = False
            print("###############################################################################################################################")
            print(f"One race started with settings: camera {cameraSett}, confidence {Yolo_confidence}, finishLine {finish_line}, maxLaps {maxLaps}")
            print("###############################################################################################################################")

            os.makedirs(os.path.abspath("RacePhoto"), exist_ok= True)
            path_Race_Photo = os.path.abspath("RacePhoto")
            for item in Main_dict:
                path = os.path.join( path_Race_Photo ,Main_dict[item])
                Paths(tag=Main_dict[item], path=path)
                os.makedirs(path, exist_ok= True)
                 
            race_id = Get_unique_race_ID()
            racing_tags = PlayerSettings.ReturnTagList()
            for obj in PlayerSettings.ReturnList():
                Players(tag=obj.Player_tag, nick=obj.Player_nick)
                
            path_to_Yolo_model = os.path.abspath("train3/weights/best.pt")
            model = YOLO(path_to_Yolo_model)
            cap = cv2.VideoCapture(cameraSett)  # external camera
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            first_iter =True
            StartOneRace = False 
            path_sound = os.path.join(os.path.abspath("Sound"),"win.mp3")
            path_temp = os.path.abspath("Temp")

            while True:
                if first_iter == False:
                    deltaTime = time() - initTime
                    count_down_widget.delete(0,tk.END)
                    count_down_widget.insert(0, "{:.2f}".format(deltaTime))
                _ , frame = cap.read()
                result = model.predict(frame) 
                if stopOneRace == True:
                    event.set()
                if StartOneRace == False:
                    pass
                else:
                    if first_iter == True:
                        height, width, _ = frame.shape
                        play_start_mp3(count_down_widget,count_down)
                        first_iter = False 
                        initTime = time()
                        deltaTime = time() - initTime
                        count_down_widget.delete(0,tk.END)
                        count_down_widget.insert(0,  "{:.2f}".format(deltaTime))
                    else:
                        Input = []
                        for i,confidence in enumerate(result[0].boxes.conf.tolist()):
                            Input.append([Main_dict[int(result[0].boxes.cls.tolist()[i])], confidence, i])
                        
                        if len(Input) != 0:
                            for item in Input:
                                founded_confidence, founded_tag, indx = item[1], item[0], item[2]
                                if founded_confidence <= Yolo_confidence:
                                    continue
                                else:
                                    start = time()
                                    if founded_tag in racing_tags:
                                       
                                        Players.UpdateAvailability(Time=deltaTime, MaxLaps=newSettings.GetLaps())
                                        x_min, y_min, x_max, y_max = result[0].boxes.xyxy.tolist()[indx]
                                        y_average =  (y_max - y_min)/2 + y_min
                                        if y_average >= newSettings.GetLine():
                                            score = Players.CheckScoreLen(desired_tag= founded_tag)
                                            Players.UpdateScore(desired_tag= founded_tag, result=float('{:.2f}'.format(deltaTime)),MaxLaps=maxLaps)
                                            score2 = Players.CheckScoreLen(desired_tag= founded_tag)
                                            img_name = f'{race_id}_{Players.GetPlayerNickBytag(desired_tag=founded_tag)}_{Players.CheckScoreLen(desired_tag=founded_tag)-1}.jpg'
                                            img_name_raw = f'{race_id}_{Players.GetPlayerNickBytag(desired_tag=founded_tag)}_{Players.CheckScoreLen(desired_tag=founded_tag)-1}raw.jpg'
                                            path_to_img_tag = os.path.join(path_Race_Photo, founded_tag)
                                            path_to_img = os.path.join(path_to_img_tag ,img_name)
                                            path_to_img_raw = os.path.join(path_to_img_tag ,img_name_raw)
                                            cv2.imwrite(fr"{path_to_img_raw}", frame)
                                            cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 0, 255), 3)
                                            cv2.line(frame, (0, int(newSettings.GetLine())), (width,int(newSettings.GetLine()) ), (0, 0, 255), 10)
                                            cv2.imwrite(fr"{path_to_img}", frame)
                                                
                                            if score2 > score:
                                                resultList = Players.ReturnScore()
                                                Widget.UpdateLeadWidget(ResultList=resultList)
                                                Widget.UpdateScoreWidget(tag=founded_tag, maxlaps= maxLaps)
                                                DetectedScore = Players.GetPlayerScore(desired_tag=founded_tag)
                                                if len(DetectedScore) == maxLaps+1:
                                                    WidgetFrame.ChangeFrameColorToGreen(tag= founded_tag)
                                                    playerObject = Players.GetPlayerObjByTag(desired_tag=founded_tag)
                                                    if playerObject.WinSound == True:
                                                        event.set()
                                                        playerObject.WinSound = False
                                                    
                                                if Players.CheckScoreLen(desired_tag=founded_tag) == 1:
                                                    Widget.writeToWidget(desired_tag=founded_tag, val= "FirstPass\n")
                                                else:
                                                    Widget.writeToWidget(desired_tag=founded_tag, val= f"{len(DetectedScore)-1}............{round((DetectedScore[-1])[1]- (DetectedScore[-2])[1],2)}\n")
                                    end = time() - start
                                    print(end)
                        if Players.CheckAllScore(maxLaps= maxLaps+1):
                            print("race ended")
                            try:
                                port = findArduinoPort()
                                ser = serial.Serial(port, baudrate=9600)
                                WritoToArduino(num='3', ser= ser)
                                ser.close()
                            except:
                                pass
                            create_report(Players=Players.player_list, NumberOfLaps=maxLaps, race_id=race_id)
                            return
                            
            
     
            
                   
        def OneFinishSound():

            path = os.path.join(os.path.abspath('Sound'),'win.mp3')
            data, samplerate = sf.read(path)
            while True:
                if stopOneRace:
                    return
                event.wait()
                sd.play(data, samplerate)
                event.clear()



        event = threading.Event()                            
        race_thread = threading.Thread(target=OneRace, args=(newSettings.GetCamera(), newSettings.GetConfidence(), newSettings.GetLine(),  newSettings.GetLaps()))
        race_thread.start()
        
        OneFinishSoundThread = threading.Thread(target=OneFinishSound)
        OneFinishSoundThread.start()
   
def spree():
    pass     
        
        
def runFromJSON(inputJson):
    pass


################################################################################################################################################################################
### MAIN  ######################################################################################################################################################################
################################################################################################################################################################################


### Basic setting ### 
window = tk.Tk()
window.geometry('1920x1080')
window.title("CAR GUI")
newSettings = Settings()
from fonts import my_font_label, my_font_widget, my_font_text, my_font_count_down, my_font_Racing_text
global ThirdLayer 
ThirdLayer = False




### GUI ICON 
#icon = tk.PhotoImage(file= os.path.join(os.path.abspath("Dependencies"),"icon.png")) : TODO Icon photo
#window.iconphoto(True, icon)

### Settings for background image
path_to_background_image = os.path.join(os.path.abspath("Dependencies"),"car.jpg")
background_image = ImageTk.PhotoImage(Image.open(path_to_background_image ))
background_image_label = tk.Label(window,   image= background_image)
background_image_label.place(x=0, y=0, relwidth=1, relheight=1)


# Setting new FRAMES
layer1  = tk.Frame(master=window, bg= '#333333',borderwidth =10, relief='raised', width=100, height=200)
layer2  = tk.Frame(master=window, bg= '#1E1E1E',borderwidth =10, relief='raised', width=1200, height=1080)
layer21 = tk.Frame(master=layer2, bg= '#333333', width=100, height=200, relief='raised',borderwidth =10)
layer22 = tk.Frame(master=layer21, bg= '#333333', width=100, height=150, relief='raised')
layer23 = tk.Frame(master=layer2, bg= '#333333', width=100, height=200, relief='raised',borderwidth =10)
layer231 = tk.Frame(master=layer23, bg= '#333333', width=100, height=200, relief='raised',borderwidth =10)
layer24 = tk.Frame(master=window, bg= '#1E1E1E',borderwidth =10, relief='raised', width=1000, height=700)
#layer25 = tk.Frame(master=layer2, bg= '#333333', width=50, height=50, relief='raised',borderwidth =10)
layerSettings = tk.Frame(master=window, bg= '#333333',borderwidth =10, relief='raised', width=100, height=200)
layer3  = tk.Frame(master=window, bg= '#333333', width=100, height=20, relief='raised',borderwidth =10)
count_down = tk.Frame(master=window, bg= '#333333', width=25, height=20, relief='raised',borderwidth =10)
count_down_underline =  tk.Frame(master=count_down, bg= '#333333', width=25, height=20, relief='raised',borderwidth =10)


###############
### WIDGETS ###
###############


# WIDGETS OF  FRAME 1 SETTINGS



screen_label  = tk.Label(master= layerSettings, text='Screen Info', background='#333333', foreground='white', font= my_font_label)
screen_entry  = ttk.Combobox(master=layerSettings, width=50,height=1, values=Resolutions(), font=my_font_text)
screen_confirm = tk.Button(master=layerSettings, text="Founded resolution",command=changeResolution, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget)
back_to_first = tk.Button(master=layerSettings, text="back",command=First_layer, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget)

### WIDGETS OF FRAME 1 MAIN

players_label  = tk.Label(master= layer1, text='Number of Players', background='#333333', foreground='#EAEAEA', font= my_font_label)
players_entry  = tk.Entry(master=layer1, font=my_font_text)
players_confirm_normal = tk.Button(master=layer1, text="OneRace",command=Second_Layer, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, relief='raised')
players_confirm_special = tk.Button(master=layer1, text="Spree", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, relief='raised')

profile_label  = tk.Label(master= layer1, text='Player Profile', background='#333333', foreground='#EAEAEA', font= my_font_label)
profile_entry  = tk.Listbox(master=layer1, width=20, height=1, font=my_font_text)
profile_confirm = tk.Button(master=layer1, text="Load",command=Second_Layer, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget)

Go_to_settings =  tk.Button(master=layer1, text="Screen Settings",command=Settings_layer, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget)

###  WIDGETS OF FRAME 2 MAIN

ButtonStartRace = tk.Button(master=layer2, text="Proceed", background='#4CAF50', foreground='#FFA500', font= my_font_widget)

nick_label = tk.Label(master= layer21, text="Type a nick", background='#333333', foreground='#EAEAEA', font= my_font_label)
nick_Entry = tk.Entry(master=layer21, font=my_font_text)
nick_confirm = tk.Button(master=layer21, text="Confirm", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, command=add_player_nick)


colors_label = tk.Label(master= layer21, text="Tag to choose", background='#333333', foreground='#EAEAEA', font= my_font_label)

path_depend = os.path.abspath("Dependencies")
Img_list = []
Img_widget_container = [] 


for image in os.listdir(path_depend):
    if image != "car.jpg":
        img_path = os.path.join(path_depend, image)
        Img_list.append(img_path)
        image_pillow = Image.open(img_path)  # Replace "image.jpg" with the path to your JPEG image file
        image_resized= ImageTk.PhotoImage(image_pillow.resize((100, 100),Image.LANCZOS)) #Image.LANCZOS filter for downsizing imgs 
        img_button = tk.Button(master=layer22,image =image_resized, text=image[:-4], command=lambda text=image[:-4]: TagFnc(text)) 
        img_button.image = image_resized # adding image_resized to the img_button object, preventing garbage collection 
        Img_widget_container.append( img_button)

#### Hard Coded dictionary, needs to be, because it matches the YOLO MODEL
global Main_dict
Main_dict = {
    0  : "blesk",
    1  : "slunce", 
    2  : "mesic",
    3  : "ohen",
    4  : "riman", 
    5  : "rytir",
    6  : "sipka",
    7  : "srdce", 
    8  : "valhala"
}

Button_settings_YOLO = tk.Button(master=layer21, text="Race Settings", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, command=Second_Layer_Settings)
back_to_first_layer = tk.Button(master=layer21, text="Back",command=First_layer,  background='#4CAF50', foreground='#EAEAEA', font= my_font_widget,width=6, height=2)

nick_storage_label = tk.Label(master= layer23, text="Created Players", background='#333333', foreground='#EAEAEA', font= my_font_label)
nick_storage_Entry = tk.Listbox(master= layer23,height=12, width=25,font=my_font_text)

Race_Button = tk.Button(master=layer23, text="Start_Race", background='#FFA500', foreground='#EAEAEA', font= my_font_widget, command=Third_Layer)
Delete_tag_button  =  tk.Button(master=layer231, text="Delete tag", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, command=Delete_tag)
nick_storage_confirm = tk.Button(master=layer231, text="Delete selected", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, command=Delete_player)
###  WIDGETS OF FRAME 2 SETTINGS

Back_to_main_frame_2 =  tk.Button(master=layer24 ,text="Back",command=CheckSettings, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, relief='raised')
confidence_label = tk.Label(master= layer24, text="YOLO confidence", background='#333333', foreground='#EAEAEA', font= my_font_label)
confidence_Entry = tk.Entry(master=layer24, font=my_font_text)
confidence_Entry.insert(0, 0.7)
MaxPlayers_widget_label = tk.Label(master= layer24, text="MaxLaps", background='#333333', foreground='#EAEAEA', font= my_font_label)
MaxPlayers_widget = tk.Entry(master=layer24, font=my_font_text)
MaxPlayers_widget.insert(0, 6)

set_line_label = tk.Label(master= layer24, text="Set Starting Line", background='#333333', foreground='#EAEAEA', font= my_font_label)
set_line_start = tk.Button(master=layer24 ,text="On/ Off",command=Camera, background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, relief='raised')
set_line_scale = ttk.Scale(master=layer24, from_=0, to=100, command=get_scale_value)
checkbox_label = tk.Label(master= layer24, text="Set Camera type", background='#333333', foreground='#EAEAEA', font= my_font_label)
var = tk.BooleanVar()
checkbox = tk.Checkbutton(master= layer24, text="internal", variable=var, command=CheckBoxCamera, font=my_font_widget)


###  WIDGETS OF Countdown
count_down_widget = tk.Entry(master=count_down_underline, font=my_font_count_down, width=5)
End_race = tk.Button(master=count_down_underline, text="End_race", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, command=EndRace)
Reset_race = tk.Button(master=count_down_underline, text="Reset_race ", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget)
Start_race = tk.Button(master=count_down_underline, text="Start_race", background='#4CAF50', foreground='#EAEAEA', font= my_font_widget, command= OneRaceStart)
Race_info =  tk.Label(master=count_down_underline, text="info", background='#333333', foreground='#EAEAEA', font= my_font_label)

play_mp3(True)
First_layer()
tk.mainloop()