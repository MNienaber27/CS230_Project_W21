import tkinter as Tk
from tkinter.filedialog import askopenfilename,askdirectory
import subprocess

### CHANGE TO YOUR UCI ACCOUNT USERNAME ###
USERNAME = "jsmith"

### LOCATION OF THE SSH KEY PAIR FOR OPENLAB ###
KEY_LOC = "~/.ssh/id_rsa"

REMOTE_ADDRESS = USERNAME + "@openlab.ics.uci.edu"

remote_files = ["None"]
ssh = subprocess.Popen(['ssh','-i',KEY_LOC,REMOTE_ADDRESS],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     universal_newlines=True,
                     bufsize=0)
ssh.stdin.write('ls')
ssh.stdin.close()

for line in ssh.stdout:
        remote_files.append(line.strip())

window = Tk.Tk()
window.title('File Explorer')
window.geometry("500x500")
window.config(background = "white")
copy_file = ''
# move_loc = ''
def browseFiles():
    global copy_file
    filename = askopenfilename(initialdir = './',title = 'Select a file')
    copy_file=filename
    parse = filename.split('/')
    label_file_explorer.configure(text="File Opened: "+ parse[-1])
# def browseDir():
#     global move_loc
#     filename = askdirectory(initialdir = '/',title = 'Select a directory')
#     move_loc=filename
#     label_dir_explorer.configure(text="Directory: "+ filename)
def store() :
    # global copy_file
    ssh = subprocess.Popen(['scp',"-i",KEY_LOC,copy_file,REMOTE_ADDRESS + ':/home/hadoop/'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    # stdout, stderr = ssh.communicate()
def retrieve():
    get_file = variable.get()
    path = REMOTE_ADDRESS + ':/home/hadoop/' + get_file
    ssh = subprocess.Popen(['scp',"-i",KEY_LOC,path, './'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    stdout, stderr = ssh.communicate()
label_file_explorer = Tk.Label(window, 
                            text = "No File Chosen",
                            width = 55, height = 4, 
                            fg = "blue")
label_dir_explorer = Tk.Label(window, 
                            text = "No Directory Chosen",
                            width = 55, height = 4, 
                            fg = "blue")

button_exit = Tk.Button(window, 
                     text = "Exit",
                     command = exit)
button_explore = Tk.Button(window, 
                        text = "Choose File",
                        command = browseFiles)
button_store = Tk.Button (window, 
                     text = "Store",
                     command = store)
button_retrieve = Tk.Button (window, 
                     text = "Retrieve",
                     command = retrieve)
# button_dir = Tk.Button(window, 
#                         text = "Choose Directory",
#                         command = browseDir)
variable = Tk.StringVar(window)
variable.set(remote_files[0])
file_menu = Tk.OptionMenu(window, variable,*remote_files)
label_file_explorer.grid(column = 1, row = 1)
button_explore.grid(column = 1, row = 2)
# label_dir_explorer.grid(column = 1, row =3)
# button_dir.grid(column=1,row=4)
button_store.grid(column=1,row=3)
file_menu.grid(column=1,row=4)
button_retrieve.grid(column=1,row=5)
button_exit.grid(column = 1,row = 6)
window.mainloop()