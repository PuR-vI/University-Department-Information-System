from tkinter import *
import ES
from tkinter import messagebox
import StudentMain
from ScrollableFrame import ScrollableFrame

class StudentSearch:
    def __init__(self, root):
        self.frame = Frame(root)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.nameLabel = Label(self.frame, text='Name', fg="black")
        self.nameEntry = Entry(self.frame, borderwidth=0)
        self.rollLabel = Label(self.frame, text='Roll No', fg="black")
        self.rollEntry = Entry(self.frame, borderwidth=0)

        self.searchButton = Button(self.frame, text='Search', command=lambda:self.search(root))
        self.searchResults = ScrollableFrame(self.frame)

        self.nameLabel.grid(row=2, column=0, padx=5, pady=3)
        self.nameEntry.grid(row=2, column=1)
        self.rollLabel.grid(row=3, column=0, padx=5, pady=3)
        self.rollEntry.grid(row=3, column=1)

        self.exitButton = Button(self.frame, text="Exit", command=exit)
        self.backButton = Button(self.frame, text="Back", command=lambda: self.back(root))

        self.searchButton.grid(row=4, column=0,columnspan=2,pady=20)
        self.searchResults.grid(row=5, column=0,padx=30, sticky="nsew",columnspan=2)

        self.exitButton.grid(row=8, column=0, padx=50, pady=50, sticky=S + W)
        self.backButton.grid(row=8, column=1, padx=50, pady=50, sticky=S + E)

        self.frame.rowconfigure(8, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        root.mainloop()

    def bindingAction(self, event):
        pass

    def display(self, root, list_):
        self.searchResults.destroy()
        self.searchResults = ScrollableFrame(self.frame)
        self.searchResults.grid(row=5, column=0,padx=30, sticky="nsew", columnspan = 2)
        self.searchResults.frame.columnconfigure(1,weight=1)

        for i in range(len(list_)):
            studentSerial = Label(self.searchResults.frame, anchor=W, text=i+1)
            studentRollAndName = Label(self.searchResults.frame, anchor=W, text=list_[i][0] + '    ' + list_[i][1])
            studentSerial.grid(row=i, column=0, sticky=W+E,padx=5)
            studentRollAndName.grid(row=i, column=1, sticky=W+E)
            studentRollAndName.bind('<Button-1>', self.bindingAction)

    def back(self, root):
        pass

    def search(self, root):
        connect_, cursor_ = ES.get_student_db_ES()
        name_ = self.nameEntry.get()
        roll_no_ = self.rollEntry.get()
        if name_ == "" and roll_no_ == "":
            cursor_.execute("SELECT * FROM student")
        elif roll_no_ == "":
            cursor_.execute("SELECT * FROM student WHERE student_name LIKE (:name)",{'name':'%'+name_+'%'})
        elif name_ == "":
            cursor_.execute("SELECT * FROM student WHERE roll LIKE (:roll)", {'roll':'%'+roll_no_+'%'})
        else:
            cursor_.execute("SELECT * FROM student WHERE student_name LIKE (:name) AND roll LIKE (:roll)", {'name':'%'+name_+'%', 'roll':'%'+roll_no_+'%'})
        self.display(root, cursor_.fetchall())

    def clear(self):
        self.frame.destroy()


if __name__ == '__main__':
    root = Tk()
    root.minsize(400, 300)
    root.maxsize(800, 600)
    root.geometry('800x600')
    StudentSearch(root)
