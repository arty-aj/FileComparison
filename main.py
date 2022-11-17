import os.path
from tkinter import *
from tkinter import Button
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import ctypes

file1_name = ""
file2_name = ""
comparedArray = []


class LineNumbers(Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)

        self.text_widget = text_widget
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
        self.text_widget.bind('<FocusIn>', self.on_key_release)
        self.text_widget.bind('<MouseWheel>', self.on_key_release)

        self.insert(1.0, '1')
        self.configure(state='disabled')

    def on_key_release(self, event=None):
        p, q = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index(END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))

        self.configure(state='normal', width=width)
        self.delete(1.0, END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')


def open_file(file):
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    global file1_name
    global file2_name

    if file == 1:
        file1_name = filedialog.askopenfile(filetypes=filetypes)
        lines = file1_name.readlines()
        for line in lines:
            txt1.insert(END, line)
        file1_name.close()

    if file == 2:
        file2_name = filedialog.askopenfile(filetypes=filetypes)
        lines = file2_name.readlines()
        for line in lines:
            txt2.insert(END, line)
        file2_name.close()

    if file == 3:
        file3_name = filedialog.askopenfile(filetypes=filetypes)
        lines = file3_name.readlines()
        for line in lines:
            txt3.insert(END, line)
        file3_name.close()


# Define a function to clear the input text
def clear_to_text_input(text):
    if text == 1:
        txt1.delete("1.0", "end")
    if text == 2:
        txt2.delete("1.0", "end")
    if text == 3:
        txt3.delete("1.0", "end")


def save_file(text):
    f = asksaveasfile(initialfile='Untitled.txt',
                      defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if text == 1:
        text2save = str(txt1.get(1.0, END))  # starts from `1.0`, not `0.0`
        f.write(text2save)
    if text == 2:
        text2save = str(txt2.get(1.0, END))  # starts from `1.0`, not `0.0`
        f.write(text2save)
    if text == 3:
        text2save = str(txt3.get(1.0, END))  # starts from `1.0`, not `0.0`
        f.write(text2save)
    f.close()


def file_compare():
    compared_array = []
    # print(file2_name.name)
    f1_array = []
    f1 = open(file1_name.name, "r")
    f2_array = []
    f2 = open(file2_name.name, "r")

    for line in f1:
        f1_array.append(line.strip('\n'))
    for line in f2:
        f2_array.append(line.strip('\n'))

    if len(f1_array) >= len(f2_array):
        indexSize = len(f1_array)
        smallestArray = len(f2_array)
        biggestArray = "f1"
    else:
        indexSize = len(f2_array)
        smallestArray = len(f1_array)
        biggestArray = "f2"

    for i in range(0, indexSize):
        if i < smallestArray:
            if f1_array[i] == f2_array[i]:
                compared_array.append(str(i + 1) + ":( )  " + f1_array[i])
            else:
                compared_array.append(str(i + 1) + ":(<-) " + f1_array[i])
                compared_array.append(str(i + 1) + ":(->) " + f2_array[i])
        else:
            if biggestArray == "f1":
                compared_array.append(str(i + 1) + ":(<-) " + f1_array[i])
            elif biggestArray == "f2":
                compared_array.append(str(i + 1) + ":(->) " + f2_array[i])

    # for i in range(len(compared_array)):
    #     print(f"{compared_array[i]}")

    for line in range(len(compared_array)):
        txt3.insert(END, compared_array[line] + "\n")


def quit_window():
    root.destroy()


if __name__ == '__main__':
    # initialize
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
    root = Tk()
    root.title('File Comparison')

    # getting screen width and height of display
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # setting tkinter window size and scaling
    root.geometry("%dx%d" % (width, height))

    root.tk.call('tk', 'scaling', '1.20')
    # icon logo
    root_icon = PhotoImage(file="Images/share-files.png")
    root.iconphoto(False, root_icon)

    # Images for button
    folder_image = PhotoImage(file="Images/folder.png")
    save_image = PhotoImage(file="Images/floppydisk.png")
    clear_image = PhotoImage(file="Images/archeology.png")
    compare_image = PhotoImage(file="Images/sync.png")

    # comparison Button
    Button(root, text='Click Me !', image=compare_image, width=80, height=80,
           command=file_compare).grid(row=0, column=3)

    # File 1 window
    text_area_1 = Text(root, width=10, height=20)
    text_area_1.grid(columnspan=3, row=0, column=0)
    txt1 = Text(text_area_1)
    lines1 = LineNumbers(text_area_1, txt1, width=2)
    lines1.pack(side=LEFT, fill=BOTH)
    txt1.pack(expand=True, fill=BOTH)
    txt1.focus()
    Button(root, text='Click Me !', image=folder_image, width=55, height=55,
           command=lambda: file1_name == open_file(1)).grid(row=1, column=0, sticky=E)
    Button(root, text='Click Me !', image=clear_image, width=55, height=55,
           command=lambda: clear_to_text_input(1)).grid(row=1, column=1)
    Button(root, text='Click Me !', image=save_image, width=55, height=55,
           command=lambda: save_file(1)).grid(row=1, column=2, sticky=W)

    # file 2 window
    text_area_2 = Text(root, width=10, height=20)
    text_area_2.grid(columnspan=3, row=0, column=4)
    txt2 = Text(text_area_2)
    lines2 = LineNumbers(text_area_2, txt2, width=2)
    lines2.pack(side=LEFT, fill=BOTH)
    txt2.pack(expand=True, fill=BOTH)
    txt2.focus()
    Button(root, text='Click Me !', image=folder_image, width=55, height=55,
           command=lambda: file1_name == open_file(2)).grid(row=1, column=4, sticky=E)
    Button(root, text='Click Me !', image=clear_image, width=55, height=55,
           command=lambda: clear_to_text_input(2)).grid(row=1, column=5)
    Button(root, text='Click Me !', image=save_image, width=55, height=55,
           command=lambda: save_file(2)).grid(row=1, column=6, sticky=W)

    # compared file window
    text_area_3 = Text(root, width=10, height=10)
    text_area_3.grid(row=2, column=3)
    txt3 = Text(text_area_3)
    lines3 = LineNumbers(text_area_3, txt3, width=2)
    lines3.pack(side=LEFT, fill=BOTH)
    txt3.pack(expand=True, fill=BOTH)
    txt3.focus()
    Button(root, text='Click Me !', image=folder_image, width=55, height=55,
           command=lambda: file1_name == open_file(3)).grid(row=4, column=2, sticky=E)
    Button(root, text='Click Me !', image=clear_image, width=55, height=55,
           command=lambda: clear_to_text_input(3)).grid(row=4, column=3)
    Button(root, text='Click Me !', image=save_image, width=55, height=55,
           command=lambda: save_file(3)).grid(row=4, column=4, sticky=W)

    # exit button (if needed)
    # Button(root,text="Quit", font=('Comic Sans', 13, 'bold'), command= quit_win).grid(row=10,column=10)

    mainloop()
