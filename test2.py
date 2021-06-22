from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import gui_background
import os
import glob

root = Tk()
root.title("Digital Attendence")

my_img = ImageTk.PhotoImage(Image.open("lol.png").resize((700, 150), Image.ANTIALIAS))

mystring = tk.StringVar(root)
root.iconbitmap("ed2.ico")

xl_name = ''


def create_attendance_sheet():
    folder_path = filedialog.askdirectory(initialdir="./", title="Select a folder")
    file_name = simpledialog.askstring("File name", "Enter the file name:")

    if folder_path != '' and file_name is None:
        messagebox.showinfo("Attendance Sheet Creation", "Attendance Sheet Created")
    elif folder_path != '' and file_name is not None:
        messagebox.showinfo("Attendance Sheet Creation", "{} created at {}".format(file_name, folder_path))
    else:
        messagebox.showinfo("Attendance Sheet Creation", "Attendance Sheet Created")


# print(mystring.get())


def open():
    return


def percentage_sheet():
    root.filename = filedialog.askopenfilename(initialdir="Attendance",
                                               title="Selece a file to calculate percentage from")
    if root.filename == '':
        messagebox.showinfo("File", "No file chosen")
        return
    file_to_calc_percentage_from = root.filename
    gui_background.percentage_works(file_to_calc_percentage_from)
    messagebox.showinfo("Percentage Update", "Attendance Percentage Updated")
    files = glob.glob(r'Attendance/Attendance Percentage' + "/*xlsx")
    max_file = max(files, key=os.path.getctime)
    os.startfile(max_file)

def show_attendance():
    root.filename = filedialog.askopenfilename(initialdir="Attendance", title="Select a file")
    if root.filename != '':
        path = root.filename
        os.startfile(path)
    else:
        messagebox.showinfo("No file", "No file chosen")


def new_win():
    global xl_name
    new_window = Toplevel(root)
    new_window.geometry("400x250")
    new_window.title("Attendance")
    new_window.iconbitmap("ed1.ico")
    new_window.resizable(False, False)
    # xl_name = Entry(new_window, width=40, textvariable=mystring).pack()
    btn5 = Button(new_window, text="Create new sheet", image=cm, width=150, height=20, compound='c',
                  activebackground="lightgreen", font=('Impact', 12), fg="red",
                  command=create_attendance_sheet).pack(pady=2)
    btn6 = Button(new_window, text="Show Attendance", image=cm, width=150, height=20, compound='c', activebackground="red",
                  font=('Impact', 12), fg="red", command=show_attendance).pack(padx=10, pady=20)
    btn7 = Button(new_window, text="Percentage", image=cm, width=150, height=20, compound='c', activebackground="red",
                  font=('Impact', 12), fg="red", command=percentage_sheet).pack(padx=10, pady=20)
    btn8 = Button(new_window, text="Back", image=cm, width=150, height=20, compound='c', activebackground="red",
                  font=('Impact', 12), fg="red", command=lambda: new_window.destroy()).pack(padx=10, pady=20)
    


def image_select():
    root.filename = filedialog.askopenfilename(initialdir="./Predict Images", title="Select an Image")
    image_file_path = root.filename
    root.filename = filedialog.askopenfilename(initialdir="./Attendance", title="Select an Attendance Sheet")
    attendance_file_path = root.filename

    if image_file_path == '':
        messagebox.showerror("Image File", "No image chosen! Chose an image to identify students.")
    elif attendance_file_path == '':
        messagebox.showerror("Attendance Sheet", "No attendance sheet chosen! Choose an attendance sheet to update "
                                                 "attendance.")
    elif (image_file_path != '') and (attendance_file_path != ''):
        gui_background.classify_image(image_file_path, attendance_file_path)
        messagebox.showinfo("Processing Complete", "Image processing complete! Attendance updated.")


def live_demo():
    gui_background.classify_video()


def result():
    # Open csv from here
    # root.filename=filedialog.askopenfilename(initialdir="C:/Users/FeaRleSS/Pictures",title="Select an Image")
    return


f = LabelFrame(root, padx=50, pady=50)
asd = Label(f, image=my_img, padx=1000, pady=150)
asd.grid(row=0, column=0, columnspan=2)
cm = PhotoImage(width=1, height=1)

btn1 = Button(f, text="Select Image", image=cm, width=250, height=30, compound='c', activebackground="lightgreen",
              font=('Impact', 12), fg="red", command=image_select).grid(row=1, column=0)
btn2 = Button(f, text="Live Camera", image=cm, width=250, height=30, compound='c', activebackground="lightgreen",
              font=('Impact', 12), fg="red", command=live_demo).grid(row=1, column=1)
btn3 = Button(f, text="Attendance", image=cm, width=250, height=30, compound='c', activebackground="lightgreen",
              font=('Impact', 12), fg="red", command=new_win).grid(row=2, column=0)
btn4 = Button(f, text="Exit", image=cm, width=250, height=30, compound='c', activebackground="red", font=('Impact', 12),
              fg="red", command=root.quit).grid(row=2, column=1)
f.pack()
root.resizable(False, False)

root.mainloop()
