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
        messagebox.showerror(title=mytitle, message=mymessage, parent=root)
    def confirm_dialog(self, string):
        return messagebox.askyesno(title="Are you sure?", message=string, parent=root)
    
RFM = RealFileManager() # for reference

### TODO: bundle error handling? ###

# functions for buttons
def create_me():
    # prompt file or directory
    wants_file = messagebox.askyesnocancel(title="Create what?", message="Do you want to create a file? (Choose 'No' to create a directory.)", parent=root)
    # handle cancel
    if wants_file is None: return
    # elif file, prompt filename, content
    if wants_file:
        # ask for filename
        name = simpledialog.askstring(title="New File Name", prompt="Enter a name for your new file. (Include the file extension.)", parent=root)
        if name is None or name == "": return # handle sad sequence
        my_path = os.path.join(os.getcwd(), name) # desired file path
        my_content = simpledialog.askstring(title="New file content", prompt="Enter content for your new file.", parent=root)
        RFM.create_file(path=my_path, content=my_content)
        messagebox.showinfo(title="Operation Complete", message=f"File {name} created.", parent=root)
    # else: directory, prompt name
    else:
        name = simpledialog.askstring(title="New Directory Name", prompt="Enter a name for your new directory.", parent=root)
        if name is None: return # sad sequence
        try:
            os.mkdir(name) # nowhere else needs safe_mkdir, so I think this is okay?
            RFM.update_display()
            messagebox.showinfo(title="Operation Complete", message=f"Directory {name} created.", parent=root)
        except PermissionError:
            messagebox.showerror(title="Permission Error", message="Cannot create directory in this location. Access is denied.", parent=root)
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e), parent=root)

def read_me():
    # prompt filename
    filename = simpledialog.askstring(title="Read File", prompt="Enter a file name to read.", parent=root)
    if filename is None or filename == "": return # handle cancel
    try:
        # open new window with label for file contents
        read_window = Toplevel(root)
        read_window.title(filename)
        read_window.geometry("800x600")

        # add text field and scrollbars
        text = Text(read_window, height=500, width=600)
        ys = ttk.Scrollbar(read_window, orient="vertical", command=text.yview)
        xs = ttk.Scrollbar(read_window, orient="horizontal", command=text.xview)
        text["yscrollcommand"] = ys.set; text["xscrollcommand"] = xs.set
        text.grid(column=0, row=0, sticky=NSEW)
        xs.grid(column=0, row=1, sticky=EW)
        ys.grid(column=1, row=0, sticky=NS)
        read_window.grid_columnconfigure(0, weight=1)
        read_window.grid_rowconfigure(0, weight=1)

        # read file
        with open(filename, "r") as f:
            text.insert("1.0", f.read())
        text.configure(state="disabled") # prevent editing of text field
    except PermissionError:
        messagebox.showerror(title="Permission Error", message="Cannot read this file. Access is denied.", parent=root)
        read_window.destroy()
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e), parent=root)
        read_window.destroy()

def update_me(): # variation on read_me()
    # prompt filename
    filename = simpledialog.askstring(title="Update File", prompt="Enter a file name to update. (Don't forget the extension.)", parent=root)
    if filename is None or filename == "": return # handle cancel
    try:
        # open new window with label for file contents
        read_window = Toplevel(root)
        read_window.title(filename)
        read_window.geometry("800x600")

        # add text field and scrollbars
        text = Text(read_window, height=500, width=600)
        ys = ttk.Scrollbar(read_window, orient="vertical", command=text.yview)
        xs = ttk.Scrollbar(read_window, orient="horizontal", command=text.xview)
        text["yscrollcommand"] = ys.set; text["xscrollcommand"] = xs.set
        text.grid(column=0, row=0, sticky=NSEW)
        xs.grid(column=0, row=1, sticky=EW)
        ys.grid(column=1, row=0, sticky=NS)
        read_window.grid_columnconfigure(0, weight=1)
        read_window.grid_rowconfigure(0, weight=1)

        # local save and exit function
        def save_and_exit():
            with open(filename, "w") as f:
                my_text = text.get("1.0", "end-1c")
                f.write(my_text)
            read_window.destroy()
            messagebox.showinfo(title="Save successful", message="Save completed successfully.", parent=root)

        # add save button
        save_button = ttk.Button(read_window, text="Save changes and exit", command=save_and_exit)
        save_button.grid(column=0, row=2, pady=10)

        # read file
        with open(filename, "r") as f:
            text.insert("1.0", f.read())

    except PermissionError:
        messagebox.showerror(title="Permission Error", message="Cannot read this file. Access is denied.", parent=root)
        read_window.destroy()
    except Exception as e:
        messagebox.showerror(title="Error", message=str(e), parent=root)
        read_window.destroy()

def delete_me():
    # prompt name
    # check if file or directory
    # process delete by case
    pass
def rename_me():
    # prompt name
    # determine if file or directory
    # prompt new name
    # change
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