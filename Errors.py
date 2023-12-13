from tkinter import messagebox
from screeninfo import get_monitors
def Empty():
    messagebox.showerror("Error", "Empty Input!")
def NotNum():
    messagebox.showerror("Error", "Input must be an integer number!")
def NumOfPlayers():
    messagebox.showerror("Error", "Num of player must be between 1 and 6")
def MaxPlayers(num):
    messagebox.showerror("Error", f"Max number of players is {num}")
def NumberOfPlayers(num, num2):
    messagebox.showerror("Error", f"Selected number of players is {num}, but only {num2} were made.")
def Wrong_Input():
    messagebox.showerror("Error", "Wrong_Input")
def nickLen():
    messagebox.showerror("Error", "Nick should have at least 3 characters lenght")
def ColorTaken(color, player):
    messagebox.showerror("Error", f"Color: {color} is taken by player {player}")
def TakenNick(nick):
    messagebox.showerror("Error", f"NICK: {nick}, is taken!")
def TakenTag(tag):
    messagebox.showerror("Error", f"TAG: {tag}, is taken!")
def MissingCol():
    messagebox.showerror("Error", f"missing color!")
def Confidence():
    messagebox.showerror("Error", f"Confidence must be a number between (0,1)")
def TooManyTags():
    messagebox.showerror("Error", f"Too many tags! ")
def UnsupportedChar(tag):
    messagebox.showerror("Error", f"This: '{tag}', is forbidden!")
def NoTag(Player):
    messagebox.showerror("Error", f"{Player}' does not have a TAG choosen.")