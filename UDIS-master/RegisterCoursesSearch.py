from tkinter import *
import ES
import StudentMain
import StudentSearch


class RegisterCoursesSearch (StudentSearch.StudentSearch):
    def __init__(self, root):
        root.title('UDIS-Register Courses')
        super().__init__(root)
        root.mainloop()

    def bindingAction(self, event):
        popup_StudentsView = Tk()
        popup_StudentsView.geometry("400x300")
        rollname = event.widget.cget('text')
        roll = rollname.split(' ')
        popup_StudentsView.title(roll[0])
        connect_, cursor_ = ES.get_student_db_ES()
        roll = roll[0]
        cursor_.execute('SELECT * FROM student WHERE roll=(:roll)', {'roll':roll})
        student = cursor_.fetchone()
        # TODO Add register courses functionality
        cursor_.execute('''SELECT * FROM all_courses WHERE sub_code != (SELECT sub_code FROM courses_taken
                         WHERE roll=(:roll) AND grade !=(:grade))''', {'roll': roll, 'grade': 'F'})
        finishedCourses=cursor_.fetchall()
        




    def back_command(self, root):
        self.clear()
        root.maxsize(800, 600)
        StudentMain.StudentMain(root)


if __name__ == '__main__':
    root = Tk()
    root.minsize(400, 300)
    root.maxsize(800, 600)
    root.geometry('800x600')
    RegisterCoursesSearch(root)
