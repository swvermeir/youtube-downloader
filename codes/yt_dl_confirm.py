from tkinter import messagebox, Toplevel, Tk, StringVar
from tkinter.ttk import Frame, Label, Button, OptionMenu, Radiobutton, Combobox


class OptionDialog(Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """
    def __init__(self, parent=None, title=None, choose_message=None, options=None, confirm_message=None):
        Toplevel.__init__(self, parent)
        self.title(title)
        self.choose_message = choose_message
        self.confirm_message = confirm_message
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.options = options
        self.resultVar = StringVar()
        self.result = ""
        self.createWidgets()
        self.grab_set()
        ## wait.window ensures that calling function waits for the window to
        ## close before the result is returned.
        self.wait_window()
        
    def createWidgets(self):
        self['padx'] = 50
        self['pady'] = 15
        padyL = 15
        padyS = 5
        
        # Choose browser
        frmQuestion = Frame(self)
        Label(frmQuestion, text=self.choose_message).grid()
        frmQuestion.grid(row=1, pady=(padyL, padyS))
        
        frmOptions = Frame(self)
        frmOptions.grid(column=0, row=2, pady=(padyS, padyL))
        choice = Combobox(frmOptions, textvariable=self.resultVar, values=self.options, state="readonly")
        choice.grid(column=0, row=2)
        choice.current(0)
        
        if self.confirm_message:
            # Confirm close
            frmConfirm = Frame(self)
            frmConfirm.grid(row=3, pady=(padyL, padyS))
            self.lblConfirm = Label(frmConfirm, text=self.confirm_message.format(result=self.resultVar.get()))
            self.lblConfirm.grid()
            choice.bind("<<ComboboxSelected>>", self.select)
            
            frmButtons = Frame(self)
            frmButtons.grid(row=4, pady=(padyS, padyL))
            
            btnYes = Button(frmButtons, text="Yes", command=self.confirm)
            btnYes.grid(column=0, row=0, padx=5)
            btnNo = Button(frmButtons, text="No", command=self.cancel)
            btnNo.grid(column=1, row=0, padx=5)
        else:
            # Confirm automatically when option is selected
            choice.bind("<<ComboboxSelected>>", self.confirm)

    def select(self, result=None):
        self.lblConfirm.config(text=self.confirm_message.format(result=self.resultVar.get()))
        
    def confirm(self, result=None):
        self.result = self.resultVar.get()
        self.destroy()
        
    def cancel(self):
        self.result = None
        self.destroy()


def confirm(title="Confirm", message="Confirm yes or no"):
    return messagebox.askyesno(title, message)


def choose(title="Choose", message="Choose one of the following", options=None):
    return OptionDialog(title=title, choose_message=message, options=options).result


def choose_confirm(title="Choose", choose_message="Choose one of the following", options=None, confirm_message="Confirm to continue"):
    return OptionDialog(title=title, choose_message=choose_message, options=options, confirm_message=confirm_message).result
    
    
if __name__ == '__main__':
    options = ["a", 'b', 'c']
    choose_confirm(options=options, confirm_message="haha jaja {result} bibi mimi")
