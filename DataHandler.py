import sqlite3
import GameObjects as go

class Database_Handler:

    def __init__(self, db_address = "Data/db.sqlite3", load_powerups = True, load_effects = True):
        self.db = sqlite3.connect(db_address)
        if load_powerups:
            self.powerups = self.get_powerups()
        if load_effects:
            self.effects = self.get_effects()

    def get_powerups(self):
        cur = self.db.cursor()
        res = cur.execute("SELECT powerupID, powerup_name FROM Powerups")
        return res.fetchall()

    def get_powerup(self,target):
        target = target.replace("_Powerup", '')
        target = target.replace("_", ' ')
        for id, name in self.powerups:
            #print(f"target: {target}, id: {id}, name: {name}")
            if id == target:
                return name
            if name == target:
                return id

    def get_effects(self):
        cur = self.db.cursor()
        res = cur.execute("SELECT effectID, effect_name FROM Effects")
        return res.fetchall()

    def add_powerup(self, powerup_name):
        cur = self.db.cursor()
        cur.execute(f"INSERT INTO Powerups (powerup_name) VALUES ('{powerup_name}')")
        self.db.commit()

    def add_effect(self,effect_name):
        cur = self.db.cursor()
        cur.execute(f"INSERT INTO Effects (effect_name) VALUES ('{effect_name}')")
        self.db.commit()

    def set_GameRunPowerups(self,powerups, date):
        cur = self.db.cursor()
        values = []
        for powerup in powerups:
            p_name = powerup.__name__
            p_name = p_name.replace("_Powerup", '')
            p_name = p_name.replace("_", ' ')
            #print(self.powerups)
            #print(p_name)
            x = 0
            while x < len(self.powerups):
                if p_name == self.powerups[x][1]:
                    values.append((date, x+1))
                    x += len(self.powerups)+10
                x += 1
            if x < len(self.powerups) + 5:
                self.add_powerup(p_name)
                values.append((date, len(self.powerups)+1))
        if values != []:
            text = "INSERT INTO GameRunPowerups (date, powerupID) VALUES"
            for value in values:
                text += f"('{value[0]}', {value[1]}),"
            text= text[:-1]
            cur.execute(text)
            self.db.commit()

    def set_GameRunEffects(self, effects, date):
        cur = self.db.cursor()
        values = []
        for effect in effects:
            e_name = effect.__class__.__name__
            e_name = e_name.replace("_", ' ')
            x = 0
            while x < len(self.effects):
                if e_name == self.effects[x][1]:
                    values.append((date, x+1))
                    x += len(self.effects)+10
                x += 1
            if x < len(self.effects) + 5:
                self.add_effect(e_name)
                values.append((date, len(self.effects)+1))
        if values != []:
            text = "INSERT INTO GameRunEffects (date, effectID) VALUES"
            for value in values:
                text += f"('{value[0]}', {value[1]}),"
            text= text[:-1]
            cur.execute(text)
            self.db.commit()

    def set_GameRun(self, date, game_version, time_survived, score, collision_object, enemies_alive, total_enemies_spawned):
        cur = self.db.cursor()

        score_per_second = score/time_survived
        time_object_spawned = 0
        if collision_object.__class__ != go.Border:
            time_object_spawned = collision_object.time_spawned
        print(date)
        values = f"('{date}', '{game_version}', '{time_survived}', '{score}', '{score_per_second}','{collision_object.__class__.__name__}', '{time_object_spawned}', {enemies_alive}, {total_enemies_spawned})"
        text = "INSERT INTO GameRun (date, game_version_time, time_survived, score, score_per_second, collision_object, time_object_spawned, enemies_alive, total_enemies_spawned) VALUES " + values 
        cur.execute(text)
        self.db.commit()

    def set_PowerupsActivated(self, date, powerup_data):
        cur = self.db.cursor()

        spawned_list = ""
        activated_list = ""
        ended_list = ""
        for key in powerup_data.keys():
            if powerup_data[key] != []:
                # there is a powerup of this type that has been activated
                for item in powerup_data[key]:
                    if item[0] == "Start Time":
                        continue
                    value = f"('{date}', {self.get_powerup(key)},'{item[0]}'"
                    if item[1] == "On Player Collision Time":
                        value += "),"
                        spawned_list += value
                        continue
                    else:
                        value += f",'{item[1]}'"
                    if item[2] == "End Effect Time":
                        value += "),"
                        activated_list += value
                    else:
                        value += f",'{item[2]}'),"
                        ended_list += value

        if spawned_list != "":
            spawned_list = spawned_list[:-1]
            text = "INSERT INTO PowerupsSpawned (date, powerupID, time_spawned) VALUES " + spawned_list
            cur.execute(text)
        #print(spawned_list)
        if activated_list != "":
            activated_list = activated_list[:-1]
            text = "INSERT INTO PowerupsSpawned (date, powerupID, time_spawned, time_activated) VALUES " + activated_list
            cur.execute(text)
        #print(activated_list)
        if ended_list != "":
            ended_list = ended_list[:-1]
            text = "INSERT INTO PowerupsSpawned (date, powerupID, time_spawned, time_activated, time_ended) VALUES " + ended_list
            cur.execute(text)
        #print(ended_list)
        self.db.commit()

