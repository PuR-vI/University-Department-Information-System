import DepartmentUDIS
from tkinter import *
import AddFunds
import ES
from PIL import Image, ImageTk

class DepartmentAccount:
    def __init__(self, root):
        root.title('Department-Account')
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

        root.geometry('800x600')
        root.minsize(800, 600)
        root.maxsize(800, 600)

        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM total')
        amount = (cursor_.fetchone())[0]

        self.addButton = Button(self.frame, text='Add Funds', anchor=W, command=lambda: self.addFunds(root))
        self.totalAmount = Label(self.frame, text='Total Amount : Rs. ' + str(amount) , anchor=W, font=('Helvetica', 15, 'bold'))

        self.backButton = Button(self.frame, text='Back', command=lambda: self.back(root))
        self.exitButton = Button(self.frame, text='Exit', command=exit)

        self.addButton.grid(row=0, pady=10)
        self.totalAmount.grid(row=1, sticky=W)

        self.exitButton.grid(row=3, sticky=N+W, padx=50, pady=10)
        self.backButton.grid(row=3, sticky=N+E, padx=50, pady=10)

        self.frame.rowconfigure(2, weight=1)

        self.viewPassbook(root)

        self.frame.columnconfigure(0, weight=1)

        root.mainloop()

    def back(self, root):
        self.clear()
        DepartmentUDIS.DepartmentMainMenu(root)

    def clear(self):
        self.frame.destroy()

    def addFunds(self, root):
        self.clear()
        AddFunds.AddFunds(root)

    def viewPassbook(self, root):
        # Make a frame inside the self.frame in the row = 3.
        displayPassbook = Frame(self.frame)
        displayPassbook.grid(row=2, sticky=E+W+N+S)
        Label(displayPassbook, text='Organisation', relief=GROOVE).grid(row=0, column=0, sticky=E+W)
        Label(displayPassbook, text='Amount', relief=GROOVE).grid(row=0, column=1, sticky=E+W)
        Label(displayPassbook, text='Date', relief=GROOVE).grid(row=0, column=2, sticky=E+W)
        Label(displayPassbook, text='Purpose', relief=GROOVE).grid(row=0, column=3, sticky=E+W)

        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM transactions')

        allTransactions = cursor_.fetchall()
        allTransactions.reverse()

        for i, transaction in enumerate(allTransactions):
            if transaction[1] > 0:
                bg = '#6F6'
            else:
                bg = '#F99'
            Label(displayPassbook, text=transaction[0], bg=bg).grid(row=i + 1, column=0, sticky = E+W)
            Label(displayPassbook, text=transaction[1], bg=bg).grid(row=i + 1, column=1, sticky = E+W)
            Label(displayPassbook, text=transaction[2], bg=bg).grid(row=i + 1, column=2, sticky = E+W)
            Label(displayPassbook, text=transaction[3], bg=bg).grid(row=i + 1, column=3, sticky = E+W)

        displayPassbook.columnconfigure(0, weight=1)
        displayPassbook.columnconfigure(3, weight=2)

    @staticmethod
    def test():
        print('Testing the DepartmentAccount Class\n')
        success = 0
        fail = 0
        print('a. Donation amount is not a number')
        try:
            AddFunds.AddFunds.addfunds('MHRD', '10 Lacs', '27/03/2021', 'PCs for Takshashila')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            print('\tPASS')
            success += 1

        print('b. Unnamed Donation')
        try:
            AddFunds.AddFunds.addfunds('', '1000000', '27/03/2021', 'PCs for Takshashila')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            print('\tPASS')
            success += 1

        print('c. Fund Amount is empty')
        try:
            AddFunds.AddFunds.addfunds('MHRD', '', '27/03/2021', 'PCs for Takshashila')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            print('\tPASS')
            success += 1

        print('d. Purpose is not mentioned')
        try:
            AddFunds.AddFunds.addfunds('MHRD', '1000000', '27/03/2021', '')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            print('\tPASS')
            success += 1

        print('e. Date format is wrong')
        try:
            AddFunds.AddFunds.addfunds('MHRD', '1000000', '27/Mar/2021', 'PCs for Takshashila')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            print('\tPASS')
            success += 1

        print('f. Date is Invalid')
        try:
            AddFunds.AddFunds.addfunds('MHRD', '1000000', '29/02/2021', 'PCs for Takshashila')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            print('\tPASS')
            success += 1

        print('g. Happy Path Testing')
        try:
            AddFunds.AddFunds.addfunds('MHRD', '1000000', '27/03/2021', 'PCs for Takshashila')
            connect_, cursor_ = ES.get_student_db_ES()
            cursor_.execute('SELECT * FROM transactions WHERE organisation=(:org) AND amount=(:amt) AND date=(:date) AND purpose=(:purpose)'
                            , {'org': 'MHRD', 'amt': 1000000, 'date': '27/03/2021', 'purpose': 'PCs for Takshashila'})
            result = cursor_.fetchall()
            cursor_.execute('SELECT * FROM total')
            amount = (cursor_.fetchone())[0]
            if result and amount == 2000000:
                success += 1
                print('\tPASS')
            else:
                fail += 1
                print('\tFAIL')
        except Exception as e:
            print(e)
            print('\tFAIL')
            fail += 1

        print(f'Test cases passed {success}/{success + fail}')
        print(f'Percentage = {(success / (success + fail)) * 100}')

if __name__ == '__main__':
    DepartmentAccount.test()

