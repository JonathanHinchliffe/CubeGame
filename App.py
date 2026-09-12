import tkinter as tk
import json

class App:

    def __init__(self, settings_loc='settings.json'):
        self.load_settings(settings_loc)
        self.create_root()
        self.main_menu()
        self.root.mainloop()

    def load_settings(self, settings_loc='settings.json'):
        with open(settings_loc, 'r', encoding='utf-8') as file:
            self.settings = json.load(file)
            self.settings["text"] = (self.settings["font"],24)
            self.settings["width"] = int(self.settings["resolution"].split("x")[0])
            self.settings["height"] = int(self.settings["resolution"].split("x")[1])

    def create_root(self):
        self.root = tk.Tk()
        self.root.title(self.settings["app_name"])
        if self.settings["fullscreen"]:
            self.root.attributes("-fullscreen",True)
        else:
            self.root.geometry(self.settings["resolution"])

    def main_menu(self):

        title_label = tk.Label(self.root, text="CUBE GAME", font=(self.settings["font"],48,"bold"))
        title_label.pack()

        user_box = tk.Entry(self.root, width=20)
        if self.settings["user"] == None:
            user_box.insert(0,"Username")
        else:
            user_box.insert(0,self.settings["user"])
        user_box.place(relx=1.0, x=-10, y=10, anchor=tk.NE)

        button_frame = tk.Frame(self.root)
        button_frame.place(relx=0.5, rely=0.45, anchor=tk.N)

        start_button = tk.Button(button_frame, width=12, text="Start Game", font=self.settings["text"])
        start_button.pack()

        settings_button = tk.Button(button_frame, width=12, text="Settings", font=self.settings["text"])
        settings_button.pack(pady=(10,0))

        exit_button = tk.Button(button_frame, width=12, text="Exit", font=self.settings["text"],command=self.root.destroy)
        exit_button.pack(pady=(10,0))

        user_box.bind("<FocusIn>", lambda event, text_box=user_box:clear_placeholder(event=event, text_box=text_box))
        user_box.bind("<FocusOut>", lambda event, text_box=user_box, settings=self.settings:exit_user_box(event=event, text_box=text_box,settings=settings))

def clear_placeholder(event, text_box):
    if text_box.get() == "Username":
        text_box.delete(0,tk.END)

def exit_user_box(event, text_box, settings):
    if text_box.get() == "":
        text_box.insert(0, "Username")
    elif settings["save_user"]:
        settings["user"] = text_box.get()   

app = App()
print(app.settings["resolution"])