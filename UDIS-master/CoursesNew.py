from tkinter import *
import DepartmentCourses
import Home
import tkinter.ttk as ttk
import ES
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk

def dropdown_defocus_CoursesNew(event):
    event.widget.selection_clear()
import ScrollableFrame

class CoursesNew:
    def __init__(self, root):
               
        self.parent = Frame(root)
        self.parent.grid(row=0, column=0, sticky='nsew')
       
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

        self.rightpad = Frame(self.parent, bg="white")
        self.leftpad = Frame(self.parent, bg="white")
        self.bottomholder=Frame(self.parent, bg="white")
        self.frame = Frame(self.parent,bg="white")

        self.rightpad.grid(row=0,column=0,sticky='nsew',rowspan=2)
        self.leftpad.grid(row=0,column=2,sticky='nsew',rowspan=2)
        self.bottomholder.grid(row=1,column=1,columnspan=3,sticky='nsew')
        self.frame.grid(row=0, column=1, sticky='nsew')
        
        self.parent.rowconfigure(0,weight=1)
        self.parent.columnconfigure(0,weight=1)
        self.parent.columnconfigure(2,weight=1)

        root.geometry('400x400')
        root.minsize(400, 400)
        root.maxsize(400, 400)

        self.coursecodeLabel = Label(self.frame, text='Course Code',bg="white",fg="black")
        self.coursecodeEntry = Entry(self.frame, borderwidth=0)
        
        self.coursenameLabel = Label(self.frame, text='Course Name',bg="white",fg="black")
        self.coursenameEntry = Entry(self.frame, borderwidth=0)
        
        self.creditLabel=Label(self.frame, text='Number of credits',bg="white",fg="black")
        self.creditEntry=Entry(self.frame, borderwidth=0)
        
        self.professornameLabel = Label(self.frame, text='Professor name',bg="white",fg="black")
        self.professornameEntry = Entry(self.frame, borderwidth=0)

        self.submitButton = Button(self.frame, text='Submit', command=lambda: self.submit(root))
        self.exitButton = Button(self.frame, text="Exit", command=exit)
        self.backButton = Button(self.frame, text="Back",
                                                  command=lambda: self.back(root))

        self.coursecodeLabel.grid(row=2, column=0,sticky=E+S,padx=5,pady=3,)
        self.coursecodeEntry.grid(row=2, column=1, sticky=W+S+E)
        self.coursenameLabel.grid(row=3, column=0,sticky=E,padx=5,pady=3)
        self.coursenameEntry.grid(row=3, column=1, sticky=W+E)
    
        self.professornameLabel.grid(row=4,column=0,sticky=E,padx=5,pady=3)
        self.professornameEntry.grid(row=4,column=1,sticky=W+E)
        self.creditLabel.grid(row=5,column=0,sticky=E,padx=5,pady=3)
        self.creditEntry.grid(row=5,column=1,sticky=W+E)

        self.submitButton.grid(row=7, column=0, columnspan=2,pady=20)

        self.exitButton.grid(row=8, column=0, pady=10, sticky=S+W)
        self.backButton.grid(row=8, column=1, pady=10, sticky=S+E)

        self.frame.rowconfigure(2,weight=1)
        self.frame.rowconfigure(8,weight=1)
        self.frame.rowconfigure(4, weight=0)
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        
        root.mainloop()

    def back(self, root):
        self.clear()
        root.maxsize(800, 600)
        DepartmentCourses.DepartmentCourses(root)

    def submit(self, root):
        coursecode_ = self.coursecodeEntry.get()
        coursename_ = self.coursenameEntry.get()
        professorname_ = self.professornameEntry.get()
        credits_ = self.creditEntry.get()
        try:
            CoursesNew.addcourse(coursecode_, coursename_, professorname_, credits_)
            messagebox.showinfo('Course', coursename_ + ' added Successfully')
            self.clear()
            DepartmentCourses.DepartmentCourses(root)
        except Exception as e:
            messagebox.showwarning('Adding Course', e)

    @staticmethod
    def addcourse(coursecode_, coursename_, professorname_, credits_):
        lengths = [len(i) for i in [coursecode_, coursename_, professorname_, credits_]]
        if 0 in lengths:
            raise Exception('One or more fields left blank')

        connect_, cursor_ = ES.get_student_db_ES()

        cursor_.execute('SELECT * from all_courses WHERE sub_code=(:code)', {'code': coursecode_})
        results = cursor_.fetchall()
        if results:
            raise Exception('A Course with the same Code already exists.')
        try:
            credits_ = int(credits_)
        except Exception:
            raise Exception('Credits is not an integer')
        if credits_ < 0 or credits_ > 5:
            raise Exception('Credits can only be between 1 and 5.')

        with connect_:
            cursor_.execute("INSERT INTO all_courses VALUES (:sub_code, :course_name,:prof_name,:credits)",
                            {'sub_code': coursecode_, 'course_name': coursename_, 'prof_name': professorname_,
                             'credits': credits_})

    def clear(self):
        self.parent.destroy()

