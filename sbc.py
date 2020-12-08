#!/usr/bin/python3
import tkinter as tk
from tkinter import *
import threading
import time
import subprocess
import configparser
from PIL import Image, ImageTk


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.WIDTH = 480
        self.HEIGHT = 320
        self.title("SBC Project")
        self.geometry("480x320")
        self.resizable(width=False, height=False)
        self.attributes('-fullscreen', True)
        self.config(cursor="none")

        # Images
        self.thermometer_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/thermometer.png"))
        self.flame_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/flame.png"))
        self.cold_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/cold.png"))
        self.humidity_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/humidity.png"))
        self.humidifier_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/humidifier.png"))
        self.settings_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/settings.png"))
        self.up_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/up.png"))
        self.down_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/down.png"))
        self.accept_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/accept.png"))
        self.back_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/back.png"))
        self.empty_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/empty.png"))
        self.exit_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/exit.png"))
        self.logo_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/logo.png"))
        self.off_image = ImageTk.PhotoImage(Image.open("/home/pi/SBCServer/img/off.png"))

        # Actuators state
        self.actuators_state = True

        # Container
        container = tk.Frame(self)
        container.config(bg="black")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frames
        self.frames = {}

        for F in (Monitor, Settings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Monitor")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def close_window(self):
        self.destroy()
        threading.Thread(target=self.set_heater_off).start()
        threading.Thread(target=self.set_humidifier_off).start()

    def set_humidifier_on(self):
        subprocess.run(['/home/pi/SBCServer/scripts/setHumidifierOn.sh'])

    def set_humidifier_off(self):
        subprocess.run(['/home/pi/SBCServer/scripts/setHumidifierOff.sh'])

    def set_heater_off(self):
        subprocess.run(['/home/pi/SBCServer/scripts/setHeaterOff.sh'])

    def set_heater_on(self):
        subprocess.run(['/home/pi/SBCServer/scripts/setHeaterOn.sh'])

    def get_actuators_state(self):
        return self.actuators_state

    def set_actuators_state(self, state):
        self.actuators_state = state


class Monitor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller

        self.temperature = "    --"
        self.get_temperature()
        self.humidity = "    --"
        self.get_humidity()
        self.heater_state = 1
        self.humidifier_state = 1
        self.date = time.strftime('%d/%m/%y - %H:%M:%S')

        # Init Config Data
        self.config = configparser.ConfigParser()
        self.config.read('/home/pi/SBCServer/server.conf')
        self.config_temperature = float(self.config.get('sensor', 'temperature'))
        self.config_humidity = float(self.config.get('sensor', 'humidity'))

        # Time Label
        self.time_label = tk.Label(self)
        self.time_label.config(bg="black", fg="white")
        self.time_label.config(font=("Helvetica", 15, "bold"))
        self.time_label.place(x=150, y=8)

        # Temperature Icon
        temperature_icon = tk.Label(self)
        temperature_icon.config(bg="black")
        temperature_icon.config(image=controller.thermometer_image)
        temperature_icon.place(x=20, y=60)

        # Temperature String
        self.temperature_text = StringVar()
        self.temperature_text.set("25.0ºc")

        # Temperature Label
        self.temperature_label = tk.Label(self)
        self.temperature_label.config(bg="black", fg="white")
        self.temperature_label.config(font=("Helvetica", 60, "bold"), bd=0)
        self.temperature_label.place(x=120, y=55)
        self.temperature_label.config(textvariable=self.temperature_text)

        # Temperature Config Text
        self.temperature_config_text = StringVar()
        self.temperature_config_text.set(str(self.config_temperature) + "ºc")

        # Temperature Config Label
        self.temperature_config_label = tk.Label(self)
        self.temperature_config_label.config(bg="black", fg="green")
        self.temperature_config_label.config(font=("Helvetica", 20, "bold"), bd=0)
        self.temperature_config_label.place(x=185, y=135)
        self.temperature_config_label.config(textvariable=self.temperature_config_text)

        # Flame Label
        self.flame_label = tk.Label(self)
        self.flame_label.config(bg="black")
        self.flame_label.config(image=controller.flame_image)
        self.flame_label.place(x=340, y=40)

        # Humidity Icon
        self.humidity_icon = tk.Label(self)
        self.humidity_icon.config(bg="black")
        self.humidity_icon.config(image=controller.humidity_image)
        self.humidity_icon.place(x=20, y=200)

        # Humidity Text
        self.humidity_text = StringVar()
        self.humidity_text.set("45.0%")

        # Humidity Label
        self.humidity_label = tk.Label(self)
        self.humidity_label.config(bg="black", fg="white")
        self.humidity_label.config(font=("Helvetica", 60, "bold"), bd=0)
        self.humidity_label.place(x=120, y=195)
        self.humidity_label.config(textvariable=self.humidity_text)

        # Humidity Config Text
        self.humidity_config_text = StringVar()
        self.humidity_config_text.set(str(self.config_humidity) + "%")

        # Humidity Config Label
        self.humidity_config_label = tk.Label(self)
        self.humidity_config_label.config(bg="black", fg="green")
        self.humidity_config_label.config(font=("Helvetica", 20, "bold"), bd=0)
        self.humidity_config_label.place(x=185, y=275)
        self.humidity_config_label.config(textvariable=self.humidity_config_text)

        # Humidifier Label
        self.humidifier_label = tk.Label(self)
        self.humidifier_label.config(bg="black")
        self.humidifier_label.config(image=controller.humidifier_image)
        self.humidifier_label.place(x=340, y=180)

        # Settings Button
        settings_button = tk.Button(self)
        settings_button.config(bg="black", activebackground="black")
        settings_button.config(highlightthickness=0, bd=0)
        settings_button.config(image=controller.settings_image)
        settings_button.config(command=lambda: controller.show_frame("Settings"))
        settings_button.place(x=380, y=55, height=90, width=90)

        # Exit Button
        exit_button = tk.Button(self)
        exit_button.config(bg="black", activebackground="black")
        exit_button.config(highlightthickness=0, bd=0)
        exit_button.config(image=controller.exit_image)
        exit_button.config(command=controller.close_window)
        exit_button.place(x=380, y=195, height=90, width=90)

        self.hide_humidifier()
        self.hide_flame()
        self.hide_cold()
        self.update_temperature()
        self.update_humidity()
        self.update_date()

    def update_date(self):
        date = time.strftime('%d/%m/%y - %H:%M:%S')
        self.time_label.config(text=date)
        self.get_config_data()
        self.after(1000, self.update_date)

    def get_temperature(self):
        self.temperature = subprocess.run(['/home/pi/SBCServer/scripts/getTemperature.sh'], stdout=subprocess.PIPE).stdout.decode().rstrip()

    def update_temperature(self):
        if self.controller.actuators_state:
            self.temperature_config_label.config(fg='green')
            t = threading.Thread(target=self.get_temperature)
            t.start()
            self.temperature_text.set(self.temperature + "ºc")
            self.get_config_data()
            if float(self.temperature) + 0.5 < self.config_temperature:
                threading.Thread(target=self.controller.set_heater_on).start()
                self.show_flame()
            else:
                if float(self.temperature) - 0.5 > self.config_temperature:
                    threading.Thread(target=self.controller.set_heater_on).start()
                    self.show_cold()
                else:
                    threading.Thread(target=self.controller.set_heater_off).start()
                    self.hide_flame()
                    self.hide_cold()
        else:
            self.hide_cold()
            self.hide_flame()
            self.temperature_config_label.config(fg='black')
        self.time_label.after(5000, self.update_temperature)

    def get_humidity(self):
        self.humidity = subprocess.run(['/home/pi/SBCServer/scripts/getHumidity.sh'], stdout=subprocess.PIPE).stdout.decode().rstrip()

    def update_humidity(self):
        if self.controller.actuators_state:
            self.humidity_config_label.config(fg='green')
            h = threading.Thread(target=self.get_humidity)
            h.start()
            self.humidity_text.set(self.humidity + "%")
            self.get_config_data()
            if float(self.humidity) + 0.5 < self.config_humidity:
                threading.Thread(target=self.controller.set_humidifier_on).start()
                self.show_humidifier()
            else:
                threading.Thread(target=self.controller.set_humidifier_off).start()
                self.hide_humidifier()
        else:
            self.hide_humidifier()
            self.humidity_config_label.config(fg='black')
        self.humidity_label.after(5000, self.update_humidity)

    def show_flame(self):
        self.flame_label.config(image=self.controller.flame_image)

    def hide_flame(self):
        self.flame_label.config(image=self.controller.empty_image)

    def show_cold(self):
        self.flame_label.config(image=self.controller.cold_image)

    def hide_cold(self):
        self.flame_label.config(image=self.controller.empty_image)

    def show_humidifier(self):
        self.humidifier_label.config(image=self.controller.humidifier_image)

    def hide_humidifier(self):
        self.humidifier_label.config(image=self.controller.empty_image)

    def get_config_data(self):
        self.config.read('/home/pi/SBCServer/server.conf')
        self.config_temperature = float(self.config.get('sensor', 'temperature'))
        self.config_humidity = float(self.config.get('sensor', 'humidity'))
        self.temperature_config_text.set(str(self.config_temperature) + "ºc")
        self.humidity_config_text.set(str(self.config_humidity) + "%")


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="black")
        self.controller = controller

        # Init Config Data
        self.config = configparser.ConfigParser()
        self.config.read('/home/pi/SBCServer/server.conf')
        self.config_temperature = float(self.config.get('sensor', 'temperature'))
        self.config_humidity = float(self.config.get('sensor', 'humidity'))
        self.temperature = self.config_temperature
        self.humidity = self.config_humidity
        # self.temperature_changed = False
        # self.get_config_data()

        # Time Label
        self.time_label = tk.Label(self)
        self.time_label.config(bg="black", fg="white")
        self.time_label.config(font=("Helvetica", 15, "bold"))
        self.time_label.place(x=150, y=8)

        # Temperature Icon
        temperature_icon = tk.Label(self)
        temperature_icon.config(bg="black")
        temperature_icon.config(image=controller.thermometer_image)
        temperature_icon.place(x=20, y=60)

        # Temperature Text
        self.temperature_text = StringVar()
        self.temperature_text.set(str(self.temperature))

        # Temperature Label
        self.temperature_label = tk.Label(self)
        self.temperature_label.config(bg="black", fg="green")
        self.temperature_label.config(font=("Helvetica", 60, "bold"), bd=0)
        self.temperature_label.place(x=120, y=55)
        self.temperature_label.config(textvariable=self.temperature_text)

        # Temperature Up Button
        temperature_up_button = tk.Button(self)
        temperature_up_button.config(bg="black", activebackground="black")
        temperature_up_button.config(highlightthickness=0, bd=0)
        temperature_up_button.config(image=controller.up_image)
        temperature_up_button.config(command=self.increase_temperature)
        temperature_up_button.place(x=300, y=50, height=50, width=50)

        # Temperature Down Button
        temperature_down_button = tk.Button(self)
        temperature_down_button.config(bg="black", activebackground="black")
        temperature_down_button.config(highlightthickness=0, bd=0)
        temperature_down_button.config(image=controller.down_image)
        temperature_down_button.config(command=self.decrease_temperature)
        temperature_down_button.place(x=300, y=100, height=50, width=50)

        # Humidity Icon
        humidity_icon = tk.Label(self)
        humidity_icon.config(bg="black")
        humidity_icon.config(image=controller.humidity_image)
        humidity_icon.place(x=20, y=200)

        # Humidity Text
        self.humidity_text = StringVar()
        self.humidity_text.set(str(self.humidity))

        # Humidity Label
        self.humidity_label = tk.Label(self)
        self.humidity_label.config(bg="black", fg="green")
        self.humidity_label.config(font=("Helvetica", 60, "bold"), bd=0)
        self.humidity_label.place(x=120, y=195)
        self.humidity_label.config(textvariable=self.humidity_text)

        # Humidity Up Button
        humidity_up_button = tk.Button(self)
        humidity_up_button.config(bg="black", activebackground="black")
        humidity_up_button.config(highlightthickness=0, bd=0)
        humidity_up_button.config(image=controller.up_image)
        humidity_up_button.config(command=self.increase_humidity)
        humidity_up_button.place(x=300, y=190, height=50, width=50)

        # Humidity Down Button
        humidity_down_button = tk.Button(self)
        humidity_down_button.config(bg="black", activebackground="black")
        humidity_down_button.config(highlightthickness=0, bd=0)
        humidity_down_button.config(image=controller.down_image)
        humidity_down_button.config(command=self.decrease_humidity)
        humidity_down_button.place(x=300, y=240, height=50, width=50)

        # Accept Button
        accept_button = tk.Button(self)
        accept_button.config(bg="black", activebackground="black")
        accept_button.config(highlightthickness=0, bd=0)
        accept_button.config(image=controller.accept_image)
        accept_button.config(command=self.set_config_data)
        accept_button.place(x=380, y=25, height=90, width=90)

        # Back Button
        back_button = tk.Button(self)
        back_button.config(bg="black", activebackground="black")
        back_button.config(highlightthickness=0, bd=0)
        back_button.config(image=controller.back_image)
        back_button.config(command=lambda: controller.show_frame("Monitor"))
        back_button.place(x=380, y=215, height=90, width=90)

        # Off Button
        off_button = tk.Button(self)
        off_button.config(bg="black", activebackground="black")
        off_button.config(highlightthickness=0, bd=0)
        off_button.config(image=controller.off_image)
        off_button.config(command=lambda: self.manage_actuators(controller))
        off_button.place(x=380, y=120, height=90, width=90)

        self.update_date()

    def update_date(self):
        date = time.strftime('%d/%m/%y - %H:%M:%S')
        self.time_label.config(text=date)
        self.after(1000, self.update_date)

    def check_temperature_change(self):
        if self.config_temperature != self.temperature:
            self.temperature_label.config(fg="red")
        else:
            self.temperature_label.config(fg="green")

    def check_humidity_change(self):
        if self.config_humidity != self.humidity:
            self.humidity_label.config(fg="red")
        else:
            self.humidity_label.config(fg="green")

    def increase_temperature(self):
        if self.temperature != 99.5:
            self.temperature = self.temperature + 0.5
            self.check_temperature_change()
            self.temperature_text.set(str(self.temperature))

    def decrease_temperature(self):
        if self.temperature != 0.0:
            self.temperature = self.temperature - 0.5
            self.check_temperature_change()
            self.temperature_text.set(str(self.temperature))

    def increase_humidity(self):
        if self.humidity != 99.5:
            self.humidity = self.humidity + 0.5
            self.check_humidity_change()
            self.humidity_text.set(str(self.humidity))

    def decrease_humidity(self):
        if self.humidity != 0.0:
            self.humidity = self.humidity - 0.5
            self.check_humidity_change()
            self.humidity_text.set(str(self.humidity))

    def get_config_data(self):
        self.config.read('/home/pi/SBCServer/server.conf')
        self.config_temperature = float(self.config.get('sensor', 'temperature'))
        self.config_humidity = float(self.config.get('sensor', 'humidity'))
        self.temperature = self.config_temperature
        self.humidity = self.config_humidity

    def set_config_data(self):
        self.config.read('/home/pi/SBCServer/server.conf')
        self.config.set('sensor', 'temperature', str(self.temperature))
        self.config.set('sensor', 'humidity', str(self.humidity))

        with open('/home/pi/SBCServer/server.conf', 'w') as configfile:  # save
            self.config.write(configfile)

        self.get_config_data()
        self.check_temperature_change()
        self.check_humidity_change()

    def manage_actuators(self, controller):
        if controller.actuators_state:
            self.temperature_label.config(fg='grey')
            self.humidity_label.config(fg='grey')
            controller.set_actuators_state(False)
            threading.Thread(target=self.controller.set_humidifier_off).start()
            threading.Thread(target=self.controller.set_heater_off).start()
        else:
            self.temperature_label.config(fg='green')
            self.humidity_label.config(fg='green')
            controller.set_actuators_state(True)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
