from tkinter import *
import ES
import StudentMain
import StudentSearch
import enum
from ScrollableFrame import ScrollableFrame
import subprocess
import os

class StudentsView (StudentSearch.StudentSearch):
    def __init__(self, root):
        root.title('UDIS-View Student')
        super().__init__(root)
        root.mainloop()

    def bindingAction(self, event):
        popupStudent = Tk()
        popupStudent.geometry("400x300")
        rollAndName = event.widget.cget('text')
        roll = rollAndName.split(' ')
        popupStudent.title(roll[0])
        connect_, cursor_ = ES.get_student_db_ES()
        roll = roll[0]
        cursor_.execute('SELECT * FROM student WHERE roll=(:roll)', {'roll':roll})
        student = cursor_.fetchone()
        cursor_.execute('SELECT * FROM courses_taken WHERE roll=(:roll) AND grade!=(:grade)',{'roll':roll,'grade':'R'})
        allCourses=cursor_.fetchall()

        Label(popupStudent, text='Roll No.').grid(row=1, column=0, sticky=W, padx=10)
        Label(popupStudent, text='Name').grid(row=2, column=0, sticky = W, padx=10)
        Label(popupStudent, text='Address').grid(row=3, column=0, sticky = W, padx=10)
        Label(popupStudent, text='Course').grid(row=4, column=0, sticky = W, padx=10)
        Label(popupStudent, text='Joining Year').grid(row=5, column=0, sticky = W, padx=10)
        Label(popupStudent, text='CGPA').grid(row=6, column=0, sticky = W, padx=10)

        cgpa=self.getCGPA(allCourses)
        
        Label(popupStudent, text=student[0]).grid(row=1, column=1, sticky = W)
        Label(popupStudent, text=student[1]).grid(row=2, column=1, sticky = W)
        Label(popupStudent, text=student[2], anchor=W, justify='left').grid(row=3, column=1, sticky = W)
        Label(popupStudent, text=student[3]).grid(row=4, column=1, sticky = W)
        Label(popupStudent, text=student[4]).grid(row=5, column=1, sticky = W)
        Label(popupStudent, text=str(cgpa)).grid(row=6, column=1, sticky = W)

        Button(popupStudent,text="View Performance",command=lambda:self.viewPerformance(roll,popupStudent,student)).grid(row=7,column=0,columnspan=2)

        popupStudent.columnconfigure(0, weight=1)
        popupStudent.columnconfigure(1, weight=2)
        popupStudent.rowconfigure(0, weight=1)
        popupStudent.rowconfigure(7, weight=2)

    @staticmethod
    def fetchPerformance(roll_no):
        connect_,cursor_=ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM courses_taken WHERE roll=(:roll) AND grade!=(:grade)',{'roll':roll_no,'grade':'R'})
        allCourses=cursor_.fetchall()
        semDict={}
        for i in allCourses:
            if i[3] in semDict:
                semDict[i[3]].append(i)
            else:
                semDict[i[3]]=[i]
    
        cursor_.execute('SELECT sub_code,sem_taken FROM courses_taken WHERE roll=(:roll) AND grade=(:fgrade)',{'roll':roll_no,'fgrade':'F'})
        backlogs=cursor_.fetchall()
        backlogsDict={}
        for i in backlogs:
            backlogsDict[i[0]]=i[1]
        
        return (backlogsDict,semDict)

    def viewPerformance(self,roll_no,popupStudent,student):
        popupStudent.destroy()
        backlogsDict,semDict=self.fetchPerformance(roll_no)
        viewWindow=Tk()
        viewWindow.title(student[0])
        viewWindow.maxsize(700,550)
        viewWindow.minsize(690,500)
        viewWindow.title(student[0])
        
        connect_,cursor_=ES.get_student_db_ES()

        perfView=ScrollableFrame(viewWindow)
        perfView.grid(row=1,column=0,sticky="nsew")

        detailsFrame=Frame(perfView.frame)
        detailsFrame.grid(row=0,column=0,sticky=E+W)

        Label(detailsFrame,text='Name: '+student[1],anchor=W,relief=GROOVE).grid(row=0,column=0,columnspan=2,sticky=W+E)
        Label(detailsFrame,text='Roll no.: '+student[0],anchor=W,relief=GROOVE).grid(row=1,column=0,sticky=W+E)
        Label(detailsFrame,text='Degree: '+student[3],anchor=W,relief=GROOVE).grid(row=1,column=1,sticky=W+E)

        detailsFrame.columnconfigure(0,weight=3)
        detailsFrame.columnconfigure(1,weight=2)

        
        
        backlogsFrame=Frame(perfView.frame)
        backlogsFrame.grid(row=1,column=0,sticky=E+W,pady=10)
        Label(backlogsFrame,text="Backlogs",anchor=W,relief=GROOVE).grid(row=0,column=0,columnspan=4,sticky=E+W)

        if len(backlogsDict)!=0:
            Label(backlogsFrame,text="Course Code",relief=GROOVE,width=12).grid(row=1,column=0,sticky=E+W)
            Label(backlogsFrame,text="Course Name",relief=GROOVE).grid(row=1,column=1,sticky=E+W)
            Label(backlogsFrame,text="Credits",relief=GROOVE,width=12).grid(row=1,column=2,sticky=E+W)
            Label(backlogsFrame,text="Most Recent semester taken in",relief=GROOVE).grid(row=1,column=3,sticky=E+W)
            
            ind=0
            for i in backlogsDict:
                cursor_.execute('SELECT course_name,credits FROM all_courses WHERE sub_code=(:code)',{'code':i})
                info=cursor_.fetchone()
                Label(backlogsFrame,text=str(i),relief=FLAT).grid(row=2+ind,column=0,sticky=E+W)
                Label(backlogsFrame,text=str(info[0]),relief=FLAT).grid(row=2+ind,column=1,sticky=E+W)
                Label(backlogsFrame,text=str(info[1]),relief=FLAT).grid(row=2+ind,column=2,sticky=E+W)
                Label(backlogsFrame,text=str(backlogsDict[i]),relief=FLAT).grid(row=2+ind,column=3,sticky=E+W)
                ind=ind+1
            backlogsFrame.columnconfigure(3,weight=1)
        else:
            Label(backlogsFrame,text="None",anchor=W,relief=GROOVE).grid(row=1,column=0,columnspan=4,sticky=E+W)
        backlogsFrame.columnconfigure(1,weight=1)
        ind=3
        for i in semDict:
            self.semPerformance(perfView,ind,i,semDict[i])
            ind=ind+1

        self.ongoingSemester(student[0],perfView,ind)

        perfView.frame.columnconfigure(0,weight=1)
        
        viewWindow.rowconfigure(1,weight=1)
        viewWindow.columnconfigure(0,weight=1)

        Button(viewWindow,text="Save as PDF",command=lambda:self.savePDF(perfView)).grid(row=2,column=0)

    def semPerformance(self,perfView,row_,semname,courselist):
        connect_,cursor_=ES.get_student_db_ES()

        semFrame=Frame(perfView.frame)
        semFrame.grid(row=row_,column=0,sticky=E+W,pady=10)
        sgpa=self.getCGPA(courselist)
        Label(semFrame,text='Semester: '+semname,relief=GROOVE,anchor=W).grid(row=0,columnspan=3,column=0,sticky=E+W)
        Label(semFrame,text='SGPA '+str(sgpa),relief=GROOVE,anchor=W).grid(row=0,column=3,sticky=E+W)

        Label(semFrame,text='Course code',relief=GROOVE,width=12).grid(row=1,column=0,sticky=E+W)
        Label(semFrame,text='Course name',relief=GROOVE).grid(row=1,column=1,sticky=E+W)
        Label(semFrame,text='Credits',relief=GROOVE,width=12).grid(row=1,column=2,sticky=E+W)
        Label(semFrame,text='Grade',relief=GROOVE,width=12).grid(row=1,column=3,sticky=E+W)

        ind=0
        for i in courselist:
            cursor_.execute('SELECT course_name,credits FROM all_courses WHERE sub_code=(:code)',{'code':i[1]})
            info=cursor_.fetchone()
            grade=i[2]
            if grade=='f':
                grade='F'
            Label(semFrame,text=i[1]).grid(row=2+ind,column=0,sticky=E+W)
            Label(semFrame,text=info[0]).grid(row=2+ind,column=1,sticky=E+W)
            Label(semFrame,text=info[1]).grid(row=2+ind,column=2,sticky=E+W)
            Label(semFrame,text=grade).grid(row=2+ind,column=3,sticky=E+W)
            ind=ind+1

        semFrame.columnconfigure(1,weight=1)

    def ongoingSemester(self,roll_no,perfView,row_):
        connect_,cursor_=ES.get_student_db_ES()
        cursor_.execute('SELECT sub_code,sem_taken FROM courses_taken WHERE roll=(:roll) AND grade=(:grade)',{'roll':roll_no,'grade':'R'})
        courselist=cursor_.fetchall()

        ongoingFrame=Frame(perfView.frame,bg='red')
        ongoingFrame.grid(column=0,row=row_,sticky=E+W,pady=10)
                
        if len(courselist)!=0:
            Label(ongoingFrame,text='Ongoing Semester: '+courselist[0][1],relief=GROOVE,anchor=W).grid(row=0,column=0,columnspan=3,sticky=E+W)
            Label(ongoingFrame,text='Course Code',relief=GROOVE,width=12).grid(row=1,column=0,sticky=E+W)
            Label(ongoingFrame,text='Course Name',relief=GROOVE).grid(row=1,column=1,sticky=E+W)
            Label(ongoingFrame,text='Credits',width=12,relief=GROOVE).grid(row=1,column=2,sticky=E+W)

            ind=0
            for i in courselist:
                cursor_.execute('SELECT course_name,credits FROM all_courses WHERE sub_code=(:code)',{'code':i[0]})
                info=cursor_.fetchone()
                Label(ongoingFrame,text=i[0]).grid(row=2+ind,column=0,sticky=E+W)
                Label(ongoingFrame,text=info[0]).grid(row=2+ind,column=1,sticky=E+W)
                Label(ongoingFrame,text=info[1]).grid(row=2+ind,column=2,sticky=E+W)
                ind=ind+1
        else: 
            Label(ongoingFrame,text='Ongoing Semester: None',relief=GROOVE,anchor=W).grid(row=0,column=0,columnspan=3,sticky=E+W)
        ongoingFrame.columnconfigure(1,weight=1)

    @staticmethod
    def getCGPA(allCourses):
        connect_,cursor_=ES.get_student_db_ES()
        gradesDict={'EX':10,'A':9,'B':8,'C':7,'D':6,'P':5,'F':0,'f':0}
        
        coursesDict={}
        for i in allCourses:
            coursesDict[i[1]]=i[2]
        cgpa=0
        credits=0
        for i in coursesDict:
            cursor_.execute('SELECT credits FROM all_courses WHERE sub_code=(:code)',{'code':i})
            credit=cursor_.fetchone()[0]
            cgpa=cgpa+credit*gradesDict[coursesDict[i]]
            credits=credits+credit
        
        if credits==0:
            return 0
        cgpa=cgpa/credits
        cgpa = "{:.2f}".format(cgpa)
        return cgpa
    
    def savePDF(self,perfView):
        perfView.canvas.postscript(file="tmp.ps", colormode='color')
        process = subprocess.Popen(["ps2pdf", "tmp.ps", "result.pdf"])
        process.wait()
        os.remove("tmp.ps")

    def back(self, root):
        self.clear()
        root.maxsize(800, 600)
        StudentMain.StudentMain(root)

    @staticmethod
    def test():
        print("\nTesting the StudentsView class")
        success = 0
        fail = 0
        allcourses=[('19CS30037', 'CS21003', 'A', 'AUT2020'), 
                ('19CS30037', 'CS21001', 'EX', 'AUT2020'), 
                ('19CS30037', 'CS10001', 'EX', 'AUT2020'), 
                ('19CS30037', 'CS21004', 'F', 'SPR2021'), 
                ('19CS30037', 'CS21002', 'A', 'SPR2021'), 
                ('19CS30037', 'CS20006', 'C', 'SPR2021')]
        
        print("\ta. Computing the CGPA:")
        if StudentsView.getCGPA(allcourses) == str(7.41):
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL")
            fail=fail+1

        backlogsDict,semDict=StudentsView.fetchPerformance('19CS10045')
        print("\tb. Cleared backlog courses not to be shown under Backlog:")
        if len(backlogsDict)==0:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL")
            fail=fail+1
        
        backlogsDict,semDict=StudentsView.fetchPerformance('19CS30037')
        print("\tc. Semesters seperated properly:")
        if len(semDict)==2:
            print("\tPASS")
            success=success+1
        else:
            print("\tFAIL")
            fail=fail+1

        print(f'Test cases passed {success}/{success+fail}')
        print(f'Percentage = {(success/(success+fail))*100}')

if __name__ == '__main__':
    root = Tk()
    root.minsize(400, 300)
    root.maxsize(800, 600)
    root.geometry('800x600')
    StudentsView(root)
