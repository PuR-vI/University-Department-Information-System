from tkinter import *
import ES
from tkinter import messagebox
import DepartmentAcademic
import CoursesNew
from ScrollableFrame import ScrollableFrame
from PIL import Image, ImageTk

class DepartmentCourses:
    def __init__(self, root):

        root.title('Academics - Courses')

        root.geometry('800x600')
        root.maxsize(800, 600)
        root.minsize(800, 600)

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


        self.courseLabel = Label(self.frame, text='Course Name',fg="white",bg="black")
        self.courseEntry = Entry(self.frame, borderwidth=0)

        self.submitButton= Button(self.frame, text='Search', command=lambda :self.search(root))
        self.addcoursesButton=Button(self.frame,text='Add Courses',command=lambda:self.add(root))
        self.displayFrame = ScrollableFrame(self.frame)
        self.courseLabel.grid(row=2, column=0, padx=5, pady=3)
        self.courseEntry.grid(row=2, column=1)

        self.exitButton = Button(self.frame, text="Exit", command=exit)
        self.backButton = Button(self.frame, text="Back",
                                             command=lambda: self.back(root))

        self.submitButton.grid(row=3, column=0,columnspan=2,pady=20)
        self.addcoursesButton.grid(row=6,column=0,columnspan=2,pady=20)
        self.displayFrame.grid(row=4, column=0,columnspan=2)

        self.exitButton.grid(row=8, column=0, pady=10, padx=50, sticky=S + W)
        self.backButton.grid(row=8, column=1, pady=10, padx=50,  sticky=S+E)

        self.frame.rowconfigure(8, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        root.mainloop()


    def display_courses(self, root, list_):
        
        self.displayFrame.destroy()
        self.displayFrame = Frame(self.frame)
        self.displayScrollframe=ScrollableFrame(self.displayFrame)
        self.displayScrollframe.grid(column=0,row=0,sticky="nsew")
        self.displayFrame.grid(row=5, column=0, columnspan=2)

        self.displayScrollframe.frame.columnconfigure(1,weight=1)
        for i in range(len(list_)):
            courseserialLabel = Label(self.displayScrollframe.frame, anchor=W, text=i+1)
            courserollnameLabel = Label(self.displayScrollframe.frame, anchor=W, text=list_[i][0] + '    ' + list_[i][1])
            courseserialLabel.grid(row=i,column=0, sticky=W+E,padx=5)
            courserollnameLabel.grid(row=i,column=1, sticky=W+E)
            # studentname_Label_DepartmentCourses.bind('<Button-1>', self.viewstudentname_popup_Command_DepartmentCourses)

    def back(self, root):
        self.clear()
        root.maxsize(800, 600)
        DepartmentAcademic.DepartmentAcademic(root)

    def search(self, root):
        coursename_ = self.courseEntry.get()
        self.display_courses(root, DepartmentCourses.searchcourse(coursename_))

    @staticmethod
    def searchcourse(coursename_):
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute("SELECT * FROM all_courses WHERE course_name LIKE (:coursename)", {'coursename':'%'+coursename_+'%'})
        return cursor_.fetchall()

    def clear(self):
        self.frame.destroy()

    def add(self, root):
        self.clear()
        CoursesNew.CoursesNew(root)

    @staticmethod
    def test():
        connect_, cursor_ = ES.get_student_db_ES()
        print('Testing the DepartmentCourses Class\n')
        success = 0
        fail = 0
        print('a. Course Code already present')
        try:
            CoursesNew.CoursesNew.addcourse('CS20006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', '2')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('b. Credits entered is not a number')
        try:
            CoursesNew.CoursesNew.addcourse('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', 'II')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('c. Credits is not in the appropriate range of {1, 2, 3, 4, 5}')
        try:
            CoursesNew.CoursesNew.addcourse('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', '-2')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            CoursesNew.CoursesNew.addcourse('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', '8')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('d. One or more fields left blank')
        try:
            CoursesNew.CoursesNew.addcourse('', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', '2')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            CoursesNew.CoursesNew.addcourse('CS29006', '', 'Abir Das, Sourangshu Bhattacharya', '2')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            CoursesNew.CoursesNew.addcourse('CS29006', 'Software Engineering Lab', '', '2')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        try:
            CoursesNew.CoursesNew.addcourse('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', '')
            fail += 1
            print('\tFAIL')
        except Exception as e:
            # print(e)
            success += 1
            print('\tPASS')

        print('e. Happy Path Testing')
        try:
            CoursesNew.CoursesNew.addcourse('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', '2')
            cursor_.execute('SELECT * FROM all_courses WHERE sub_code=(:code)', {'code': 'CS29006'})
            results = cursor_.fetchall()
            if not len(results) == 1:
                # print('More than one result returned')
                print('\tFAIL')
                fail += 1
            elif not (results[0][0] == 'CS29006' and results[0][1] == 'Software Engineering Lab' and results[0][2] == 'Abir Das, Sourangshu Bhattacharya' and results[0][3] == 2):
                # print('Data entered doesn\'t match')
                print('\tFAIL')
                fail += 1
            else:
                print('\tPASS')
                success += 1
        except Exception as e:
            # print(e)
            fail += 1
            print('\tFAIL')

        try:
            CoursesNew.CoursesNew.addcourse('CS29002', 'Switching Circuits Lab', 'Chittaranjan Mandal, Pabitra Mitra', '2')
            cursor_.execute('SELECT * FROM all_courses WHERE sub_code=(:code)', {'code': 'CS29002'})
            results = cursor_.fetchall()
            if not len(results) == 1:
                # print('More than one result returned')
                print('\tFAIL')
                fail += 1
            elif not (results[0][0] == 'CS29002' and results[0][1] == 'Switching Circuits Lab' and results[0][2] == 'Chittaranjan Mandal, Pabitra Mitra' and results[0][3] == 2):
                # print('Data entered doesn\'t match')
                print('\tFAIL')
                fail += 1
            else:
                print('\tPASS')
                success += 1
        except Exception as e:
            # print(e)
            fail += 1
            print('\tFAIL')

        try:
            CoursesNew.CoursesNew.addcourse('CS29003', 'Algorithms Lab', 'Animesh Mukherjee, Pawan Goyal', '2')
            cursor_.execute('SELECT * FROM all_courses WHERE sub_code=(:code)', {'code': 'CS29003'})
            results = cursor_.fetchall()
            if not len(results) == 1:
                # print('More than one result returned')
                print('\tFAIL')
                fail += 1
            elif not (results[0][0] == 'CS29003' and results[0][1] == 'Algorithms Lab' and results[0][2] == 'Animesh Mukherjee, Pawan Goyal' and results[0][3] == 2):
                # print('Data entered doesn\'t match')
                print('\tFAIL')
                fail += 1
            else:
                print('\tPASS')
                success += 1
        except Exception as e:
            # print(e)
            fail += 1
            print('\tFAIL')

        try:
            CoursesNew.CoursesNew.addcourse('CS39003', 'Compilers Lab', 'Partha Pratim Das', '2')
            cursor_.execute('SELECT * FROM all_courses WHERE sub_code=(:code)', {'code': 'CS39003'})
            results = cursor_.fetchall()
            if not len(results) == 1:
                # print('More than one result returned')
                print('\tFAIL')
                fail += 1
            elif not (results[0][0] == 'CS39003' and results[0][1] == 'Compilers Lab' and results[0][2] == 'Partha Pratim Das' and results[0][3] == 2):
                # print('Data entered doesn\'t match')
                print('\tFAIL')
                fail += 1
            else:
                print('\tPASS')
                success += 1
        except Exception as e:
            # print(e)
            fail += 1
            print('\tFAIL')

        print('f. Searching Courses with empty keyword')
        expected = [('CS31003', 'Compilers', 'Partha Pratim Das', 3), ('CS31005', 'Algorithms II', 'Abhijit Das', 4), ('CS21004', 'FLAT', 'Abhijit Das', 4), ('CS21002', 'SCLD', 'Chittaranjan Mandal', 4), ('CS20006', 'Software Engineering', 'Partha Pratim Das', 3), ('CS21003', 'Algorithms I', 'Pawan Goyal', 4), ('CS21001', 'Discrete Structures', 'Aritra Hazra', 4), ('CS10001', 'PDS', 'Sudeshna Sarkar', 3), ('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', 2), ('CS29002', 'Switching Circuits Lab', 'Chittaranjan Mandal, Pabitra Mitra', 2), ('CS29003', 'Algorithms Lab', 'Animesh Mukherjee, Pawan Goyal', 2), ('CS39003', 'Compilers Lab', 'Partha Pratim Das', 2)]
        result = DepartmentCourses.searchcourse('')
        if expected == result:
            success += 1
            print('\tPASS')
        else:
            fail += 1
            print('\tFAIL')

        print('g. Searching Courses with Keyword "Lab"')
        expected = [('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', 2), ('CS29002', 'Switching Circuits Lab', 'Chittaranjan Mandal, Pabitra Mitra', 2), ('CS29003', 'Algorithms Lab', 'Animesh Mukherjee, Pawan Goyal', 2), ('CS39003', 'Compilers Lab', 'Partha Pratim Das', 2)]
        if expected == DepartmentCourses.searchcourse('Lab'):
            success += 1
            print('\tPASS')
        else:
            fail += 1
            print('\tFAIL')

        print('h. Searching Courses with Keyword "Software"')
        expected = [('CS20006', 'Software Engineering', 'Partha Pratim Das', 3), ('CS29006', 'Software Engineering Lab', 'Abir Das, Sourangshu Bhattacharya', 2)]
        if expected == DepartmentCourses.searchcourse('Software'):
            success += 1
            print('\tPASS')
        else:
            fail += 1
            print('\tFAIL')

        print(f'Test cases passed {success}/{success + fail}')
        print(f'Percentage = {(success / (success + fail)) * 100}')


if __name__ == '__main__':
    DepartmentCourses.test()
