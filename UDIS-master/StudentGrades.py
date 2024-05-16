from tkinter import *
import ES
import StudentMain
import StudentSearch
from ScrollableFrame import ScrollableFrame
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3

def dropdown_defocus_StudentNew(event):
    event.widget.selection_clear()

class StudentGrades (StudentSearch.StudentSearch):
    def __init__(self, root):
        root.title('UDIS - Enter Grades')
        super().__init__(root)
        root.mainloop()

    @staticmethod
    def getCourses(roll):
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('''SELECT * FROM courses_taken WHERE roll == (:roll) AND grade == (:grade)''',
                        {'roll': roll, 'grade': 'R'})

        courses = cursor_.fetchall()
        return courses

    def bindingAction(self, event):

        rollAndName = event.widget.cget('text')
        roll = rollAndName.split(' ')

        roll = roll[0]
       

        courses = StudentGrades.getCourses(roll)

        if len(courses) == 0:
            messagebox.showinfo("Enter grades for " + roll, "No grades to be entered")
            return

        popupCourse = Tk()
        popupCourse.eval('tk::PlaceWindow . center')
        popupCourse.config(bg='white')
        popupCourse.geometry("505x460")
        popupCourse.minsize(506, 460)
        popupCourse.maxsize(506, 460)
        popupCourse.title("Enter grades for " + roll[0])


        entryframe = Frame(popupCourse)
        entryframe.grid(row=0, column=0)



        courseframe = ScrollableFrame(popupCourse, 340, 490)

        combostyle = ttk.Style()
        combostyle.map('TCombobox', fieldbackground=[('readonly', 'white')])
        combostyle.map('TCombobox', selectbackground=[('readonly', 'white')])


        courseDropdown = []
        Label(courseframe.frame, text="Code", padx=10, borderwidth=1, relief='solid').grid(row=0, column=0, sticky=W+E)
        Label(courseframe.frame, text="Course Name", anchor=W, padx=20, borderwidth=1, relief='solid').grid(row=0, column=1, sticky=W+E)
        Label(courseframe.frame, text="Sem Taken", anchor=W, padx=10, borderwidth=1, relief='solid').grid(row=0, column=2, sticky=W+E)
        Label(courseframe.frame, text="Grade", anchor=W, padx=10, borderwidth=1, relief='solid').grid(row=0, column=3, sticky=W+E)
        for i in range(len(courses)):
            Label(courseframe.frame, text=courses[i][1], padx=10).grid(row=i+1, column=0)
            conn_, cursor_ = ES.get_student_db_ES()
            cursor_.execute('SELECT * FROM all_courses WHERE sub_code == (:code)',{"code": courses[i][1]} )
            c_name = cursor_.fetchone()
            Label(courseframe.frame, text=c_name[1], anchor=W, padx=20).grid(row=i + 1, column=1, sticky=W + E)
            
            Label(courseframe.frame, text=courses[i][3], padx=10).grid(row=i + 1, column=2, sticky=W + E)

            courseDropdown.append(ttk.Combobox(courseframe.frame,
                                               foreground="black",
                                               width=10,
                                               takefocus=False,
                                               state='readonly'))
            courseDropdown[i]['value'] = ('EX','A', 'B', 'C','D','P','F')
            courseDropdown[i].current(0)
            courseDropdown[i].bind("<FocusIn>", dropdown_defocus_StudentNew)

            courseDropdown[i].grid(row=i+1, column=3, sticky=E+W)


        courseframe.grid(row=1, column=0)

        submitbutton = ttk.Button(master=popupCourse,
                                  text='Submit', command=lambda: self.formsubmit(roll, courses, courseDropdown, popupCourse))
        submitbutton.config(padding = [5,5,5,5])
        submitbutton.grid(row=4, column=0, columnspan=1)


        popupCourse.columnconfigure(0, weight=1) # Serial Name of Course
        popupCourse.columnconfigure(1, weight=2) # Name of Course
        popupCourse.columnconfigure(2, weight=1) # Credits of the Course
        popupCourse.columnconfigure(3, weight=1)

    def formsubmit(self, roll, courses, dropdown, window):
        grades = [c.get() for c in dropdown]
        try:
            StudentGrades.submit(roll, courses, grades)
            messagebox.showinfo("Enter Grades", "Grades updated for " + roll)
            window.destroy()

        except Exception as e:
            messagebox.showwarning("Enter grades", e)


    @staticmethod
    def submit(roll, courses, grades):
        conn, cursor = ES.get_student_db_ES()
        tx = [grade=="" for grade in grades]
        if tx.count(True) > 0:
            raise Exception("Some columns blank while entering grades")

        try:
            for i in range (len(courses)):
                with conn:
                    if grades[i]!='F':
                        cursor.execute('''UPDATE courses_taken
                                          SET grade = "f"
                                          WHERE roll ==(:roll) AND sub_code==(:sub_code) AND grade=="F"''',
                                       {"roll" : roll,
                                        "sub_code" : courses[i][1]})

                    cursor.execute('''UPDATE courses_taken
                                      SET grade = (:grade)
                                      WHERE roll==(:roll) AND sub_code==(:code) AND sem_taken==(:sem)''',
                                   {"grade": grades[i],
                                    "roll": roll,
                                    "code": courses[i][1],
                                    "sem": courses[i][3]})

        except sqlite3.OperationalError:
            raise Exception("sqlite3 OperationalError")

    @staticmethod
    def test():
        print("Unit test for StudentGrades class")
        print("\ta. Visibility of Courses for Grading")
        success = 0
        fail = 0
        c1 = StudentGrades.getCourses('19CS30037')
        cx = [c[1] for c in c1]
        cx2 = ['CS21004', 'CS29002']
        try:
            if sorted(cx) == sorted(cx2):
                print("\tPASS")
                success+=1
            else:
                print("\tFAIL")
                fail+=1

        except:
            print("\tFAIL")
            fail += 1

        print("\tb. Empty Columns while Grading")
        c1 = StudentGrades.getCourses('19CS10075')
        cx = [c[1] for c in c1]
        grades = ['A']*len(cx)
        grades[len(grades)- 1] = ''
        try:
            StudentGrades.submit('19CS10075', c1, grades)
            fail += 1
            print("\tFAIL")

        except:
            success +=1
            print("\tPASS")

        print("\tc. Happy path, grading subjects")
        c1 = StudentGrades.getCourses('19CS30037')
        grades = ['A']*len(c1)
        cx = [c[1] for c in c1]
        f = False
        for i in range(len(c1)):
            if cx[i] == 'CS21004':
                grades[i] = 'B'
            elif cx[i] == 'CS29002':
                grades[i] = 'A'
            else:
                fail += 1
                f = True
                print("\tFAIL")

        if not f:
            try:
                StudentGrades.submit('19CS30037', c1, grades)
                print("\tPASS")
                success +=1
            except:
                print("\tFAIL")
                fail +=1

        print(f'Test cases passed {success}/{success + fail}')
        print(f'Percentage = {(success / (success + fail)) * 100}')


    def back(self, root):
        self.clear()
        root.maxsize(800, 600)
        StudentMain.StudentMain(root)


if __name__ == '__main__':
    StudentGrades.test()
