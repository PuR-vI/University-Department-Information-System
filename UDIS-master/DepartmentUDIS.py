from tkinter import *
from tkinter import ttk
import ES
import Home
import DepartmentAcademic
import DepartmentAccount
import DepartmentInventory
from PIL import Image, ImageTk

global root_

class DepartmentMainMenu:
    def __init__(self, root):
        root.title("UDIS - Department")
        root.geometry('800x600')
        root.minsize(800, 600)
        root.maxsize(800, 600)

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

        self.inventoryButton = Button(self.frame, text="Manage Inventory", anchor=W, font=font_style,
                                      command=lambda: self.inventory(root), height=3, width=20)

        self.academicsButton = Button(self.frame, text="Academic Section", anchor=W, font=font_style,
                                      command=lambda: self.academics(root), height=3, width=20)

        self.accountsButton = Button(self.frame, text="Account Details", anchor=W, font=font_style,
                                     command=lambda: self.accounts(root), height=3, width=20)

        self.exitButton = Button(self.frame,font='font_style', text="Exit", command=exit,bg='Red',fg='white',height=2, width=10)
        self.backButton = Button(self.frame,font='font_style', text="Back", command=lambda:self.back(root),bg='Cyan',fg='white',height=2, width=10)

        self.inventoryButton.grid(row=0, column=0, columnspan=2,sticky=E+W)
        self.academicsButton.grid(row=1, column=0, columnspan=2,sticky=E+W)
        self.accountsButton.grid(row=2, column=0, columnspan=2,sticky=E+W)

        self.exitButton.grid(row=3, column=0,pady=10,sticky=S)
        self.backButton.grid(row=3, column=1,pady=10,sticky=S)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)

        root.mainloop()

    def back(self,root):
        self.clear()
        Home.Home(root)

    def inventory(self, root):
        self.clear()
        DepartmentInventory.DepartmentInventory(root)
        

    def academics(self, root):
        self.clear()
        DepartmentAcademic.DepartmentAcademic(root)

    def accounts(self, root):
        self.clear()
        DepartmentAccount.DepartmentAccount(root)

    def clear(self):
        self.frame.destroy()
       
if __name__ == '__main__':
    root = Tk()
    DepartmentMainMenu(root)