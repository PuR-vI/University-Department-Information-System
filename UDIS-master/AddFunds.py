import DepartmentAccount
import ES
from tkinter import *
from tkinter import messagebox
import datetime
from PIL import Image, ImageTk

class AddFunds:
    def __init__(self, root):
        root.title('Add Funds')
        root.geometry('600x600')  # Increase window size

        # Load the image
        image = Image.open("add_funds.jpg")
        # Resize the image to fit the window size
        image = image.resize((600, 600))
        photo = ImageTk.PhotoImage(image)

        # Create a label with the image
        bg_label = Label(root, image=photo)
        bg_label.image = photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

        # Create a frame for other widgets
        self.frame = Frame(root, bg='#D1D5D8')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text="New Entry", fg="black", bg='#D1D5D8', font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)
        Label(self.frame, text="Donor", anchor='w', fg="black",bg='#D1D5D8',font=("Helvetica", 12)).grid(row=1, column=0)
        Label(self.frame, text='Amount', anchor='w', fg="black",bg='#D1D5D8', font=("Helvetica", 12)).grid(row=2, column=0)
        Label(self.frame, text='Date', anchor='w', fg="black",bg='#D1D5D8', font=("Helvetica", 12)).grid(row=3, column=0)
        Label(self.frame, text='Purpose', anchor='w', fg="black",bg='#D1D5D8', font=("Helvetica", 12)).grid(row=4, column=0)

        self.donorEntry = Entry(self.frame, bg="white", fg="black",width=30)  # Changed foreground and background colors
        self.amountEntry = Entry(self.frame, bg="white", fg="black",width=30)  # Changed foreground and background colors
        self.dateEntry = Entry(self.frame, bg="white", fg="black",width=30)  # Changed foreground and background colors
        self.purposeEntry = Entry(self.frame, bg="white", fg="black",width=30)  # Changed foreground and background colors


        self.donorEntry = Entry(self.frame)
        self.amountEntry = Entry(self.frame)
        self.dateEntry = Entry(self.frame)
        self.purposeEntry = Entry(self.frame)

        self.donorEntry.grid(row=1, column=1)
        self.amountEntry.grid(row=2, column=1)
        self.dateEntry.grid(row=3, column=1)
        self.purposeEntry.grid(row=4, column=1)

        self.submitButton = Button(self.frame, text='Add Funds', anchor=W, command=lambda: self.submit(root), bg="green", fg="white", font=("Helvetica", 12))
        self.backButton = Button(self.frame, text='Back', command=lambda: self.back(root), bg="teal", fg="white", font=("Helvetica", 12))
        self.exitButton = Button(self.frame, text='Exit', command=exit, bg="brown", fg="white", font=("Helvetica", 12))


        self.submitButton.grid(row=5, columnspan=2, pady=50)

        self.exitButton.grid(row=7, column=0, sticky=N + W, padx=50, pady=50)
        self.backButton.grid(row=7, column=1, sticky=N + E, padx=50, pady=50)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        root.mainloop()

    def submit(self, root):
        donor_ = self.donorEntry.get()
        amount_ = self.amountEntry.get()
        date_ = self.dateEntry.get()
        purpose_ = self.purposeEntry.get()
        try:
            AddFunds.addfunds(donor_, amount_, date_, purpose_)
            messagebox.showinfo('Funds', 'Added successfully')
            self.clear()
            DepartmentAccount.DepartmentAccount(root)
        except Exception as e:
            messagebox.showwarning('Adding Funds', e)

    @staticmethod
    def addfunds(donor_, amount_, date_, purpose_):
        lengths = [len(i) for i in [donor_, amount_, date_, purpose_]]
        if 0 in lengths:
            raise Exception('One or more fields left blank')

        connect_, cursor_ = ES.get_student_db_ES()
        try:
            amount_ = int(amount_)
        except ValueError:
            raise Exception('Amount is not a valid number')
        if not amount_ > 0:
            raise Exception('Amount is not a positive number')

        try:
            datetime.datetime.strptime(date_, '%d/%m/%Y')
        except ValueError:
            raise Exception('Incorrect Date Format')

        with connect_:
            cursor_.execute('INSERT INTO transactions VALUES (:donor, :amount, :date, :purpose)',
                            {'donor': donor_, 'amount': amount_, 'date': date_, 'purpose': purpose_})

            cursor_.execute('SELECT * from total')
            amount = (cursor_.fetchone())[0]
            cursor_.execute('UPDATE total SET amount=(:n_amt) WHERE amount=(:o_amt)',
                            {'n_amt': amount + amount_, 'o_amt': amount})

    def back(self, root):
        self.clear()
        DepartmentAccount.DepartmentAccount(root)

    def clear(self):
        self.frame.destroy()