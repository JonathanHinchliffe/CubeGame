import tkinter as tk
import json
import DataHandler as dh

class App:

    def __init__(self, settings_loc='settings.json'):
        self.load_settings(settings_loc)
        self.dh = dh.Database_Handler(db_address="db.sqlite3")
        self.create_root()
        self.create_main_menu()
        self.root.mainloop()

    def load_settings(self, settings_loc='settings.json'):
        with open(settings_loc, 'r', encoding='utf-8') as file:
            self.settings = json.load(file)
            self.settings["button_text"] = (self.settings["font"],24)
            self.settings["settings_text"] = (self.settings["font"],18)
            self.settings["settings_text_small"] = (self.settings["font"],12)
            self.settings["width"] = int(self.settings["resolution"].split("x")[0])
            self.settings["height"] = int(self.settings["resolution"].split("x")[1])

    def create_root(self):
        self.root = tk.Tk()
        self.root.title(self.settings["app_name"])
        if self.settings["fullscreen"]:
            self.root.attributes("-fullscreen",True)
        else:
            self.root.geometry(self.settings["resolution"])

    def create_main_menu(self):

        self.title_label = tk.Label(self.root, text="CUBE GAME", font=(self.settings["font"],48,"bold"))
        self.title_label.pack()

        self.user_box = tk.Entry(self.root, width=20)
        if self.settings["user"] == None:
            self.user_box.insert(0,"Username")
        else:
            self.user_box.insert(0,self.settings["user"])
        self.user_box.place(relx=1.0, x=-10, y=10, anchor=tk.NE)

        self.mm_button_frame = tk.Frame(self.root)
        self.mm_button_frame.place(relx=0.5, rely=0.45, anchor=tk.N)

        self.start_button = tk.Button(self.mm_button_frame, width=12, text="Start Game", font=self.settings["button_text"])
        self.start_button.pack()

        to_settings = lambda self=self: self.create_settings_menu() 
        self.settings_button = tk.Button(self.mm_button_frame, width=12, text="Settings", font=self.settings["button_text"], command=to_settings)
        self.settings_button.pack(pady=(10,0))

        self.exit_button = tk.Button(self.mm_button_frame, width=12, text="Exit", font=self.settings["button_text"],command=self.root.destroy)
        self.exit_button.pack(pady=(10,0))

        self.user_box.bind("<FocusIn>", lambda event, text_box=self.user_box:clear_placeholder(event=event, text_box=text_box))
        self.user_box.bind("<FocusOut>", lambda event, text_box=self.user_box, settings=self.settings:exit_user_box(event=event, text_box=text_box,settings=settings))

    def create_settings_menu(self):
        self.mm_button_frame.place_forget()

        self.settings_frame = tk.Frame(self.root, width=int(self.settings["width"]*0.6), height=int(self.settings["height"]*0.8))
        self.settings_frame.pack()

        self.powerup_label = tk.Label(self.settings_frame, text="Powerups", font=self.settings["settings_text"]
                                      ).grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        last_collumn = 2
        row = 0
        self.powerup_buttons = []
        for id, name in sorted(self.dh.powerups):           
            self.powerup_buttons.append(
                tk.Button(self.settings_frame, text=name, font=self.settings["settings_text_small"], bg="green2")
            )
            self.powerup_buttons[-1].grid(row=0, column=last_collumn+1, padx=5,pady=10)
            func = lambda num = id-1: toggle_button(self.powerup_buttons[num])
            self.powerup_buttons[-1].config(command=func)
            last_collumn += 1
            if last_collumn == 5:
                row+= 1
                last_collumn = 2
        if last_collumn != 2:
            row+= 1
        self.effects_label = tk.Label(self.settings_frame, text="Effects", font=self.settings["settings_text"]
                                      ).grid(row=row,column=0,columnspan=2,padx=10,pady=10)
        last_collumn=2
        self.effect_buttons = []
        for id, name in sorted(self.dh.effects):
            self.effect_buttons.append(
                tk.Button(self.settings_frame, text=name, font=self.settings["settings_text_small"], bg="green2")
            )
            self.effect_buttons[-1].grid(row=1, column=last_collumn+1, padx=5,pady=10)
            func = lambda num = id-1: toggle_button(self.effect_buttons[num])
            self.effect_buttons[-1].config(command=func)
            last_collumn += 1
            if last_collumn == 5:
                row+= 1
                last_collumn = 2

def clear_placeholder(event, text_box):
    if text_box.get() == "Username":
        text_box.delete(0,tk.END)

def exit_user_box(event, text_box, settings):
    if text_box.get() == "":
        text_box.insert(0, "Username")
    elif settings["save_user"]:
        settings["user"] = text_box.get()   

def toggle_button(button):
    if button.cget("bg") == "green2":
        button.config(bg="red")
    else:
        button.config(bg="green2")

app = App()
print(app.settings["resolution"])