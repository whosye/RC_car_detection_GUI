from Errors import TakenNick,  TakenTag, NoTag, NotNum, NumOfPlayers
import pygame, os

path_to_win_sound = os.path.join(os.path.abspath("Sound"), "win.mp3")

class Settings:

    def __init__(self):
        self.cameraSett = 0
        self.Yolo_confidence = 0.7
        self.finish_line = 0
        self.maxLapse = 6
        self.Penalty = False
        self.MaxPlayers = None

    def GetCamera(self):
        return self.cameraSett
    def GetConfidence(self):
        return self.Yolo_confidence 
    def GetLine(self):
        return self.finish_line
    def GetLaps(self):
        return self.maxLapse
    def EditCamera(self, new):
        self.cameraSett = new
    def EditConfidence(self, new):
        self.Yolo_confidence = new
    def EditLine(self, new):
        self.finish_line = new
    def EditLaps(self, new):
        self.maxLapse = new 
    def TogglePenalty(self):
        if self.Penalty == False:
            self.Penalty = True
            return self.Penalty
        else:
            self.Penalty = False
            return self.Penalty
    def GetPenaltyState(self):
        return self.Penalty
    def Set_MaxPlayers(self, val)-> bool:
        if val == None:
            self.MaxPlayers = None
        else:
            try:
                val = int(val)
                if not(val > 0 and val <=6):
                    NumOfPlayers()
                    return False
                else:
                    self.MaxPlayers = val 
                    return True
            except:
                NotNum()
                return False
    def Get_MaxPlayers(self):
        return self.MaxPlayers
    
    def Set_default(self):
        self.cameraSett = 0
        self.Yolo_confidence = 0.7
        self.finish_line = 0
        self.maxLapse = 6
        self.Penalty = False
        self.MaxPlayers = None
    
            

class PlayerSettings(Settings):
    PlayerList = []
    def __init__(self,nick:[str]) -> None:

        print(f"creating {nick}")
        self._nick = nick
        self._tag = None
        PlayerSettings.PlayerList.append(self)
    @property
    def Player_nick(self):
        return self._nick
    
    @Player_nick.setter
    def Player_nick(self, val):
            self._nick = val 

    @Player_nick.getter
    def Player_nick(self):
        return self._nick
        
    @Player_nick.deleter
    def Player_nick(self):
        del self._nick
        
    @property
    def Player_tag(self):
        return self._tag
    
    @Player_tag.setter
    def Player_tag(self, val):
            self._tag = val 

    @Player_tag.getter
    def Player_tag(self):
        return self._tag
        
    @Player_tag.deleter
    def Player_tag(self):
        del self._tag 
 
    @classmethod
    def setTagByName(cls,desired_name, tag):
        for player in cls.PlayerList:
            if desired_name == player.Player_nick:
                player.Player_tag = tag
                print("Founded, Showing all created players",'\n')
                PlayerSettings.ShowAllPlayers()
                return
    
    @classmethod
    def checkForName(cls,name)->bool:
        for player in cls.PlayerList:
            if name == player.Player_nick:
                TakenNick(name)
                return True
        return False
    
    @classmethod
    def checkForTag(cls,tag)->bool:
        for player in cls.PlayerList:
            if tag == player.Player_tag:
                TakenTag(tag)
                return True
        return False
                

    @classmethod
    def ShowAllPlayers(cls):
        if len(cls.PlayerList) ==0:
            print("Empty player list")
        else:
            for player in cls.PlayerList:
                print(f"Nick: {player.Player_nick} tag: {player.Player_tag}")
        
    @classmethod
    def returnObjByName(cls, name): 
        for player in cls.PlayerList:
            if name == player.Player_nick:
                return player

    @classmethod
    def returnObjByTag(cls,tag):
        for player in cls.PlayerList:
            if tag == player.Player_tag:
                return player     
            
    @classmethod
    def removeObjBy(cls,val, name = True):
        if name:
            for player in cls.PlayerList:
                if val == player.Player_nick:
                    cls.PlayerList.remove(player)
        else:  
            for player in cls.PlayerList:
                if val == player.Player_tag:
                    cls.PlayerList.remove(player) 
    @classmethod
    def removeNoneObj(cls):
        for obj in cls.PlayerList:
            if obj.Player_nick == None and obj.Player_tag == None:
                cls.PlayerList.remove(obj)
    @classmethod
    def RemoveAllObj(cls):
        cls.PlayerList = []
        
    @classmethod
    def CheckIfThereIsNone(cls) ->bool:
        for obj in cls.PlayerList:
            if obj.Player_nick == None or obj.Player_tag == None:
                NoTag(obj.Player_nick)
                return True
    @classmethod
    def ReturnNumberOfObj(cls):
        return len(cls.PlayerList)
    @classmethod
    def ReturnList(cls)->list:
        return cls.PlayerList
    @classmethod
    def ReturnTagList(cls):
        tagList = []
        for obj in cls.PlayerList:
            tagList.append(obj.Player_tag)
        return tagList

class Players():
    player_list = []
    pause = 5
    def __init__(self,tag, nick):
        self.tag = tag 
        self._nick = nick 
        self.Score = []
        self.Round_count = 0
        self.Available = True
        self.lastTimeCheck = 0 
        self.WinSound = True
        self.relativeScore = []
        Players.player_list.append(self)
     
    @classmethod
    def UpdateScore(cls, desired_tag,result, MaxLaps):
        for player in cls.player_list:
            if desired_tag == player.tag:
                if player.Available == True:
                    if len(player.Score) != MaxLaps+1: # +1 because firtst round does not count
                        player.Available = False      
                        player.Score.append([player.Round_count, result])
                        player.Round_count += 1         
                        if len(player.Score)!= 1 and len(player.Score)!= 0:
                            player.relativeScore.append([player.Round_count-1,round((player.Score[-1])[1]- (player.Score[-2])[1],2)])
      
    @classmethod
    def UpdateAvailability(cls, Time,  MaxLaps ):
        for player in cls.player_list:
            if player.Available == False:
                if len(player.Score) != 0:
                    lastTime = (player.Score[-1])[1]
                    if Time - lastTime >= cls.pause:
                        player.Available = True
                    else:
                        player.Available = False
                elif len(player.Score) == MaxLaps:
                    player.Available = False
                        
    @classmethod
    def SetFirstTimeCheck(cls, desired_tag, Time):
        for player in cls.player_list:
            if player.tag == desired_tag:
                    player.lastTimeCheck = Time 
                
                
    @classmethod
    def CheckAvailability(cls, desired_tag):
        for player in cls.player_list:
            if player.tag == desired_tag:
                    return player.Available 
                
    @classmethod       
    def CheckScoreLen(cls, desired_tag):
        for player in cls.player_list:
            if player.tag == desired_tag:
                    return len(player.Score)


    @classmethod
    def ClearPlayer(cls):
        cls.player_list.clear()
            
    @classmethod
    def ShowPlayers(cls):
        for player in cls.player_list:
                print(player.__dict__)
        
    @classmethod
    def GetPlayerScore(cls,desired_tag):
        for player in cls.player_list:
            if desired_tag == player.tag:
                return player.Score
    
    @classmethod
    def GetAllScore(cls):
        return Players.player_list
    @classmethod
    def CheckAllScore(cls, maxLaps)->bool:
        exit_race = True
        for obj in Players.player_list:
            if len(obj.Score) < maxLaps:
                exit_race =  False
        return exit_race
    @classmethod
    def GetPlayerNickBytag(cls,desired_tag):
        for player in cls.player_list:
            if desired_tag == player.tag:
                return player._nick  
    @classmethod
    def GetPlayerTagByNick(cls,desired_nick):
        for player in cls.player_list:
            if desired_nick == player._nick:
                return player.tag 
    @classmethod
    def GetPlayerObjByNick(cls,desired_nick):
        for player in cls.player_list:
            if desired_nick == player._nick:
                return player
    @classmethod
    def GetPlayerObjByTag(cls,desired_tag):
        for player in cls.player_list:
            if desired_tag == player.tag:
                return player
            
            
    @classmethod
    def ReturnScore(cls):
        def custom_sort(player):
            if player.Score:
                return (-player.Score[-1][0], player.Score[-1][1])
            else:
                return (float('-inf'), float('inf'))
        sorted_players = sorted(cls.player_list, key=custom_sort)
        result  = []
        j=0
        for player in (sorted_players):
            if player.Score:
                print(f"{player.tag}: Lap {player.Score[-1][0]}, Time {player.Score[-1][1]}")
                j += 1
                result.append([player.tag,j])
            else:
                print(f"{player.tag}: No laps recorded.")
                result.append([player.tag,None])

        return result
      
                    
 
class WidgetFrame:
    frames = []
    
    def __init__(self, tag, frame) -> None:
        self._tag = tag 
        self._frame = frame 
        WidgetFrame.frames.append(self)
    @property
    def Frame(self):
        return self._frame
    @property
    def tag(self):
        return self._tag
    @classmethod
    def GetFrameBytag(cls, desired_tag):
        for frame in cls.frames:
            if frame.tag == desired_tag:
                return frame.Frame
    @classmethod
    def Clear_Frame_list(cls):
        cls.frames = []
    @classmethod  
    def ChangeFrameColorToGreen(cls,tag):
        frame = cls.GetFrameBytag(desired_tag=tag)
        frame.configure(bg = "green")
    
        
        

class Widget(PlayerSettings):

    widget_container = []
    def __init__(self, nick,frame ,widget_text, widget_label, widget_tag,lapsCounter_text,position_text, PlayerTag  ):
        import tkinter as tk 
        self._nick = nick
        self._frame = frame 
        self._text = widget_text
        self._label = widget_label
        self._tag = widget_tag
        self._lapsCounter_text = lapsCounter_text
        self._position_text = position_text
        self.PlayerTag =  PlayerTag 
        
        Widget.widget_container.append(self)
            
    def get_attributes(self):
        for key, value in self.__dict__.items():
            print(f'Attribute: {key}, Value: {value}')
        
    @property
    def get_nick(self):
        return self._nick 
    @get_nick.getter
    def get_nick(self):
        return self._nick     
    @property
    def frame(self):
        return self._frame
    @frame.getter
    def frame(self):
        return self._frame 

    @property
    def widget_frame(self):
        return self._frame 
    
    @widget_frame.setter
    def widget_frame(self, val):
            self._frame = val 

    @widget_frame.getter
    def widget_frame(self):
        return self._frame
        
    @widget_frame.deleter
    def widget_frame(self):
        del self._frame   
        

    @property
    def widget_lapsCounter_text(self):
        return self._lapsCounter_text
    
    @widget_lapsCounter_text.setter
    def widget_lapsCounter_text(self, val):
            self._lapsCounter_text = val 

    @widget_lapsCounter_text.getter
    def widget_lapsCounter_text(self):
        return self._lapsCounter_text
        
    @widget_lapsCounter_text.deleter
    def widget_lapsCounter_text(self):
        del self._lapsCounter_text  

    @property
    def widget_position_text (self):
        return self._position_text 
    
    @widget_position_text.setter
    def widget_position_text(self, val):
            self._position_text = val 

    @widget_position_text.getter
    def widget_position_text(self):
        return self._position_text
        
    @widget_position_text.deleter
    def widget_position_text(self):
        del self._position_text
    @property
    def widget_text(self):
        return self._text 
    
    @widget_text.setter
    def widget_text(self, val):
            self._text = val 

    @widget_text.getter
    def widget_text(self):
        return self._text
        
    @widget_text.deleter
    def widget_text(self):
        del self._text  

    @property
    def widget_label (self):
        return self._label 
    
    @widget_label.setter
    def widget_label(self, val):
            self._label = val 

    @widget_label.getter
    def widget_label(self):
        return self._label
        
    @widget_label.deleter
    def widget_label(self):
        del self._label  

    @property
    def widget_tag(self):
        return self._tag
    
    @widget_tag.setter
    def widget_tag(self, val):
            self._tag = val 

    @widget_tag.getter
    def widget_tag(self):
        return self._tag
        
    @widget_tag.deleter
    def widget_tag(self):
        del self._tag
    
    @classmethod
    def placeWidgets(cls):
        import tkinter as tk 
        
 
        x = 0.1
        for i, widget in enumerate(cls.widget_container):
            
            if i == 0: 
                widget.widget_frame.place(relx=0.1 ,rely=0.4, anchor='center')
                widget.widget_tag.pack(pady= 5)
                widget.widget_label.pack(pady= 5)
                widget.widget_position_text.pack(pady=5)
                widget.widget_lapsCounter_text.pack(pady= 5)
                widget.widget_text.pack(pady= 5)

                

            else:
                x += 0.2
                widget.widget_frame.place(relx=x ,rely=0.4, anchor='center')
                widget.widget_tag.pack(pady= 5)
                widget.widget_label.pack(pady= 5)
                widget.widget_position_text.pack(pady=5)
                widget.widget_lapsCounter_text.pack(pady= 5)
                widget.widget_text.pack(pady= 5)

                
    @classmethod         
    def dismissWidgets(cls):
        for widget in cls.widget_container:
            widget.widget_frame.place_forget()
    @classmethod         
    def ClearContainer(cls):
        cls.widget_container = []
    @classmethod         
    def returnContainer(cls):
        return cls.widget_container
    @classmethod         
    def clearWidgetText(cls):
        import tkinter as tk
        for widget in cls.widget_container:
            widget.widget_text.delete(0, tk.END)
    @classmethod
    def writeToWidget(cls, desired_tag, val):
        for widget in cls.widget_container:
            widget_tag = PlayerSettings.returnObjByName(widget.get_nick).Player_tag
            if  widget_tag == desired_tag:
                widget._text.insert(1.0, val)
                return
    @classmethod
    def UpdateLeadWidget(cls, ResultList): # :TODO 
        for widget in cls.widget_container:
            widget.widget_position_text.delete("1.0", "end")
            for result in ResultList:
                if result[1] == None:
                    continue
                if widget.PlayerTag == result[0]: 
                    widget.widget_position_text.insert("1.0",f"Pos................{result[1]}")
                    
    @classmethod
    def UpdateScoreWidget(cls, tag, maxlaps): # :TODO 
        score = len(Players.GetPlayerScore(desired_tag=tag))
        for widget in cls.widget_container:
            if widget.PlayerTag == tag: 
                if score == 1 or score ==0:
                    return
                else:
                    widget.widget_lapsCounter_text.delete("1.0", "end")
                    widget.widget_lapsCounter_text.insert("1.0",f"Laps..............{score-1}/{maxlaps}")


        
                    

        
class Paths: 
    paths = [] 
    def __init__(self, tag, path) -> None:
        self._tag = tag 
        self._path = path
        Paths.paths.append(self)
    @property
    def path(self):
        return self._path
    @path.getter
    def path(self):
        return self._path
    @path.setter
    def path(self,val):
        self._tag = val 
        return val 
    @classmethod
    def get_path(cls,tag): 
        for path in cls.paths: 
            if path.tag == tag: 
                return path.path 
            
class Cleaner():
    @classmethod
    def ResetEverything(cls):
        for obj in Widget.returnContainer():
            del obj.widget_frame
        Widget.ClearContainer()
        PlayerSettings.RemoveAllObj()
        WidgetFrame.Clear_Frame_list()
        Players.ClearPlayer()
        
    @classmethod
    def ResetRace(cls):
        for obj in Widget.returnContainer():
            del obj.widget_frame
        Widget.ClearContainer()
        WidgetFrame.Clear_Frame_list()
    
        