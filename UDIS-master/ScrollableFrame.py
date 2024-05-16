import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, height=340, width=430):
        
        tk.Frame.__init__(self, parent,bg='red')
        tk.Frame.update(self)

        self.canvas = tk.Canvas(self, bd=0,height=340, background="#ffffff",relief='ridge',highlightthickness=0)
        self.frame = tk.Frame(self.canvas,bg="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True)
        self.canvas_frame=self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind('<Configure>',self.FrameWidth)

    def FrameWidth(self,event):
        canvas_width=event.width
        self.canvas.itemconfig(self.canvas_frame,width=canvas_width)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))