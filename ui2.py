# ui2.py supports both file and directory upload/delete/retrieve
import tkinter as Tk
from tkinter.filedialog import askopenfilename, askdirectory
import subprocess

KEY_LOC = "~/Downloads/KeyPair3.pem"
REMOTE_ADDRESS = "hadoop@ec2-3-239-255-133.compute-1.amazonaws.com"
# KEY_LOC = "~/.ssh/id_rsa"
# REMOTE_ADDRESS = "localhost"
remote_files = ["None"]
copy_file = ''
move_loc = ''

def updateFiles():
    global remote_files
    remote_files = ["None"]
    ssh = subprocess.Popen(['ssh', '-i', KEY_LOC, REMOTE_ADDRESS],
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)

    ssh.stdin.write('hdfs dfs -ls /')
    ssh.stdin.close()
    for line in ssh.stdout:
            remote_files.append(line.strip().split('/')[-1])

# single file upload
def browseFiles():
    global copy_file
    filename = askopenfilename(initialdir='/', title='Select a file')
    copy_file = filename
    parse = filename.split('/')
    label_file_explorer.configure(text="File Opened: " + parse[-1])

# dir upload
def browseDir():
    global move_loc
    dirname = askdirectory(initialdir='/', title='Select a directory')
    move_loc = dirname
    label_dir_explorer.configure(text="Directory: " + move_loc)

def storefile():
    ### DOES NOT DELETE FILE AFTER ADDING IT TO MASTER. TO BE IMPLEMENTED###
    # scp -i ~/Downloads/KeyPair3.pem test.txt hadoop@ec2-52-87-191-193.compute-1.amazonaws.com:/home/hadoop/
    # ssh = subprocess.Popen(['scp', '-i', KEY_LOC, copy_file, REMOTE_ADDRESS + ':/home/hadoop/'],
    fname = copy_file.split('/')[-1]
    ssh = subprocess.Popen(['scp', '-i', KEY_LOC, copy_file, REMOTE_ADDRESS + ':/home/hadoop/'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    sp = subprocess.Popen(['ssh','-i', KEY_LOC, REMOTE_ADDRESS, 'hdfs dfs -put ' + fname + ' /'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    updateFiles()
    updateMenu()

def storedir():
    ### DOES NOT DELETE FILE AFTER ADDING IT TO MASTER. TO BE IMPLEMENTED###
    # scp -r -i ~/Downloads/KeyPair3.pem tenfile/ hadoop@ec2-52-87-191-193.compute-1.amazonaws.com:/home/hadoop/
    # ssh = subprocess.Popen(['scp', '-r', '-i', KEY_LOC, move_loc, REMOTE_ADDRESS + ':/home/hadoop/'],
    dirname = move_loc.split('/')[-1]
    ssh = subprocess.Popen(['scp', '-r', '-i', KEY_LOC, move_loc, REMOTE_ADDRESS + ':/home/hadoop/'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,)
    hd = subprocess.Popen(['ssh', '-i', KEY_LOC, REMOTE_ADDRESS, 'hdfs dfs -put ' + dirname + ' /'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    stdout, stderr = ssh.communicate()
    updateFiles()
    updateMenu()

def deletefile():
    # ssh -i ~/Downloads/KeyPair3.pem hadoop@ec2-52-87-191-193.compute-1.amazonaws.com "rm -f -r ~/test.txt"
    get_file = variable.get()
    # path = REMOTE_ADDRESS + ':/home/hadoop/' + get_file
    ssh = subprocess.Popen(['ssh', '-i', KEY_LOC, REMOTE_ADDRESS, 'hdfs dfs -rm /' + get_file],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    stdout, stderr = ssh.communicate()
    updateFiles()
    updateMenu()


def deletedir():
    # ssh -i ~/Downloads/KeyPair3.pem hadoop@ec2-52-87-191-193.compute-1.amazonaws.com "rm -f -r ~/test"
    get_file = variable.get()
    # path = REMOTE_ADDRESS + ':/home/hadoop/' + get_file
    ssh = subprocess.Popen(['ssh', '-i', KEY_LOC, REMOTE_ADDRESS, 'hdfs dfs -rm -r /' + get_file + '/'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    stdout, stderr = ssh.communicate()
    updateFiles()
    updateMenu()


def retrievefile():
    ### DOES NOT DELETE FILE AFTER ADDING IT TO MASTER. TO BE IMPLEMENTED###
    # scp -i ~/Downloads/KeyPair3.pem hadoop@ec2-52-87-191-193.compute-1.amazonaws.com:/home/hadoop/test.txt ./
    get_file = variable.get()
    mfile = subprocess.run(['ssh', '-i', KEY_LOC, REMOTE_ADDRESS, 'hdfs dfs -copyToLocal /' + get_file, '/home/hadoop/'])
    path = REMOTE_ADDRESS + ':/home/hadoop/' + get_file
    ssh = subprocess.Popen(['scp', '-i', KEY_LOC, path, './'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    stdout, stderr = ssh.communicate()

def retrievedir():
    ### DOES NOT DELETE FILE AFTER ADDING IT TO MASTER. TO BE IMPLEMENTED###
    # scp -r -i ~/Downloads/KeyPair3.pem hadoop@ec2-52-87-191-193.compute-1.amazonaws.com:/home/hadoop/test ./
    get_file = variable.get()
    mdir = subprocess.run(['ssh', '-i', KEY_LOC, REMOTE_ADDRESS, 'hdfs dfs -copyToLocal /' + get_file, '/home/hadoop/'])
    path = REMOTE_ADDRESS + ':/home/hadoop/' + get_file
    ssh = subprocess.Popen(['scp', '-r', '-i', KEY_LOC, path, './'],
                     stdin =subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True,)
    stdout, stderr = ssh.communicate()

def updateMenu():
        menu = file_menu["menu"]
        menu.delete(0, "end")
        for string in remote_files:
            menu.add_command(label=string, 
                             command=lambda value=string: variable.set(value))

updateFiles()
window = Tk.Tk()
window.title('File Explorer')
window.geometry("500x500")
window.config(background="white")

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
button_explore_file = Tk.Button(window,
                        text = "Choose File",
                        command = browseFiles)
button_store_file = Tk.Button(window,
                     text = "Store File",
                     command = storefile)
button_retrieve_file = Tk.Button(window,
                     text = "Retrieve File",
                     command = retrievefile)
button_delete_file = Tk.Button(window,
                     text = "Delete File",
                     command = deletefile)
button_dir = Tk.Button(window,
                        text = "Choose Directory",
                        command = browseDir)
button_store_dir = Tk.Button(window,
                     text = "Store Dir",
                     command = storedir)
button_retrieve_dir = Tk.Button(window,
                     text = "Retrieve Dir",
                     command = retrievedir)
button_delete_dir = Tk.Button(window,
                     text = "Delete Dir",
                     command = deletedir)


variable = Tk.StringVar(window)
variable.set(remote_files[0])
file_menu = Tk.OptionMenu(window, variable,*remote_files)
label_file_explorer.grid(column = 1, row = 1)
button_explore_file.grid(column = 1, row = 2)
button_store_file.grid(column=1,row=3)
file_menu.grid(column=1,row=4)
button_retrieve_file.grid(column=1,row=5)
button_delete_file.grid(column=1,row=6)

button_dir.grid(column=1,row=7)
button_store_dir.grid(column=1,row=8)
button_retrieve_dir.grid(column=1,row=9)
button_delete_dir.grid(column=1,row=10)
label_dir_explorer.grid(column = 1, row=11)

button_exit.grid(column = 1,row = 12)

window.mainloop()