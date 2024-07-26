from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class MainWindow():

    def __init__(self):
        self.window_width = 1280
        self.window_height = 720

        self.window = Tk()
        self.window.title("Craig Calculator")
        self.window.geometry(f"{self.window_width}x{self.window_height}") 
        self.window.configure(bg = "#c7cbd1")

        self.craig_height = 66
        self.selection_height = 74

        self.canvas = Canvas(self.window, width = self.window_width, height = self.window_height - 49, background=self.window["bg"], highlightthickness=0)
        self.canvas.pack(side=BOTTOM)

        self.clicked = StringVar()
        self.clicked.set("Custom")
        self.option_menu = OptionMenu(self.window, self.clicked, "Custom", "Joey Shea", "Shaquille O'Neal", "Basketball Hoop", "Eiffel Tower", "Peter Griffin", command=self.UpdateButton)
        self.option_menu.configure(bg="#b4b8bf", highlightbackground="#000000", highlightcolor="#000000")
        self.option_menu.pack(side=LEFT, padx=(7, 0), anchor=N, pady=(7, 0))

        self.inches_entry = Entry(self.window)
        self.inches_entry.configure(width=5)
        self.inches_entry.bind("<Return>", self.UpdateHeight) 
        self.inches_entry.pack(side=RIGHT, padx=(0, 7), anchor=N, pady=(7, 0))

        self.inches_entry_label = Label(self.window, text="inches", background=self.window["bg"])
        self.inches_entry_label.pack(side=RIGHT, padx=(4, 0), anchor=N, pady=(7, 0))

        self.feet_entry = Entry(self.window)
        self.feet_entry.configure(width=5)
        self.feet_entry.bind("<Return>", self.UpdateHeight)
        self.feet_entry.pack(side=RIGHT, anchor=N, pady=(7, 0))

        self.feet_entry_label = Label(self.window, text="feet", background=self.window["bg"])
        self.feet_entry_label.pack(side=RIGHT, anchor=N, pady=(7, 0))
        
        self.LoadImages()

    def LoadImages(self):
        self.craig_image = Image.open("Assets/Craig.png")
        self.craig_image = self.craig_image.resize((round((self.canvas.winfo_reqheight() / 2) * self.craig_image.width / self.craig_image.height), round(self.canvas.winfo_reqheight() / 2)))
        self.craig_imageTk = ImageTk.PhotoImage(self.craig_image)

        self.person_image = Image.open("Assets/Custom.png")
        self.person_image = self.person_image.resize((round(self.person_image.size[0] * (self.craig_image.size[1] * self.selection_height / (self.craig_height)) / self.person_image.size[1]), round(self.craig_image.size[1] * self.selection_height / (self.craig_height))))
        self.person_imageTk = ImageTk.PhotoImage(self.person_image)

        # 5 ft 6.75 in = 315 pixels
        self.canvas.create_image(self.canvas.winfo_reqwidth() / 40 * 17, self.canvas.winfo_reqheight() - self.craig_image.size[1] - 50, anchor = N, image = self.craig_imageTk)
        self.canvas.create_image(self.canvas.winfo_reqwidth() / 40 * 23, self.canvas.winfo_reqheight() - self.person_image.size[1] - 50, anchor = N, image = self.person_imageTk)

    def UpdateButton(self, arg = None):
        selection = self.clicked.get()
        if selection == "Custom":
            self.UpdateImage("Assets/Custom.png", self.selection_height)  # Adjust height as needed
        elif selection == "Joey Shea":
            self.UpdateImage("Assets/Joey Shea.png", 76 + 2)
        elif selection == "Shaquille O'Neal":
            self.UpdateImage("Assets/Shaquille O'Neal.png", 85)
        elif selection == "Basketball Hoop":
            self.UpdateImage("Assets/Basketball Hoop.png", 156 - 12)
        elif selection == "Eiffel Tower":
            self.UpdateImage("Assets/Eiffel Tower.png", 12996)
        elif selection == "Peter Griffin":
            self.UpdateImage("Assets/Peter Griffin.png", 72 + 2)

    def UpdateHeight(self, arg = None):
        
        try:
            self.selection_height = float(self.feet_entry.get().strip()) * 12 + float(self.inches_entry.get().strip())
        except:
            try:
                self.selection_height = float(self.feet_entry.get().strip()) * 12
            except:
                try:
                    self.selection_height = float(self.inches_entry.get().strip())
                except:
                    self.selection_height = 74

        
        if self.clicked.get() == "Custom":
            try:
                self.UpdateImage("Assets/Custom.png", self.selection_height)
            except:
                self.UpdateImage("Assets/Custom.png", 74)

    def UpdateImage(self, image_file, height_in_inches):
        self.person_image = Image.open(image_file)
        self.craig_image = Image.open("Assets/Craig.png")
        self.craig_image = self.craig_image.resize((round((self.canvas.winfo_reqheight() / 2) * self.craig_image.width / self.craig_image.height), round(self.canvas.winfo_reqheight() / 2)))

        if round(self.craig_image.size[1] * height_in_inches / (self.craig_height)) < self.canvas.winfo_reqheight() - 100:
            # Image Smaller Than Height
            self.person_image = self.person_image.resize((round(self.person_image.size[0] * (self.craig_image.size[1] * height_in_inches / (self.craig_height)) / self.person_image.size[1]), round(self.craig_image.size[1] * height_in_inches / (self.craig_height))))
        else:
            # Image Bigger Than Height
            self.person_image = self.person_image.resize((round((self.canvas.winfo_reqheight() - 50) * self.person_image.size[0] / self.person_image.size[1]), round(self.canvas.winfo_reqheight() - 50)))
            if round((self.craig_height / height_in_inches * self.person_image.height) * self.craig_image.width / self.craig_image.height) > 0:
                self.craig_image = self.craig_image.resize((round((self.craig_height / height_in_inches * self.person_image.height) * self.craig_image.width / self.craig_image.height), round(self.craig_height / height_in_inches * self.person_image.height)))
            else:
                self.craig_image = self.craig_image.resize((1, 2))

        self.craig_imageTk = ImageTk.PhotoImage(self.craig_image)
        self.canvas.create_image(self.canvas.winfo_reqwidth() / 40 * 17, self.canvas.winfo_reqheight() - self.craig_image.size[1] - 50, anchor = N, image = self.craig_imageTk)
        self.person_imageTk = ImageTk.PhotoImage(self.person_image)
        self.canvas.create_image(self.canvas.winfo_reqwidth() / 40 * 23, self.canvas.winfo_reqheight() - self.person_image.size[1] - 50, anchor = N, image = self.person_imageTk)


mw = MainWindow()
mw.window.mainloop()