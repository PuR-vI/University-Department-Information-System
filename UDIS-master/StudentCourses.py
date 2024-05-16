from tkinter import *
import ES
import StudentMain
import StudentSearch
from ScrollableFrame import ScrollableFrame
import tkinter.ttk as ttk
from tkinter import messagebox


class StudentCourses (StudentSearch.StudentSearch):
    def __init__(self, root):
        root.title('UDIS-Register Courses')
        super().__init__(root)
        root.mainloop()

    @staticmethod
    def getcourses(roll):
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('''SELECT * FROM all_courses WHERE sub_code NOT IN (SELECT sub_code FROM courses_taken
                                 WHERE roll=(:roll) AND grade !=(:grade))''', {'roll': roll, 'grade': 'F'})

        courses = cursor_.fetchall()

        return courses
    def bindingAction(self, event):
        popupCourse = Tk()
        popupCourse.eval('tk::PlaceWindow . center')
        popupCourse.config(bg='white')
        popupCourse.geometry("430x460")
        popupCourse.minsize(430, 460)
        popupCourse.maxsize(430, 460)
        rollAndName = event.widget.cget('text')
        roll = rollAndName.split(' ')
        popupCourse.title("Register courses for " + roll[0])
        roll = roll[0]

        courses = StudentCourses.getcourses(roll)

        entryframe = Frame(popupCourse)
        entryframe.grid(row=0, column=0)
        tex = Label(entryframe, text="Enter Semester", padx=5, bg='white', pady=20)
        tex.grid(row=0, column=0)
        sem = Entry(entryframe)
        entryframe.configure(bg='white')
        sem.grid(row=0, column=1)

        courseframe = ScrollableFrame(popupCourse)
        buttons = []
        Label(courseframe.frame, text="Code", padx=10, borderwidth=1, relief='solid').grid(row=0, column=0, sticky=W+E)
        Label(courseframe.frame, text="Course Name", anchor=W, padx=20, borderwidth=1, relief='solid').grid(row=0, column=1, sticky=W+E)
        Label(courseframe.frame, text="Credits", anchor=W, padx=10, borderwidth=1, relief='solid').grid(row=0, column=2, sticky=W+E)
        Label(courseframe.frame, text=" ", anchor=W, padx=10, borderwidth=1, relief='solid').grid(row=0, column=3, sticky=W+E)
        for i in range(len(courses)):
            Label(courseframe.frame, text=courses[i][0], padx=10).grid(row=i+1, column=0)
            Label(courseframe.frame, text=courses[i][1], anchor=W, padx=20).grid(row=i+1, column=1, sticky=W+E)
            Label(courseframe.frame, text=courses[i][3], padx=10).grid(row=i+1, column=2, sticky=W+E)
            buttons.append(ttk.Checkbutton(courseframe.frame,
                                           takefocus=0,
                                           var = IntVar(0)))
            buttons[i].grid(row=i+1, column=3, sticky=E+W)
            buttons[i].state(['!alternate'])

        courseframe.grid(row=1, column=0)

        submitbutton = ttk.Button(master=popupCourse,
                                  text='Submit',
                                  command= lambda : self.formsubmit(buttons,
                                                                    sem,
                                                                    courses,
                                                                    roll,
                                                                    popupCourse))
        submitbutton.config(padding = [5,5,5,5])
        submitbutton.grid(row=4, column=0, columnspan=1)


        popupCourse.columnconfigure(0, weight=1) # Serial Name of Course
        popupCourse.columnconfigure(1, weight=2) # Name of Course
        popupCourse.columnconfigure(2, weight=1) # Credits of the Course
        popupCourse.columnconfigure(3, weight=1)

    def formsubmit(self, buttons_, sem, courses, roll, popupcourse):
        try:
            values = [button.instate(['selected']) for button in buttons_]
            StudentCourses.submit(values, sem.get(), courses, roll)
            messagebox.showinfo("Register courses", "Courses successfully registered")
            popupcourse.destroy()

        except Exception as e:
            messagebox.showerror("Register courses", e)


    @staticmethod
    def submit(values, sem, courses, roll):
        x = values.count(True)

        if x > 7:
            raise  Exception('Student cannot register more than 7 courses')
        elif sem == "":
            raise Exception('Registration Error', 'Semester column is empty')
        elif sem[:3] != "AUT" and sem[:3] != "SPR":
            raise Exception('Registration Error', 'Semester values can only be AUT<year> or SPR<year>')
        conn_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT roll FROM courses_taken WHERE grade="f" OR grade="F"')
        if (len(cursor_.fetchall())) > 0:
            if x > 5:
                raise Exception('Student with backlog cannot register more than 5 courses')

        ### TODO Check the backlog situations after making interfaces in the database
        for i in range(len(values)):
            if values[i]:
                course_code = courses[i][0]
                grade = 'R'
                seme = sem
                with conn_:
                    cursor_.execute("INSERT INTO courses_taken VALUES (:roll, :sub_code, :grade, :sem_taken)",
                                        {'roll': roll, 'sub_code': course_code, 'grade': grade, 'sem_taken': seme})



    def back(self, root):
        self.clear()
        root.maxsize(800, 600)
        StudentMain.StudentMain(root)

    @staticmethod
    def test():
        success = 0
        failure = 0

        print("\nTesting the StudentsCourses class")
        print("\ta. Only non-cleared courses should be displayed")
        c1 = StudentCourses.getcourses('19CS10055')
        clist1 = [c[1] for c in c1]
        clist2 = ['Algorithms Lab',
                  'Switching Circuits Lab',
                  'Software Engineering Lab',
                  'Compilers',
                  'Algorithms II',
                  'Compilers Lab']
        try:
            if sorted(clist1) == sorted(clist2):
                print("\tPASS")
                success +=1
            else:
                print("\tFAIL")
                failure +=1
        except:
            print("\tFAIL")
            failure += 1

        print("\tb. Backlogged courses are shown")
        c1 = StudentCourses.getcourses('19CS30037')
        clist1 = [c[1] for c in c1]
        clist2.append('FLAT')
        # print(clist1)
        # print(clist2)
        try:
            if sorted(clist1) == sorted(clist2):
                print("\tPASS")
                success +=1
            else:
                print("\tFAIL")
                failure +=1
        except:
            print("\tFAIL")
            failure += 1

        print("\tc. Cleared Backlogged courses are not shown")
        c1 = StudentCourses.getcourses('19CS10045')
        clist1 = [c[1] for c in c1]
        try:
            if 'Discrete Structures' not in clist1:
                print("\tPASS")
                success +=1
            else:
                print("\tFAIL")
                failure +=1
        except:
            print("\tFAIL")
            failure += 1

        print('\td. Maximum cap on the number of courses (non-backlog)')
        try:
            f = False
            try:
                c1 = StudentCourses.getcourses('19CS10075')
            except:
                failure+=1
                print("\tFAIL")
                f = True
            if not f:
                StudentCourses.submit([True, True, True, True, True, True, True, True],'AUT2019', c1,'19CS10075')

        except:
            print("\tPASS")
            success += 1

        print('\te. Maximum cap on the number of courses (backlog)')
        try:
            f = False
            try:
                c1 = StudentCourses.getcourses('19CS10045')
            except:
                failure+=1
                print("\tFAIL")
                f = True
            if not f:
                StudentCourses.submit([True, True, True, True, True, True],'AUT2019', c1,'19CS10075')

        except:
            print("\tPASS")
            success += 1

        print('\tf. Check if all registered and not graded courses have a grade of R')
        try:
            c1 = StudentCourses.getcourses('19CS10075')
            cl = [c[1] for c in c1]
            nl = [False]*len(c1)
            for i in range(len(cl)):
                if cl[i] in ['PDS', 'Algorithms I', 'Discrete Structures']:
                    nl[i] = True

            StudentCourses.submit(nl, 'AUT2019', c1, '19CS10075')

            conn, cursor = ES.get_student_db_ES()
            with conn:
                cursor.execute("SELECT grade FROM courses_taken WHERE roll='19CS10075' ")
                cs = cursor.fetchall()
                matrix = [c[0]=='R' for c in cs]
                if matrix.count(True) == 3:
                    print("\tPASS")
                    success +=1
                else:
                    print("\tFAIL")
                    failure +=1

        except Exception as e:
            print("\tFAIL")
            failure +=1

        print('\tg. Can register a backlogged course')
        try:
            c1 = StudentCourses.getcourses('19CS30037')
            cx = [c[1] for c in c1]
            nl = [False]*len(cx)
            for i in range(len(cx)):
                if cx[i] in ['FLAT', 'Switching Circuits Lab']:
                    nl[i] = True

            StudentCourses.submit(nl, 'AUT2020',c1, '19CS30037')
            conn, cursor = ES.get_student_db_ES()
            with conn:
                cursor.execute("SELECT * FROM courses_taken WHERE roll='19CS30037' AND grade='R'")
                cs = cursor.fetchall()
                csx = [c[1] for c in cs]

                if 'CS21004' in csx:
                    print("\tPASS")
                    success += 1
                else:
                    print("\tFAIL")
                    failure += 1

        except:
            print('\tFAIL')
            failure += 1

        print(f'\tTest cases passed {success}/{success + failure}')
        print(f'\tPercentage = {(success / (success + failure)) * 100}')

if __name__ == '__main__':
   StudentCourses.test()
