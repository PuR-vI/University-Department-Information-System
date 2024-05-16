from tkinter import *
import tkinter.ttk as ttk
import ES
import DepartmentUDIS
import DepartmentPurchase
from ScrollableFrame import ScrollableFrame
from PIL import Image, ImageTk

def dropdown_defocus(event):
    event.widget.selection_clear()

class DepartmentInventory:
    def __init__(self,root):
        root.title("Department Inventory")
        root.geometry('800x600')
        root.minsize(800, 600)
        root.maxsize(800, 600)
        self.frame=Frame(root)
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

        self.itemnameLabel=Label(self.frame,text="Item Name: ",anchor=E)
        self.itemnameEntry=Entry(self.frame,borderwidth=0,width=27)
        self.itemtypeLabel=Label(self.frame,text="Type: ",anchor=E)

        self.combostyle=ttk.Style()
        self.combostyle.map('TCombobox', fieldbackground=[('readonly', 'white')])
        self.combostyle.map('TCombobox', selectbackground=[('readonly', 'white')])
        # self.combostyle.

        self.var=StringVar(self.frame)
        self.var.set("All")
        self.typeDropdown = ttk.Combobox(self.frame,foreground="black",width=27,takefocus=False,textvariable=self.var,state='readonly')
        self.typeDropdown['value']=('All',
                                        'Miscellaneous',
                                        'Computers',
                                        'Furniture',
                                        'Stationery')
        self.typeDropdown.bind("<FocusIn>", dropdown_defocus)

        self.submitButton=Button(self.frame,text='Search',command=lambda:self.search())
        self.addButton=Button(self.frame,text='Purchase New Item',command=lambda:self.add(root))
        self.displayFrame=ScrollableFrame(self.frame)

        self.backButton=Button(self.frame,text="Back",command=lambda: self.back(root))
        self.exitButton=Button(self.frame,text="Exit",command=exit)

        self.itemnameLabel.grid(row=0,column=0,sticky=E+W,pady=10,padx=10)
        self.itemnameEntry.grid(row=0,column=1,sticky=W,pady=10)
        self.itemtypeLabel.grid(row=1,column=0,sticky=E+W,pady=10,padx=10)
        self.typeDropdown.grid(row=1,column=1,sticky=W,pady=10)
        self.submitButton.grid(row=2,column=0,sticky=E,pady=10,padx=10)
        self.addButton.grid(row=2,column=1,sticky=W,pady=10,padx=10)
        self.displayFrame.grid(row=3,column=0,columnspan=2,sticky="nsew",padx=10,pady=10)
        self.exitButton.grid(row=4,column=0,columnspan=2,sticky=W,padx=50,pady=20)
        self.backButton.grid(row=4,column=1,columnspan=2,sticky=E,padx=50,pady=20)

        for i in range(2):
            self.frame.columnconfigure(i,weight=1)
        self.frame.rowconfigure(3,weight=1)

    def display(self,list_):
        self.displayFrame.destroy()
        self.displayFrame=ScrollableFrame(self.frame)
        self.displayFrame.grid(row=3,column=0,columnspan=2,sticky="nsew",padx=10,pady=10)
        # print(list_)
        Label(self.displayFrame.frame,text='Sl. no.',relief=GROOVE).grid(row=0,column=0,sticky=E+W,padx=2)
        Label(self.displayFrame.frame,text='Item Name',relief=GROOVE).grid(row=0,column=1,sticky=E+W,padx=2)
        Label(self.displayFrame.frame,text='Location',relief=GROOVE).grid(row=0,column=2,sticky=E+W,padx=2)
        Label(self.displayFrame.frame,text='Quanitity',relief=GROOVE).grid(row=0,column=3,sticky=E+W,padx=2)
        Label(self.displayFrame.frame,text='Type',relief=GROOVE).grid(row=0,column=4,sticky=E+W,padx=2)

        for i in range(len(list_)):
            itemSerial = Label(self.displayFrame.frame, anchor=W, text=i+1)
            itemName = Label(self.displayFrame.frame,wraplength=400, anchor=W, text=list_[i][0])
            itemLocation = Label(self.displayFrame.frame, anchor=W, text=list_[i][1])
            itemQuantity= Label(self.displayFrame.frame, anchor=W, text=list_[i][2])
            itemType= Label(self.displayFrame.frame, anchor=W, text=list_[i][3])
            
            itemSerial.grid(row=i+1, column=0, sticky=W+E,padx=2,pady=1)
            itemName.grid(row=i+1, column=1, sticky=W+E,padx=2,pady=1)
            itemLocation.grid(row=i+1,column=2,sticky=W+E,padx=2,pady=1)
            itemQuantity.grid(row=i+1,column=3,sticky=W+E,padx=2,pady=1)
            itemType.grid(row=i+1,column=4,sticky=W+E,padx=2,pady=1)
            # studentRollAndName.bind('<Button-1>', self.bindingAction)   
        self.displayFrame.frame.columnconfigure(1,weight=1)  
    
    @staticmethod
    def getInventory(name_,type_):
        connect_, cursor_ = ES.get_student_db_ES()
        if name_ == "" and type_ == "All":
            cursor_.execute("SELECT * FROM inventory")
        elif name_ != "" and type_=="All":
            cursor_.execute("SELECT * FROM inventory WHERE item_name LIKE (:name)",{'name':'%'+name_+'%'})
        elif name_ == "" and type_!="All":
            cursor_.execute("SELECT * FROM inventory WHERE type LIKE (:type)", {'type':'%'+type_+'%'})
        else:
            cursor_.execute("SELECT * FROM inventory WHERE item_name LIKE (:name) AND type LIKE (:type)", {'name':'%'+name_+'%', 'type':'%'+type_+'%'})

        return cursor_.fetchall()

    def search(self):
        
        name_ = self.itemnameEntry.get()
        type_ = self.typeDropdown.get()
    
        self.display(DepartmentInventory.getInventory(name_,type_))

    def add(self,root):
        self.clear()
        DepartmentPurchase.DepartmentPurchase(root)

    def back(self,root):
        self.clear()
        DepartmentUDIS.DepartmentMainMenu(root)

    @staticmethod
    def test():
        print("\nTesting the Department Purchase class")
        success = 0
        fail = 0
        print("\ta. Blank name and type all:")
        
        list_=[('Pens', 'Academic Section', 100, 'Stationery', 500), ('Computer Table', 'Software Lab', 10, 'Furniture', 100)]
        if DepartmentInventory.getInventory('','All')==list_:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1
        
        print("\tb. Specific name and type all:")
        list_=[('Pens', 'Academic Section', 100, 'Stationery', 500)]
        if DepartmentInventory.getInventory('Pens','All')==list_:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1
        
        print("\tc. No name and type specific:")
        list_=[('Pens', 'Academic Section', 100, 'Stationery', 500)]
        if DepartmentInventory.getInventory('','Stationery')==list_:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1

        print("\td. Name specific and type specific:")
        list_=[('Computer Table', 'Software Lab', 10, 'Furniture', 100)]
        if DepartmentInventory.getInventory('comp','Furniture')==list_:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1
        
        print(f'Test cases passed {success}/{success+fail}')
        print(f'Percentage = {(success/(success+fail))*100}')

    def clear(self):
        self.frame.destroy()