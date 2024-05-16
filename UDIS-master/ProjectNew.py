from tkinter import *
import DepartmentProject
import sqlite3
from tkinter import messagebox
import ES
import datetime
from PIL import Image, ImageTk

class ProjectNew:
    def __init__(self, root):

        root.title("Add Project")
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


        Label(self.frame, text='Name').grid(row=0, column=0)
        Label(self.frame, text='Organisation').grid(row=1, column=0)
        Label(self.frame, text='Incharge').grid(row=2, column=0)
        Label(self.frame, text='Duration').grid(row=3, column=0)
        Label(self.frame, text='Fund Allocated').grid(row=4, column=0)
        Label(self.frame, text='Date of Sanction').grid(row=5, column=0)

        self.nameEntry = Entry(self.frame, borderwidth=1)
        self.orgEntry = Entry(self.frame, borderwidth=1)
        self.inchargeEntry = Entry(self.frame, borderwidth=1)
        self.durationEntry = Entry(self.frame, borderwidth=1)
        self.amountEntry = Entry(self.frame, borderwidth=1)
        self.dateEntry = Entry(self.frame, borderwidth=1)

        self.nameEntry.grid(row=0, column=1)
        self.orgEntry.grid(row=1, column=1)
        self.inchargeEntry.grid(row=2, column=1)
        self.durationEntry.grid(row=3, column=1)
        self.amountEntry.grid(row=4, column=1)
        self.dateEntry.grid(row=5, column=1)

        Button(self.frame, text='Submit', command=lambda:self.submit(root)).grid(row=7, column=0, columnspan=2)
        Button(self.frame, text='Exit', command=exit).grid(row=8, column=1)
        Button(self.frame, text='Back', command=lambda:self.back(root)).grid(row=8, column=0)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        root.mainloop()

    def submit(self, root):
        name_ = self.nameEntry.get()
        org_ = self.orgEntry.get()
        incharge_ = self.inchargeEntry.get()
        duration_ = self.durationEntry.get()
        amount_ = int(self.amountEntry.get())
        date_ = self.dateEntry.get()
        try:
            ProjectNew.addproject(name_, org_, incharge_, duration_, amount_, date_)
            messagebox.showinfo('Project', name_ + ' has been added.')
            self.clear()
            self.back(root)
        except Exception as e:
            messagebox.showwarning('Project', e)

    @staticmethod
    def addproject(name_, org_, incharge_, duration_, amount_, date_):
        connect_, cursor_ = ES.get_student_db_ES()
        lengths = [len(i) for i in [name_, org_, incharge_, duration_, date_]]
       
        if 0 in lengths:
            raise Exception('One or more of the fields are blank')
        try:
            amount_ = int(amount_)
        except ValueError:
            raise Exception('Amount is not a valid number')
        if amount_ <= 0:
            raise Exception('Amount should be a positive number')
        cursor_.execute('SELECT * FROM total')
        if amount_ > (cursor_.fetchone())[0]:
            raise Exception('Unsufficient Funds')
        cursor_.execute('SELECT * FROM projects WHERE name=(:name)', {'name': name_})
        results = cursor_.fetchall()
        if results:
            raise Exception('Project with the same name already exists')

        try:
            datetime.datetime.strptime(date_, '%d/%m/%Y')
        except Exception:
            raise Exception('Invalid Date')

        with connect_:
            cursor_.execute('INSERT INTO projects VALUES (:org, :inc, :dur, :status, :name)',
                                {'org': org_, 'inc': incharge_, 'dur': duration_, 'status': 'Ongoing', 'name': name_})
            cursor_.execute('INSERT INTO transactions VALUES (:donor, :amount, :date, :purpose)',
                                {'donor': org_, 'amount': -1 * amount_, 'date': date_, 'purpose': 'Project : ' + name_})
            if not amount_:
                return
            cursor_.execute('SELECT * from total')
            amount = (cursor_.fetchone())[0]
            cursor_.execute('UPDATE total SET amount=(:n_amt) WHERE amount=(:o_amt)',
                                {'n_amt': amount - amount_, 'o_amt': amount})

    def back(self, root):
        self.clear()
        DepartmentProject.DepartmentProject(root)

    def clear(self):
        self.frame.destroy()