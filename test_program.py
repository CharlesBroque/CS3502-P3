from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog
from functools import partial
import os
import shutil
import fileops

# fileops overrides
class RealFileManager(fileops.FileManager):
    def update_display(self):
        render_directory()
    def show_error(self, mymessage, mytitle="Error"):
        messagebox.showerror(title=mytitle, message=mymessage)
    def confirm_dialog(self, string):
        return messagebox.askyesno(title="Are you sure?", message=string)
    
RFM = RealFileManager() # for reference

# functions for buttons
def create_me():
    # prompt file or directory
    wants_file = messagebox.askyesnocancel(title="Create what?", message="Do you want to create a file? (Choose 'No' to create a directory.)")
    # sad path go away
    if wants_file == None: return
    # elif file, prompt filename, content
    if wants_file:
        name = simpledialog.askstring(title="New File Name", prompt="Enter a name for your new file. (Include the file extension.)")
        my_path = os.path.join(os.getcwd(), name)
        my_content = simpledialog.askstring(title="New file content", prompt="Enter content for your new file.")
        RFM.create_file(path=my_path, content=my_content)
    # else: directory, prompt name
    else:
        name = simpledialog.askstring(title="New Directory Name", prompt="Enter a name for your new directory.")
        try:
            os.mkdir(name) # nowhere else needs safe_mkdir, so I think this is okay?
        except PermissionError:
            messagebox.showerror(title="Permission Error", message="Cannot create directory in this location. Access is denied.")
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))

def read_me():
    # prompt filename
    # open window
    pass
def update_me():
    # prompt filename
    # prompt new content
    pass
def delete_me():
    # prompt file or directory
    pass
def rename_me():
    # prompt name
    # determine if file or directory
    pass
def navigate_me():
    path = simpledialog.askstring(title="Where to?", prompt="Enter the name of a directory.")
    safe_chdir(path)
    
def safe_chdir(path):
    if path == None or path == "": return
    if os.path.isdir(path):
        try:
            os.chdir(path)
        except PermissionError:
            messagebox.showerror(title="Permission error", message=f"Access to {path} is denied.")
        render_directory()
    else:
        messagebox.showerror(title="Path error", message=f"No such path {path}")

def render_directory():
    # clear current directory listing
    for w in dirnameFrame.winfo_children():
        w.destroy()
    
    # title current directory frame
    dirnameFrame.configure(text=os.getcwd())
    stuff_in_here = []
    try:
        stuff_in_here = os.listdir()
    except PermissionError: # weird
        messagebox.showerror(title="Permission Error", message=f"Access is denied: cannot list directories in {os.getcwd()}")

    # make buttons for folders and labels for files
    column_height = 20
    ttk.Button(dirnameFrame, text="..", command=partial(safe_chdir, "..")).grid(column=0, row=0)
    i = 1
    for entry in stuff_in_here:
        if os.path.isdir(entry):
            command_with_arg = partial(safe_chdir, entry)
            ttk.Button(dirnameFrame, text=entry, command=command_with_arg).grid(column=i//column_height, row=i%column_height)
        else:
            ttk.Label(dirnameFrame, text=entry).grid(column=i//column_height, row=i%column_height)
        i += 1


root = Tk()
root.title("File System Operations Project")
root.minsize(width=900, height=600)

# left frame
buttonFrame = ttk.Frame(root, width=200, height=600)
buttonFrame.grid(row=0, column=0, padx=10, pady=5)

## function buttons
ttk.Button(buttonFrame, text="Create", command=create_me).grid(column=0, row=10)
ttk.Button(buttonFrame, text="Read", command=read_me).grid(column=0, row=20)
ttk.Button(buttonFrame, text="Update", command=update_me).grid(column=0, row=30)
ttk.Button(buttonFrame, text="Delete", command=delete_me).grid(column=0, row=40)
ttk.Button(buttonFrame, text="Rename", command=rename_me).grid(column=0, row=50)
ttk.Button(buttonFrame, text="Navigate", command=navigate_me).grid(column=0, row=60)
ttk.Button(buttonFrame, text="Quit", command=root.destroy).grid(column=0, row=70)

# right frame
directoryFrame = ttk.Labelframe(root, text="Directory View", width=600, height=600)
directoryFrame.grid(row=0, column=1, padx=10, pady=5)

dirnameFrame = ttk.LabelFrame(directoryFrame, text=os.getcwd(), width=600, height=600)
dirnameFrame.grid(row=0, column=2, padx=10, pady=5)
dirListing = ttk.Label(dirnameFrame, text="")
dirListing.grid(row=0, column=3, padx=10, pady=5)
render_directory()



root.mainloop()