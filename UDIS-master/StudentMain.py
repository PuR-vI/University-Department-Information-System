from tkinter import *
import ES
import Home
import StudentsNew
import StudentsView
import StudentCourses
import StudentGrades
from PIL import Image, ImageTk

class StudentMain:
    def __init__(self, root):
        root.title("UDIS - Student")
        # Only for unit testing
        #
        root.minsize(800, 600)
        root.maxsize(800, 600)
        root.geometry('800x600')

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

        self.newButton = Button(self.frame, text="Add New Student", anchor=W,
                                                 command=lambda: self.new(root),font='font_style',height=3, width=20)
        self.courseButton = Button(self.frame, text="Register Courses", anchor=W,
                                                 command=lambda: self.course(root),font='font_style',height=3, width=20)
        self.viewButton = Button(self.frame, text="View Student", anchor=W,
                                                  command=lambda: self.view(root),font='font_style',height=3, width=20)
        self.gradeButton = Button(self.frame, text="Enter Student Grades", anchor=W,
                                                   command=lambda: self.grades(root),font='font_style',height=3, width=20)
        self.exitButton = Button(self.frame, text="Exit", command=exit,font='font_style',height=2, width=10)
        self.backButton = Button(self.frame, text="Back", command=lambda: self.back(root),font='font_style',height=2, width=10)

        self.newButton.grid(row=0, column=0, columnspan=2, sticky=E + W)
        self.courseButton.grid(row=1, column=0, columnspan=2, sticky=E + W)
        self.viewButton.grid(row=2, column=0, columnspan=2, sticky=E + W)
        self.gradeButton.grid(row=3, column=0, columnspan=2, sticky=E + W)
        self.exitButton.grid(row=4, column=0, pady=10, sticky=S)
        self.backButton.grid(row=4, column=1, pady=10, sticky=S)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=1)

    def back(self, root):
        
        self.clear()
        Home.Home(root)

    def new(self, root):
        
        self.clear()
        StudentsNew.StudentNew(root)

    def view(self, root):
        
        self.clear()
        StudentsView.StudentsView(root)

    def course(self, root):
        self.clear()
        StudentCourses.StudentCourses(root)

    def clear(self):
        self.frame.destroy()

    def grades(self, root):
        self.clear()
        StudentGrades.StudentGrades(root)

if __name__ == '__main__':
    root = Tk()
    StudentMain(root)