from tkinter import *
import os
from sqlite3 import *
import ES
from tkinter import messagebox


def setCredentials():

    window=Tk()
    window.title("Set Credentials")
    window.configure(background="black") 
    Label(window,text='Set User ID: ', fg='white', bg='black').grid(row=0,column=0,sticky=E) 
    Label(window,text='Set Password: ', fg='white', bg='black').grid(row=1,column=0,sticky=E)  
    Label(window,text='Confirm Password: ', fg='white', bg='black').grid(row=2,column=0,sticky=E)
    idEntry=Entry(window)
    pwEntry=Entry(window,show="*")
    cpwEntry=Entry(window,show="*")

    idEntry.grid(row=0,column=1,sticky=W)
    pwEntry.grid(row=1,column=1,sticky=W)
    cpwEntry.grid(row=2,column=1,sticky=W)
    Button(window,text='Set Credentials',command=lambda:setButton(window,pwEntry,idEntry,cpwEntry)).grid(row=3,column=0,columnspan=2)

    window.mainloop()

def setButton(window,pwEntry,idEntry,cpwEntry):
        id_=idEntry.get()
        pw_=pwEntry.get()
        cpw_=cpwEntry.get()
        if pw_=='' and id_=='':
            messagebox.showerror("Set Credentials", "Do not leave any fields empty")
        else:
            connect_,cursor_=Main.init_sql()
            if cpw_==pw_:
                with connect_:
                    cursor_.execute('INSERT INTO authentication VALUES (:id,:pw)',{'id':id_,'pw':pw_})
                window.destroy()
            else:
                messagebox.showerror("Set Credentials", "Password confirmation failed")


class Main():
    def __init__(self):
        self.root = Tk()
        self.root.minsize(400, 300)
        self.root.maxsize(800, 600)
        self.root.geometry('800x600')
        self.root.configure(background="grey")
        self.root.rowconfigure(0, weight=1)

    @staticmethod
    def init_sql():
        file_name = 'Backend/UDIS.db'
        if not os.path.exists(file_name):
            connect_ = connect(file_name)
            cursor_ = connect_.cursor()
            with connect_:
                cursor_.execute("""
                                CREATE TABLE student 
                                    (roll text UNIQUE, student_name text, address text, course text, joining text)""")
                cursor_.execute("""
                                CREATE TABLE courses_taken
                                    (roll text, sub_code text, grade text, sem_taken text)""")

                cursor_.execute("""
                                CREATE TABLE all_courses
                                    (sub_code text UNIQUE, course_name text, prof_name text, credits int)""")

                cursor_.execute("""
                                CREATE TABLE projects
                                (organisation text NOT NULL UNIQUE, incharge text NOT NULL, duration text, 
                                    status text DEFAULT 'Ongoing', name text NOT NULL)""")

                cursor_.execute("""
                                CREATE TABLE publications
                                (prof_name text NOT NULL, pub_name text NOT NULL, date text NOT NULL)""")

                cursor_.execute("""
                                CREATE TABLE inventory 
                                (item_name text NOT NULL, location text, quantity integer NOT NULL, type text NOT NULL, price integer NOT NULL)""")

                cursor_.execute("""CREATE TABLE transactions 
                                (organisation text NOT NULL, amount int, date text NOT NULL, purpose text NOT NULL)""")

                cursor_.execute('''CREATE TABLE total (amount INT)''')
                cursor_.execute('''INSERT INTO total VALUES (0)''')

                cursor_.execute('''CREATE TABLE authentication (userid text NOT NULL, password NOT NULL)''')
        
            while True:
                setCredentials()
                cursor_.execute('SELECT * FROM authentication')
                check=cursor_.fetchall()
                if len(check)!=0:
                    break
                

        else:
            connect_ = connect(file_name)
            cursor_ = connect_.cursor()

        return connect_, cursor_

    def get_root(self):
        return self.root

if __name__ == '__main__':
    connect_, cursor_ = Main.init_sql()
    a = Main()
    ES.ES(a.get_root())
    a.root.mainloop()
