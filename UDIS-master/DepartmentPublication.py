from tkinter import *
import DepartmentResearch
from ScrollableFrame import ScrollableFrame
import ES
import PublicationNew
from PIL import Image, ImageTk

class DepartmentPublication(DepartmentResearch.DepartmentResearch):
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


        root.title('UDIS-Department-Academics-Publications')
        super().__init__(root)
        self.display()
        root.mainloop()

    def display(self):
        self.displayAll.destroy()
        self.displayAll = ScrollableFrame(self.frame)
        self.displayAll.grid(row=0, column=0, padx=30, sticky=N+S+E+W)
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM publications')
        allPublications = cursor_.fetchall()
        Label(self.displayAll.frame, text='Sr. No.', relief=GROOVE).grid(row=0, column=0, sticky=E+W)
        Label(self.displayAll.frame, text='Author', relief=GROOVE).grid(row=0, column=1, sticky=E+W)
        Label(self.displayAll.frame, text='Name', relief=GROOVE).grid(row=0, column=2, sticky=E+W)
        Label(self.displayAll.frame, text='Date', relief=GROOVE).grid(row=0, column=3, sticky=E+W)

        for i in range(len(allPublications)):
            Label(self.displayAll.frame, anchor=W, text=i+1).grid(row=i+1, column=0, sticky=E+W, padx=2, pady=2)
            Label(self.displayAll.frame, anchor=W, text=allPublications[i][0]).grid(row=i+1, column=1, sticky=E+W, padx=2, pady=2)
            publicationName = Label(self.displayAll.frame, anchor=W, text=allPublications[i][1])
            publicationName.grid(row=i+1, column=2, sticky=E+W, padx=2, pady=2)
            Label(self.displayAll.frame, anchor=W, text=allPublications[i][2]).grid(row=i+1, column=3, sticky=E+W, padx=2, pady=2)
            publicationName.bind('<Button-1>', self.bindingAction)

        self.displayAll.frame.columnconfigure(2, weight=2)
        self.displayAll.frame.columnconfigure(1, weight=1)

    def bindingAction(self, event):
        popupPublication = Tk()
        popupPublication.geometry('400x300')
        publicationName = event.widget.cget('text')
        popupPublication.title(publicationName)
        connect_, cursor_ = ES.get_student_db_ES()
        cursor_.execute('SELECT * FROM publications WHERE pub_name=(:name)', {'name':publicationName})
        publication = cursor_.fetchone()

        Label(popupPublication, text='Author').grid(row=1, column=0, sticky=W, padx=10)
        Label(popupPublication, text='Name').grid(row=2, column=0, sticky=W, padx=10)
        Label(popupPublication, text='Date').grid(row=3, column=0, sticky=W, padx=10)

        Label(popupPublication, text=publication[0]).grid(row=1, column=1, sticky=W)
        Label(popupPublication, text=publication[1]).grid(row=2, column=1, sticky=W)
        Label(popupPublication, text=publication[2]).grid(row=3, column=1, sticky=W)

    def new(self, root):
        self.clear()
        PublicationNew.PublicationNew(root)

    @staticmethod
    def test():
        connect_, cursor_ = ES.get_student_db_ES()
        print('Testing the DepartmentPublication Class\n')
        success = 0
        fail = 0
        print('a. Some fields are left empty')
        try :
            PublicationNew.PublicationNew.addpublication('Heuristic search through islands', 'Partha Pratim Chakraborty', '')
            fail+=1
            print('\tFAIL')
        except Exception:
            print('\tPASS')
            success+=1

        try :
            PublicationNew.PublicationNew.addpublication('', 'Partha Pratim Chakraborty', '2009')
            fail+=1
            print('\tFAIL')
        except Exception:
            print('\tPASS')
            success+=1

        print('b. Publication already exists')
        try :
            PublicationNew.PublicationNew.addpublication('Automatic Detection of Human Fall', 'C. Mandal', '2007')
            fail+=1
            print('\tFAIL')
        except Exception:
            print('\tPASS')
            success+=1

        print('c. Happy path test')
        try :
            PublicationNew.PublicationNew.addpublication('Heuristic search through islands', 'Partha Pratim Chakraborty', '2009')
            cursor_.execute('SELECT * FROM publications WHERE pub_name=(:name)', {'name': 'Heuristic search through islands'})
            results = cursor_.fetchall()
            if not len(results) == 1:
                print('\tFAIL')
                fail+=1
            elif not (results[0][0] == 'Partha Pratim Chakraborty' and results[0][1] == 'Heuristic search through islands' and results[0][2] == '2009'):
                print('\tFAIL')
                fail+=1
            else:
                print('\tPASS')
                success+=1
        except Exception as e:
            print("\tFAIL")
            fail+=1

        print(f'Test cases passed {success}/{success + fail}')
        print(f'Percentage = {(success / (success + fail)) * 100}')


if __name__ == '__main__':
    DepartmentPublication.test()