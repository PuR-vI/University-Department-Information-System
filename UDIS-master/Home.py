from tkinter import *
from tkinter import ttk
import ES
import StudentMain
import DepartmentUDIS
from PIL import Image, ImageTk

class Home:
    def __init__(self, root):

        root.title("UDIS - Homepage")
        
        self.frame = Frame(root, bg="black")
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
        font_style = ("Helvetica", 12)

        Label(self.frame, text="Welcome to UDIS", fg="black", bg='#D1D5D8', font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)

        student_image = Image.open("student_icon.jpg")
        student_image = student_image.resize((150, 150))
        student_photo = ImageTk.PhotoImage(student_image)

        self.studentButton = ttk.Button(self.frame, text='Student', compound=TOP, image=student_photo, command=lambda: self.student(root))
        self.studentButton.image = student_photo
        self.studentButton.grid(row=1, column=0, padx=10, pady=10)

        dept_image = Image.open("dept_icon.jpg")
        dept_image = dept_image.resize((150, 150))
        dept_photo = ImageTk.PhotoImage(dept_image)

        self.departmentButton = ttk.Button(self.frame, text='Department', compound=TOP, image=dept_photo, command=lambda: self.department(root))
        self.departmentButton.image = dept_photo
        self.departmentButton.grid(row=1, column=1, padx=10, pady=10)

        self.exitButton =Button(self.frame, text="Exit",bg='Red',fg='White', command=root.quit)
        self.exitButton.grid(row=2, column=0, padx=10, pady=10)

        self.signOutButton =Button(self.frame, text="Sign Out", bg='Brown',fg='White', command=lambda: self.sign_out(root))
        self.signOutButton.grid(row=2, column=1, padx=10, pady=10)

        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def student(self, root):
        self.clear()
        StudentMain.StudentMain(root)

    def department(self, root):
        self.clear()
        DepartmentUDIS.DepartmentMainMenu(root)

    def back(self, root):
        self.clear()
        ES.ES(root)

    def clear(self):
        self.frame.destroy()

if __name__ == '__main__':
    root = Tk()
    Home(root)
