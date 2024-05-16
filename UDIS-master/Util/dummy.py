# importing tkinter.ttk 
from tkinter import *
from tkinter.ttk import * 
  
# creating root 
root = Tk() 
  
# label text 
Label(root, text ='Select Programming language of your choice').place(x = 20, y = 0) 
  
# check buttons 
java = Checkbutton(root, text ='Java', 
                   takefocus = 0).place(x = 40, y = 30) 
  
cpp = Checkbutton(root, text ='C++', 
                  takefocus = 0).place(x = 40, y = 50) 
  
python = Checkbutton(root, text ='Python', 
                     takefocus = 0).place(x = 40, y = 70) 
  
c = Checkbutton(root, text ='C', 
                takefocus = 0).place(x = 40, y = 90) 

root.mainloop()