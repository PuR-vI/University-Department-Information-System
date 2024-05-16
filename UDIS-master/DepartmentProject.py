from tkinter import *
import DepartmentResearch
from ScrollableFrame import ScrollableFrame
import ES
import ProjectNew
from tkinter import messagebox
from PIL import Image, ImageTk

class DepartmentProject(DepartmentResearch.DepartmentResearch):
    def __init__(self, root):

        root.geometry('800x600')
        root.minsize(800, 600)
        root.maxsize(800, 600)

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


        root.title('UDIS-Department-Academics-Projects')
        super().__init__(root)
        self.display()
        root.mainloop()

    def display(self):
        self.displayAll.destroy()
        self.displayAll = ScrollableFrame(self.frame)
        self.displayAll.grid(row=0, column=0, padx=30, sticky=N+S+E+W)
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM projects')
        allProjects = cursor_.fetchall()
        Label(self.displayAll.frame, text='Sr. No.', relief=GROOVE).grid(row=0, column=0, sticky=E+W)
        Label(self.displayAll.frame, text='Organisation', relief=GROOVE).grid(row=0, column=1, sticky=E+W)
        Label(self.displayAll.frame, text='Incharge', relief=GROOVE).grid(row=0, column=2, sticky=E+W)
        Label(self.displayAll.frame, text='Duration', relief=GROOVE).grid(row=0, column=3, sticky=E+W)
        Label(self.displayAll.frame, text='Status', relief=GROOVE).grid(row=0, column=4, sticky=E+W)
        Label(self.displayAll.frame, text='Name', relief=GROOVE).grid(row=0, column=5, sticky=E+W)

        for i in range(len(allProjects)):
            Label(self.displayAll.frame, anchor=W, text=i+1).grid(row=i+1, column=0, sticky=E+W, padx=2, pady=2)
            Label(self.displayAll.frame, anchor=W, text=allProjects[i][0]).grid(row=i+1, column=1, sticky=E+W, padx=2, pady=2)
            Label(self.displayAll.frame, anchor=W, text=allProjects[i][1]).grid(row=i+1, column=2, sticky=E+W, padx=2, pady=2)
            Label(self.displayAll.frame, anchor=W, text=allProjects[i][2]).grid(row=i+1, column=3, sticky=E+W, padx=2, pady=2)
            Label(self.displayAll.frame, anchor=W, text=allProjects[i][3]).grid(row=i+1, column=4, sticky=E+W, padx=2, pady=2)
            projectName = Label(self.displayAll.frame, anchor=W, text=allProjects[i][4], wraplength=300)
            projectName.grid(row=i+1, column=5, sticky=W+E)
            projectName.bind('<Button-1>', self.bindingAction)

        self.displayAll.frame.columnconfigure(1, weight=1)
        self.displayAll.frame.columnconfigure(2, weight=1)
        self.displayAll.frame.columnconfigure(5, weight=3)


    def bindingAction(self, event):
        popupProject = Tk()
        popupProject.geometry('400x300')
        projectName = event.widget.cget('text')
        popupProject.title(projectName)
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM projects WHERE name=(:name)', {'name':projectName})
        project = cursor_.fetchone()

        Label(popupProject, text='Organisation').grid(row=1, column=0, sticky=W, padx=10)
        Label(popupProject, text='Incharge').grid(row=2, column=0, sticky=W, padx=10)
        Label(popupProject, text='Duration').grid(row=3, column=0, sticky=W, padx=10)
        Label(popupProject, text='Status').grid(row=4, column=0, sticky=W, padx=10)
        Label(popupProject, text='Name').grid(row=5, column=0, sticky=W, padx=10)

        Button(popupProject, text='Mark Project as Complete', command=lambda: self.markComplete(projectName)).grid(row=6, column=0, columnspan=2)

        Label(popupProject, text=project[0]).grid(row=1, column=1, sticky=W)
        Label(popupProject, text=project[1]).grid(row=2, column=1, sticky=W)
        Label(popupProject, text=project[2]).grid(row=3, column=1, sticky=W)
        Label(popupProject, text=project[3]).grid(row=4, column=1, sticky=W)
        Label(popupProject, text=project[4], anchor=W, justify='left', wraplength=250).grid(row=5, column=1, sticky=W)

        popupProject.columnconfigure(0, weight=1)
        popupProject.columnconfigure(1, weight=3)

    def markComplete(self, name):
        response = messagebox.askyesno(title='Mark Project as Complete', message='Are you sure you want to mark this Project: ' + name + ' as Complete')
        if response == 'no':
            return
        connect_, cursor_ = ES.get_student_db_ES()
        with connect_:
            cursor_.execute('''UPDATE projects SET status="Completed" WHERE name=(:name)''', {'name': name})

    def new(self, root):
        self.clear()
        ProjectNew.ProjectNew(root)

    @staticmethod
    def test():
        print('Testing the DepartmentProject Class\n')
        success = 0
        failure = 0
        print('a. One or more fields left blank')
        try:
            ProjectNew.ProjectNew.addproject('', 'Flipkart', 'Niloy Ganguly', '2018-2023', '20000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', '', 'Niloy Ganguly', '2018-2023', '20000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', '', '2018-2023', '20000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '', '20000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '2018-2023', '', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '2018-2023', '20000', '')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('b. Invalid funds value')
        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '2018-2023', '-23000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '2018-2023', '20 Thousand', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('c. Sufficient Balance not present in the Department Account')
        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '2018-2023', '20000000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('d. Project Name already Exists')
        try:
            ProjectNew.ProjectNew.addproject('Unified Software-Defined Architecture for Industrial Internet of Things', 'IMPRINT-II', 'Sudip Misra', '2019-2020', '20000', '07/04/2021')
            failure += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('e. Happy Path Testing')
        try:
            ProjectNew.ProjectNew.addproject('Social Computing for E-Commerce', 'Flipkart', 'Niloy Ganguly', '2018-2023', '20000', '07/04/2021')
            connect_, cursor_ = ES.get_student_db_ES()
            cursor_.execute('SELECT * FROM projects WHERE name=(:name)',
                            {'name': 'Social Computing for E-Commerce'})
            results1 = cursor_.fetchall()
            cursor_.execute('SELECT * FROM transactions WHERE organisation=(:org) AND amount=(:amt) AND date=(:date) AND purpose=(:purpose)'
                , {'org': 'Flipkart', 'amt': -20000, 'date': '07/04/2021',
                   'purpose': 'Project : Social Computing for E-Commerce'})
            results2 = cursor_.fetchall()
            if not len(results1) == 1:
                print('\tFAIL')
                failure += 1
            elif not (results1[0][0] == 'Flipkart' and results1[0][1] == 'Niloy Ganguly' and results1[0][2] == '2018-2023' and results1[0][4] == 'Social Computing for E-Commerce'):
                print('\tFAIL')
                failure += 1
            elif not results2:
                print('\tFAIL')
                failure += 1
            else:
                success += 1
                print('\tPASS')
        except Exception as e:
            # print(e)
            failure += 1
            print('\tFAIL')

        print(f'Test cases passed {success}/{success + failure}')
        print(f'Percentage = {(success / (success + failure)) * 100}')


if __name__ == '__main__':
    DepartmentProject.test()