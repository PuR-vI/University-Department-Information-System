from tkinter import *
from tkinter import ttk
import ES
import Home
import DepartmentUDIS
import DepartmentCourses
import DepartmentProject
import DepartmentPublication
from PIL import Image, ImageTk

global root_

class DepartmentAcademic:
    def __init__(self, root):
        root.title("Department - Academics")
        root.geometry('800x600')
        root.minsize(800, 600)
        root.maxsize(800, 600)

        # Only for unit testing
        #
        # root.minsize(400, 300)
        # root.maxsize(800, 600)
        # root.geometry('800x600')

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

        self.projectButton = Button(self.frame,font='font_style', text="Research Projects",anchor=W,
                                                 command = lambda: self.project(root),height=3, width=20)

        self.publicationsButton = Button(self.frame,font='font_style', text="Research Publications",anchor=W,
                                                 command= lambda: self.publications(root),height=3, width=20)

        self.coursesButton = Button(self.frame,font='font_style', text="Courses Offered",anchor=W,
                                                 command=lambda: self.courses(root),height=3, width=20)

        self.exitButton = Button(self.frame,font='font_style', text="Exit", command=exit,bg='Red',fg='white',height=2, width=10)
        self.backButton = Button(self.frame,font='font_style', text="Back", command=lambda:self.back(root),bg='#3B82DB',fg='white',height=2, width=10)

        self.projectButton.grid(row=0, column=0, columnspan=2,sticky=E+W)
        self.publicationsButton.grid(row=1, column=0, columnspan=2,sticky=E+W)
        self.coursesButton.grid(row=2, column=0, columnspan=2,sticky=E+W)

        self.exitButton.grid(row=4, column=0,pady=10,sticky=S)
        self.backButton.grid(row=4, column=1,pady=10,sticky=S)
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)

        # root.mainloop()

    def back(self,root):
        self.clear()
        DepartmentUDIS.DepartmentMainMenu(root)

    def project(self, root):
        self.clear()
        DepartmentProject.DepartmentProject(root)

    def publications(self, root):
        self.clear()
        DepartmentPublication.DepartmentPublication(root)

    def courses(self, root):
        self.clear()
        DepartmentCourses.DepartmentCourses(root)

    def clear(self):
        self.frame.destroy()

if __name__ == '__main__':
    root = Tk()
    DepartmentAcademic(root)