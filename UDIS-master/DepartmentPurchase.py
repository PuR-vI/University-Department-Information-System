from tkinter import *
import DepartmentInventory
import ES
import datetime
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import Image, ImageTk

def dropdown_defocus(event):
    event.widget.selection_clear()

class DepartmentPurchase:
    def __init__(self,root):
        root.title("Purchase Items")
        root.geometry("400x400")
        root.maxsize(400,400)
        root.minsize(400,400)
        self.frame=Frame(root)
        self.frame.grid(row=0,column=0,sticky="nsew")

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


        self.nameLabel= Label(self.frame,text="Name")
        self.typeLabel= Label(self.frame,text="Type")
        self.quantityLabel= Label(self.frame,text="Quantity")
        self.totpriceLabel= Label(self.frame,text="Total Price")
        self.dateLabel= Label(self.frame,text="Date of purchase")
        self.locationLabel= Label(self.frame,text="Location")

        self.nameEntry = Entry(self.frame,borderwidth=0)

        self.combostyle=ttk.Style()
        self.combostyle.map('TCombobox', fieldbackground=[('readonly', 'white')])
        self.combostyle.map('TCombobox', selectbackground=[('readonly', 'white')])

        self.var=StringVar(self.frame)
        self.var.set("Miscellaneous")
        self.typeDropdown = ttk.Combobox(self.frame,foreground="black",width=27,takefocus=False,textvariable=self.var,state='readonly')
        self.typeDropdown['value']=('Miscellaneous',
                                        'Computers',
                                        'Furniture',
                                        'Stationery')
        self.typeDropdown.bind("<FocusIn>", dropdown_defocus)

        self.quantityEntry = Entry(self.frame,borderwidth=0)
        self.totpriceEntry = Entry(self.frame,borderwidth=0)
        self.dateEntry = Entry(self.frame,borderwidth=0)
        self.locationEntry = Entry(self.frame,borderwidth=0)

        self.nameLabel.grid(row=0,column=0,sticky=E+S,padx=5,pady=3)
        self.typeLabel.grid(row=1,column=0,sticky=E,padx=5,pady=3)
        self.quantityLabel.grid(row=2,column=0,sticky=E,padx=5,pady=3)
        self.totpriceLabel.grid(row=3,column=0,sticky=E,padx=5,pady=3)
        self.dateLabel.grid(row=4,column=0,sticky=E,padx=5,pady=3)
        self.locationLabel.grid(row=5,column=0,sticky=E,padx=5,pady=3)

        self.purchaseButton=Button(self.frame,text="Purchase",command=lambda:self.purchase(root))
        self.backButton=Button(self.frame,text="Back",command=lambda:self.back(root))
        self.exitButton=Button(self.frame,text="Exit",command=exit)

        self.nameEntry.grid(row=0,column=1,sticky=W+S+E,padx=5,pady=3)
        self.typeDropdown.grid(row=1,column=1,sticky=W+E,padx=5,pady=3)
        self.quantityEntry.grid(row=2,column=1,sticky=W+E,padx=5,pady=3)
        self.totpriceEntry.grid(row=3,column=1,sticky=W+E,padx=5,pady=3)
        self.dateEntry.grid(row=4,column=1,sticky=W+E,padx=5,pady=3)
        self.locationEntry.grid(row=5,column=1,sticky=E+W,padx=5,pady=3)

        self.purchaseButton.grid(row=6,columnspan=2,column=0,pady=10)
        self.backButton.grid(row=7,columnspan=2,column=0,sticky=E,padx=50,pady=50)
        self.exitButton.grid(row=7,columnspan=2,column=0,sticky=W,padx=50,pady=50)

        self.frame.rowconfigure(0,weight=1)
        self.frame.rowconfigure(7,weight=1)
        self.frame.columnconfigure(0,weight=1)
        self.frame.columnconfigure(1,weight=2)

    @staticmethod
    def insertInventory(name_,type_,quantity_,price_,date_,location_):
        if name_=='' or type_=='' or quantity_=='' or price_=='' or date_=='' or location_=='':
            raise Exception('Enter data in all the fields')

        try:
            price_=int(price_)
        except ValueError as v:
            raise Exception('Enter non-negative integer price')
        if price_<=0:
            raise Exception('Enter non-negative integer price')
            
        try:
            quantity_=int(quantity_)
        except ValueError as v:
            raise Exception('Enter non-negative integer quantity')
        if quantity_<=0:
            raise Exception('Enter non-negative integer quantity')

        try:
            datetime.datetime.strptime(date_, '%d/%m/%Y')
        except ValueError:
            raise Exception("Incorrect date format")
        
        connect_,cursor_=ES.get_student_db_ES()
        cursor_.execute('SELECT * from total')
        amount = (cursor_.fetchone())[0]

        if amount<price_:
            raise Exception('Insufficent funds')

        with connect_:
            
            cursor_.execute("""SELECT * FROM inventory WHERE item_name=(:name) AND location=(:location) AND quantity=(:quantity)
                        AND type=(:type) AND price=(:price)""",{"name":name_,"location":location_,"quantity":quantity_,
                        "type":type_,"price":price_})
            existing=cursor_.fetchall()

            if len(existing)==0:
                cursor_.execute("INSERT INTO inventory VALUES (:name,:location,:quantity,:type,:price)",
                        {'name':name_,'location':location_,'quantity':quantity_,'type':type_,'price':price_})
                cursor_.execute("INSERT INTO transactions VALUES (:organisation,:amount,:date,:purpose)",
                        {'organisation':'Self','amount':-price_,'date':date_,'purpose':'Purchased '+name_})

                cursor_.execute('UPDATE total SET amount=(:n_amt) WHERE amount=(:o_amt)',
                                {'n_amt': amount - price_, 'o_amt': amount})
            else:
                cursor_.execute("""SELECT quantity FROM inventory WHERE item_name=(:name) AND location=(:location) AND quantity=(:quantity)
                        AND type=(:type) AND price=(:price)""",{"name":name_,"location":location_,"quantity":quantity_,
                        "type":type_,"price":price_})
                _quantity=cursor_.fetchone()[0]
                cursor_.execute("""UPDATE inventory SET quantity=(:n_quantity) WHERE item_name=(:name) AND location=(:location) AND quantity=(:quantity)
                        AND type=(:type) AND price=(:price) """,{"name":name_,"location":location_,"quantity":quantity_,
                        "type":type_,"price":price_,"n_quantity":_quantity+quantity_})

            
        
        

    def purchase(self,root):
        name_=self.nameEntry.get()
        type_=self.typeDropdown.get()
        quantity_=self.quantityEntry.get()
        price_=self.totpriceEntry.get()
        date_=self.dateEntry.get()
        location_=self.locationEntry.get()

        try:
            DepartmentPurchase.insertInventory(name_,type_,quantity_,price_,date_,location_)
            self.back(root)
        except Exception as e:
            messagebox.showerror("Failed Purchase", str(e))

    @staticmethod
    def test():
        print("\nTesting the Department Purchase class")
        success = 0
        fail = 0
        print("\ta. Happy path:")
        try:
            DepartmentPurchase.insertInventory('Pens','Stationery',100,500,'20/03/2009','Academic Section')
            print("\tPASS")
            success=success+1
        except:
            print("FAIL\n")
            fail=fail+1
        
        print("\tb. Empty fields:")
        try:
            DepartmentPurchase.insertInventory('','Stationery',100,500,'20/03/2009','Academic Section')
            print("FAIL\n")
            fail=fail+1
        except:
            print("\tPASS")
            success=success+1
        print("\tc. Quantity of items is negative:")
        try:
            DepartmentPurchase.insertInventory('Computer Table','Furniture',-5,1000,'20/03/2009','Software Lab')
            print("\tFAIL\n")
            fail=fail+1
        except:
            print("\tPASS")
            success=success+1

        print("\td. Price is negative:")
        try:
            DepartmentPurchase.insertInventory('Computer Table','Furniture',5,-1000,'20/03/2009','Software Lab')
            print("\tFAIL\n")
            fail=fail+1
        except:
            print("\tPASS")
            success=success+1

        print("\te. Price is not an integer:")
        try:
            DepartmentPurchase.insertInventory('Computer Table','Furniture',5,'1XC','20/03/2009','Software Lab')
            print("\tFAIL\n")
            fail=fail+1
        except:
            print("\tPASS")
            success=success+1

        print("\tf. Price is deducted from total amount:")
        
        connect_,cursor_=ES.get_student_db_ES()
        cursor_.execute('SELECT * from total')
        amount = (cursor_.fetchone())[0]

        DepartmentPurchase.insertInventory('Computer Table','Furniture',5,100,'20/03/2009','Software Lab')
        
        cursor_.execute('SELECT * from total')
        amount_ = (cursor_.fetchone())[0]

        if amount-amount_==100:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1
        
        print("\tg. Insufficient Amount exception:")
        try:
            DepartmentPurchase.insertInventory('Supercomputer','Computers',1,10000000,'20/03/2009','Software Lab')
            print("\tFAIL\n")
            fail=fail+1
        except:
            print("\tPASS")
            success=success+1
            
        print("\th. Increase in quantity upon inserting same item")
        DepartmentPurchase.insertInventory('Computer Table','Furniture',5,100,'20/03/2009','Software Lab')
        cursor_.execute("SELECT quantity FROM inventory WHERE item_name=(:name)",{'name':'Computer Table'})
        quantity=cursor_.fetchone()[0]

        if quantity==10:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL\n")
            fail=fail+1


        print(f'Test cases passed {success}/{success+fail}')
        print(f'Percentage = {(success/(success+fail))*100}')

        

    def back(self,root):
        self.clear()
        DepartmentInventory.DepartmentInventory(root)

    def clear(self):
        self.frame.destroy()