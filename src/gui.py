from tkinter import *
from tkinter import ttk
from work import MyWork

class MyGui:

    def __init__(self, root):
        '''setting the initial GUI: define different parts to the given grid
        please note: if the variable changes when running the program, then you should define it as a public variable.
        maxvlue: the default number is 100, which could be changing by the user. getting data from the GUI
        progress: from 0-100, getting the data from the backend.
        result: the caculate result. getting the data from the backend.
        '''
        self.rootwnd = root
        root.title("MyGui Example with Background Worker Thread")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
       
        ttk.Label(mainframe, text="Summation from 0 to: ").grid(column=1, row=1, sticky=E)
        self.maxvalue = StringVar(value=100)
        maxentry = ttk.Entry(mainframe, width=7, textvariable=self.maxvalue)
        maxentry.grid(column=2, row=1, sticky=(W, E))
        
        ttk.Label(mainframe, text="Progress (%): ").grid(column=1, row=2, sticky=E)
        self.progress = StringVar()
        ttk.Label(mainframe, textvariable=self.progress).grid(column=2, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="Result: ").grid(column=1, row=3, sticky=E)
        self.sumvalue = StringVar()
        ttk.Label(mainframe, textvariable=self.sumvalue).grid(column=2, row=3, sticky=(W, E))

        self.startbtn = ttk.Button(mainframe, text="Start", command=self.calculate)
        self.startbtn.grid(column=2, row=4, sticky=(W, E, S, N))

        # setting border for all the widgets on the main frame
        for child in mainframe.winfo_children():   
            child.grid_configure(padx=5, pady=5)

        maxentry.focus()
        root.bind("<Return>", self.calculate)

        # https://stackoverflow.com/questions/41912004/how-to-use-tcl-tk-bind-function-on-tkinters-widgets-in-python
        # register an event. using the showprogress function to update progress data, once the passing data has changed from the backend.
        cmd = root.register(self.showprogress)
        root.tk.call("bind", root, "<<ProgressEvent>>", cmd + " %d")
        
        cmd = root.register(self.showresult)
        root.tk.call("bind", root, "<<ResultEvent>>", cmd + " %d")

        # all the widgets prensent adaptively 
        root.columnconfigure(0, weight=1)   
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)
        mainframe.rowconfigure(4, weight=1)

        self.started = False
        
    def calculate(self, *args):
        '''passing and showing the backend data to frontend. if the caculate has been started, then you should not start again.'''
        try:
            if self.started:
                self.work.stop()
                self.startbtn["text"] = "Start"
                self.started = False
            else:
                self.work = MyWork(int(self.maxvalue.get()), self.setprogress, self.setresult)
                self.work.start()
                self.startbtn["text"] = "Stop"
                self.sumvalue.set("")
                self.started = True
        except ValueError:
            pass
    
    def setprogress(self, value):
        '''add an event loop when the value changed and update the value at GUI
        please mind you should register the event at the beginning.
        '''
        self.rootwnd.event_generate("<<ProgressEvent>>", data=value)

    def showprogress(self, value):
        '''update the progress value'''
        self.progress.set(value)

    def setresult(self, value):
        self.rootwnd.event_generate("<<ResultEvent>>", data=value)

    def showresult(self, value):
        self.sumvalue.set(value)
        self.startbtn["text"] = "Start"
        self.started = False