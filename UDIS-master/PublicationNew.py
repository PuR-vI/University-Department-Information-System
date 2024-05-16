from tkinter import *
import DepartmentPublication
import sqlite3
from tkinter import messagebox
import ES
from PIL import Image, ImageTk

class PublicationNew:
    def __init__(self, root):
        root.title("Add Publications")
        root.geometry('400x400')
        root.minsize(400, 400)
        root.maxsize(400, 400)

        self.frame = Frame(root)
        self.frame.grid(row=0, column=0, sticky='nsew')

         # Load the image
        image = Image.open("leaves.jpg")
        # Resize the image to fit the window size
        image = image.resize((800, 600))
        photo = ImageTk.PhotoImage(image)

        # Create a label with the image
        bg_label = Label(root, image=photo)
        bg_label.image = photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

        # Create a frame for other widgets
        self.frame = Frame(root, bg='#D1D5D8')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Change font size and type
        font_style = ("Helevatica", 14)


        Label(self.frame, text='Author').grid(row=0, column=0)
        Label(self.frame, text='Name').grid(row=1, column=0)
        Label(self.frame, text='Date').grid(row=2, column=0)

        self.nameEntry = Entry(self.frame, borderwidth=1)
        self.authorEntry = Entry(self.frame, borderwidth=1)
        self.dateEntry = Entry(self.frame, borderwidth=1)

        self.nameEntry.grid(row=1, column=1)
        self.authorEntry.grid(row=0, column=1)
        self.dateEntry.grid(row=2, column=1)

        Button(self.frame, text='Submit', command=lambda:self.submit(root)).grid(row=5, column=0, columnspan=2)
        Button(self.frame, text='Exit', command=exit).grid(row=6, column=1)
        Button(self.frame, text='Back', command=lambda:self.back(root)).grid(row=6, column=0)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        root.mainloop()

    def submit(self, root):
        name_ = self.nameEntry.get()
        author_ = self.authorEntry.get()
        date_ = self.dateEntry.get()
        try:
            PublicationNew.addpublication(name_, author_, date_)
            messagebox.showinfo('Publication', name_ + ' added successfully')
            self.clear()
            DepartmentPublication.DepartmentPublication(root)
        except Exception as e:
            messagebox.showwarning('Publication', e)

    @staticmethod
    def addpublication(name_, author_, date_):

        lengths = [len(i) for i in [name_, author_, date_]]
        if 0 in lengths:
            raise Exception('One or more fields left blank')

        connect_, cursor_ = ES.get_student_db_ES()

        cursor_.execute('SELECT * FROM publications WHERE pub_name=(:name)', {'name': name_})
        results = cursor_.fetchall()
        if results:
            raise Exception('A publication with the same name already exists')

        with connect_:
            cursor_.execute('INSERT INTO publications VALUES (:author, :name, :date)',
                                {'author': author_, 'name': name_, 'date': date_})

    def back(self, root):
        self.clear()
        DepartmentPublication.DepartmentPublication(root)

    def clear(self):
        self.frame.destroy()