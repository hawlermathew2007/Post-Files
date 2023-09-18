from tkinter import *
from tkinter import messagebox
import hashlib
import os

sha256 = hashlib.sha256()

def login():
	user = entry1.get()
	pword = entry2.get()

	if user == "" or pword == "":
		messagebox.showwarning(title= "Unable to allow", message= "PLEASE FILL UP THE BLANK BOX!")
		return

	data = pword.encode()
	sha256.update(data)

	with open("player_information.txt", "r") as f:		#should be less heavy if it's each 
		lists = f.readlines()
	for i in range(len(lists)):
		if ("Username: " + str(user) + "\n") == lists[i]:
			check_pword = lists[i + 2]
			if ("Password: " + sha256.hexdigest() + "\n") == check_pword:
				highscore = lists[i + 3][12:]
				if not os.path.exists("highscore_pi.txt"):
					f = open("highscore_pi.txt", "x")
				with open("highscore_pi.txt", "w") as f:
					f.write("")
				with open("highscore_pi.txt", "a") as f:
					f.write(highscore)
					f.write(user)
				window.destroy()
				return
			else:
				messagebox.showwarning(title= "Try again!", message= "Your password is incorrect!")
				window.destroy()
				import suorlg
				return

	messagebox.showwarning(title= "Your username is unvailable", message="There's no account named " + user)
	window.destroy()
	import suorlg

	print("Password: " + sha256.hexdigest())

window = Tk()
window.title("Login")
window.resizable(False, False)

check = IntVar()

label = Label(window, text= "Login", font= ("Arial", 40), pady= 20)
label.pack()

block = Label(window)
block.pack()

frame = Frame(window)
frame.pack()

username = Label(frame, text= "Username: ", font= ("Arial", 20))
username.grid(row= 0, column= 0, sticky= W)

entry1 = Entry(frame, font= ("Consolas", 18), width= 25)
entry1.grid(row= 0, column= 1)

block = Label(frame, height= 2)
block.grid(row= 1, column= 0)

password = Label(frame, text= "Password: ", font= ("Arial",20))
password.grid(row= 2, column= 0, sticky= W)

entry2 = Entry(frame,show="*", font= ("Consolas",18), width= 25)
entry2.grid(row= 2, column= 1)

block = Label(frame)
block.grid(row= 3, column= 0)

show = Checkbutton(frame, text= "Show password ", font= ("Arial", 15), variable= check, onvalue= 1, offvalue= 0, 
	command= lambda: entry2.config(show= '') if check.get()==1 else entry2.config(show="*"))
show.grid(row= 4, column=0, sticky=W)

blockit = Label(window)
blockit.pack()

login = Button(window, text= "Login", padx= 18, pady= 4, font= ("Arial",25), command= login)
login.pack()

blockit = Label(window)
blockit.pack()

word = Label(window, text= "Login to see your current high score!", font=("Arial",15), padx= 15, pady= 10)
word.pack()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (500 / 2))
y = int((screen_height / 2) - (470 / 1.75))

window.geometry(f'{500}x{470}+{x}+{y}')

window.mainloop()