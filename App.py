import tkinter as tk
import json
import DataHandler as dh
import GameObjects as go

class App:

    def __init__(self, settings_loc='settings.json'):
        self.dh = dh.Database_Handler()
        self.load_settings(settings_loc)
        self.create_root()
        self.startup_logic()
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
            self.settings["powerups"] = []
            for p in sorted(self.dh.get_powerups()):
                self.settings["powerups"].append([p[0],p[1],True])
            self.settings["effects"] = []
            for e in sorted(self.dh.get_effects()):
                self.settings["effects"].append([e[0],e[1],True])
            self.settings["frames"] = dict()           

    def create_root(self):
        self.root = tk.Tk()
        self.root.title(self.settings["app_name"])
        if self.settings["fullscreen"]:
            self.root.attributes("-fullscreen",True)
        else:
            self.root.geometry(self.settings["resolution"])

    def create_main_menu(self):

        self.header_frame = tk.Frame(self.root)
        display = lambda self = self: self.header_frame.pack(fill="x")
        display()
        self.settings["frames"]["header_frame"] = dict(name = self.header_frame, display = display)

        self.title_label = tk.Label(self.header_frame, text="CUBE GAME", font=(self.settings["font"],48,"bold"))
        self.title_label.pack()


        self.user_box = tk.Entry(self.header_frame, width=20)
        if self.settings["user"] == None:
            self.user_box.insert(0,"Username")
        else:
            self.user_box.insert(0,self.settings["user"])
        self.user_box.place(relx=1.0, x=-10, y=10, anchor=tk.NE)

        self.mm_button_frame = tk.Frame(self.root)
        display = lambda self = self: self.mm_button_frame.place(relx=0.5, rely=0.45, anchor=tk.N)
        display()
        self.settings["frames"]["mm_button_frame"] = dict(name = self.mm_button_frame, display = display)

        start_game = lambda self=self: self.to_game_screen()
        self.start_button = tk.Button(self.mm_button_frame, width=12, text="Start Game", font=self.settings["button_text"], command=start_game)
        self.start_button.pack()

        to_settings = lambda self=self: self.to_settings_menu() 
        self.settings_button = tk.Button(self.mm_button_frame, width=12, text="Settings", font=self.settings["button_text"], command=to_settings)
        self.settings_button.pack(pady=(10,0))

        self.exit_button = tk.Button(self.mm_button_frame, width=12, text="Exit", font=self.settings["button_text"],command=self.root.destroy)
        self.exit_button.pack(pady=(10,0))

        self.user_box.bind("<FocusIn>", lambda event, text_box=self.user_box:clear_placeholder(event=event, text_box=text_box))
        self.user_box.bind("<FocusOut>", lambda event, text_box=self.user_box, settings=self.settings:exit_user_box(event=event, text_box=text_box,settings=settings))

        self.main_menu_created = True

    def create_settings_menu(self):

        self.settings_frame = tk.Frame(self.root, width=int(self.settings["width"]*0.6), height=int(self.settings["height"]*0.8))
        display = lambda self = self: self.settings_frame.pack()
        display()
        self.settings["frames"]["settings_frame"] = dict(name = self.settings_frame, display = display)

        self.settings_to_mm_button = tk.Button(self.settings_frame, text="Main Menu", font=self.settings["settings_text_small"])
        self.settings_to_mm_button.grid(row=0, column=0,padx=10,pady=10)
        func = lambda self=self: self.to_main_menu()
        self.settings_to_mm_button.config(command=func)
        self.settings_title_label = tk.Label(self.settings_frame, text="Settings", font=self.settings["settings_text"]
                                             ).grid(row=0, column=1, columnspan=4, padx=10, pady=10)
        row = 2
        self.filler_label = tk.Label(self.settings_frame, text="").grid(row=1,column=0,columnspan=5,padx=10,pady=10)
        self.powerup_label = tk.Label(self.settings_frame, text="Powerups", font=self.settings["settings_text"]
                                      ).grid(row=row,column=0,columnspan=2,padx=10,pady=10)
        last_collumn = 2
        
        self.powerup_buttons = []
        for id, name in sorted(self.dh.powerups):           
            self.powerup_buttons.append(
                tk.Button(self.settings_frame, text=name, font=self.settings["settings_text_small"], bg="green2")
            )
            self.powerup_buttons[-1].grid(row=row, column=last_collumn+1, padx=5,pady=10)
            func = lambda self = self, id = id, type="powerups": self.toggle_button(self.powerup_buttons[id-1], id, type)
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
            self.effect_buttons[-1].grid(row=row, column=last_collumn+1, padx=5,pady=10)
            func = lambda self = self,id = id, type="effects": self.toggle_button(self.effect_buttons[id-1], id, type)
            self.effect_buttons[-1].config(command=func)
            last_collumn += 1
            if last_collumn == 5:
                row+= 1
                last_collumn = 2
        self.settings_menu_created = True

    def create_game_screen(self):
        self.game_screen_frame = tk.Frame(self.root)
        display = lambda self = self: self.game_screen_frame.pack(fill="both")
        display()
        self.settings["frames"]["game_screen_frame"] = dict(name = self.game_screen_frame, display = display)

        self.canvas = tk.Canvas(self.game_screen_frame, width=self.settings["width"], height=self.settings["height"], bg="white")
        self.canvas.pack()
        self.game_screen_created = True

    def hide_everything(self):
        for key, value in self.settings["frames"].items():
            if "mm_button" in key:
                value["name"].place_forget()
            else:
                value["name"].pack_forget()

    def to_settings_menu(self):
        self.hide_everything()
        self.settings["frames"]["header_frame"]["display"]()
        if self.settings_menu_created:           
            self.settings["frames"]["settings_frame"]["display"]()
        else:
            self.create_settings_menu()

    def to_main_menu(self):
        self.hide_everything()
        if self.main_menu_created:
            self.settings["frames"]["header_frame"]["display"]()
            self.settings["frames"]["mm_button_frame"]["display"]()
        else:
            self.create_main_menu()

    def to_game_screen(self):
        self.hide_everything()
        if self.game_screen_created:
            self.settings["frames"]["game_screen_frame"]["display"]()
        else:
            self.create_game_screen()
        self.start_game()

    def start_game(self):
        powerups = []
        for p in self.settings["powerups"]:
            if p[2]:
                name = p[1].replace(" ","_")
                name += "_Powerup"
                powerups.append(getattr(go, name))
        powerups = tuple(powerups)
        effects = []
        for e in self.settings["effects"]:
            if e[2]:
                name = e[1].replace(" ", "_")
                effects.append(getattr(go,name)())
        effects = tuple(effects)
        self.game = go.Game(self.canvas, effects=effects, enemy_types=(go.Cube), powerups=powerups)
        self.root.bind("<Motion>", lambda event, objects=self.game.objects: self.game.player.position_update(event=event, objects=objects))
        self.root.update()
        self.game.start_game()

    def toggle_button(self, button, id=-1, type=""):
        if button.cget("bg") == "green2":
            button.config(bg="red")
            if id != -1 and type != "":
                self.settings[type][id-1][2] = False
        else:
            button.config(bg="green2")
            if id != -1 and type != "":
                self.settings[type][id-1][2] = True

    def startup_logic(self):
        self.main_menu_created = False
        self.settings_menu_created = False
        self.game_screen_created = False

def clear_placeholder(event, text_box):
    if text_box.get() == "Username":
        text_box.delete(0,tk.END)

def exit_user_box(event, text_box, settings):
    if text_box.get() == "":
        text_box.insert(0, "Username")
    elif settings["save_user"]:
        settings["user"] = text_box.get()   
