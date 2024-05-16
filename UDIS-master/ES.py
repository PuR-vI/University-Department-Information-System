from tkinter import *
from tkinter import messagebox
# import StudentsUDIS
import Home
import sqlite3
from PIL import Image, ImageTk

def get_student_db_ES():
    connect_ = sqlite3.connect('Backend/UDIS.db')
    cursor_ = connect_.cursor()
    return connect_, cursor_

class ES:
    def __init__(self, root):

        root.title("UDIS")

        self.frame = Frame(root, bg="black")
        self.frame.grid(row=0, column=0, sticky='nsew')

         # Load the image
        image = Image.open("login.jpg")
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

        # Change font size and type
        font_style = ("Helvetica", 12)

        Label(self.frame, text="Enter Credentials", fg="black", bg='#D1D5D8', font=("Helvetica", 16, "bold")).grid(row=0, columnspan=2, pady=10)
        self.idLabel = Label(self.frame, text="User ID", bg='#D1D5D8', fg='black', font=font_style)
        self.idLabel.grid(row=1, column=0)
        self.idEntry = Entry(self.frame, font=font_style)
        self.idEntry.grid(row=1, column=1)
        self.pwLabel = Label(self.frame, text="Password", fg='black', bg='#D1D5D8', font=font_style)
        self.pwLabel.grid(row=2, column=0)
        self.pwEntry = Entry(self.frame, show="*", font=font_style)
        self.pwEntry.grid(row=2, column=1)

        # Make the button green
        self.submitButton =Button(self.frame, text="Login",bg='Green',fg='White', command=lambda: self.login(root))
        self.submitButton.grid(row=3, columnspan=2, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=1)

    @staticmethod
    def authenticate(id_ip,pw_ip):
        connect_,cursor_ = get_student_db_ES()
        cursor_.execute('SELECT * FROM authentication')
        data=cursor_.fetchone()
        if id_ip==data[0] and pw_ip==data[1]:
            return True
        else:
            return False

    def login(self,root):
        id_ip = self.idEntry.get()
        pw_ip = self.pwEntry.get()
        if ES.authenticate(id_ip,pw_ip):
            self.clear()
            Home.Home(root)
        else:
            messagebox.showerror("Failed Login", "Invalid Credentials")
        
    def clear(self):
        self.frame.destroy()

    @staticmethod
    def test():
        print("\nTesting the ES class")
        success = 0
        fail = 0
        print("\ta. Correct user ID correct password:")
        if ES.authenticate("admin","password")==True:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1

        print("\tb. Correct user ID wrong password:")
        if ES.authenticate("admin","passwor")==False:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL")
            fail=fail+1
        
        print("\tc. Wrong user ID correct password:")
        if ES.authenticate("ain","password")==False:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL")
            fail=fail+1
        
        print("\ta. Wrong user ID wrong password:")
        if ES.authenticate("adin","psword")==False:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL")
            fail=fail+1
        
        print(f'Test cases passed {success}/{success+fail}')
        print(f'Percentage = {(success/(success+fail))*100}')



if __name__ == '__main__':
    root = Tk()

    a = ES(root)
    del a
