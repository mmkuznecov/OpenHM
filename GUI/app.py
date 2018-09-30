import Tkinter as tk
import Tkinter, Tkconstants, tkFileDialog
from PIL import ImageTk, Image
import ctypes
import hm_class_mapping as hm


al_type = str("null")

root = tk.Tk()
root.geometry("500x200")
root.title("OpenHM")
root.configure(background = "#F46524")
root.iconbitmap(default="icon.ico")

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('OpenHM')


mb = tk.Menubutton ( root, text="btn_text", height = 2, width = 32, background = "white", relief = "groove")
mb.menu  =  tk.Menu( mb, tearoff = 0)
mb["menu"]  =  mb.menu
alg1 = "Alg1"
alg2 = "Alg2"
alg3 = "Alg3"
items = [[alg1, tk.IntVar()], [alg2, tk.IntVar()], [alg3, tk.IntVar()]]

def Item_test():
	ret = str("null")
	for item in items:
		if item[1].get():
			ret = str(item[0])
			mb.config(text = str(item[0]))
			item[1].set(1)
		else:
			item[1].set(0)
	return ret

for i in items:
	mb.menu.add_checkbutton ( label=i[0], variable = i[1], command = Item_test)		

def start_stream_mapping():
	root.destroy()
	pass
	

def start_path_mapping():
	algorithm_tipe = Item_test()
	pathfilename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("video","*.mp4"),("video", "*.avi"),("all files","*.*")))
	if pathfilename != "":
		root.destroy()
		a = hm.Mkmap(pathfilename)
		
		if algorithm_tipe == "Alg1":
			a.mapping1()
		elif algorithm_tipe == "Alg2":
			a.mapping2()
		elif algorithm_tipe == "Alg3":
			a.mapping3()
		else:
			a.mapping1()

#image =tk.PhotoImage(file = "C:\\Python27\\OpenHM\\App\\logo_good.png")


stream_button = tk.Button(root, text = 'Start streaming', height = 2, width = 13, background = "white", command = start_stream_mapping, relief = "groove")

stream_button2 = tk.Button(root, text = 'Analyze video', height = 2, width = 13, background = "white", command = start_path_mapping, relief = "groove")

image = Image.open('logo_good.png').resize((228,107))
image2 = ImageTk.PhotoImage(image)
logo = tk.Label(root, image = image2, height=100, borderwidth=0, highlightthickness=0)

#path_entry = tk.Entry(root, width = 33)


mb.config(text = "Choose algoritm type")

stream_button.place(x =370, y = 150, anchor = "e")
stream_button2.place(x = 470, y = 150, anchor = "e")
logo.place(x = 130, y = 100, anchor = "center")
#path_entry.place(x = 470, y = 100, anchor = "e")
mb.place(x = 470, y = 50, anchor = "e")

root.mainloop()

