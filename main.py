import pyautogui
import time
import threading
from pynput import keyboard
import customtkinter as ctk
import tkinter as tk
import sys, os



rod_in_water = False
debug = False
drag_time = 1
drag_sleep_time = 1
throwtime = 2
start = False
running_thread = None

# Coral Island inspired theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # base, we override with custom colors

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)

def toggle_start_stop():
    global start, rod_in_water
    start = not start

    if not start:
        rod_in_water = False
        try:
            pyautogui.dragTo(100, 100, duration=0.2, button='right')
        except:
            pass

    print("Bot started" if start else "Bot stopped")
    overlay.update_status(start)


def on_key_press(key):
    try:
        if key == keyboard.Key.f10:
            toggle_start_stop()
    except:
        pass


listener = keyboard.Listener(on_press=on_key_press)
listener.start()


class StatusOverlay:
    def __init__(self):
        self.win = tk.Toplevel()

        self.win.withdraw()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-toolwindow", True)
        self.win.attributes("-disabled", True)
        self.win.attributes("-alpha", 0.7)
        self.win.configure(bg="black")
        self.win.attributes("-transparentcolor", "black")

        self.win.deiconify()

        self.win.geometry("130x40+10+10")

        self.label = tk.Label(
            self.win,
            text="STOPPED",
            font=('Arial', 14, "bold"),
            fg="white",
            bg="#b23b3b"  # coral red
        )
        self.label.pack(fill="both", expand=True)

    def update_status(self, active):
        if active:
            self.label.config(text="ACTIVE", bg="#2e8b57")  # sea green
        else:
            self.label.config(text="STOPPED", bg="#b23b3b")


class MyGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Coral Island Fishing Bot")
        self.root.geometry("400x400")

        # === Calm Coral Island Background ===
        self.root.configure(fg_color="#0b6aa1")  # deep teal

        # === Title ===
        title = ctk.CTkLabel(
            self.root,
            text="Coral Island Fishing Bot",
            font=("Arial Rounded MT Bold", 26),
            text_color="#acdce2"  # warm sand
        )
        title.pack(pady=20)

        # === Help Button ===
        help_button = ctk.CTkButton(
            self.root,
            text="Help / Instructions",
            fg_color="#d2aa67",      # muted coral
            hover_color="#a58650",
            text_color="black",
            corner_radius=14,
            command=self.open_help
        )
        help_button.pack(pady=10)

        # === Info Label ===
        info = ctk.CTkLabel(
            self.root,
            text="F10 = Start / Stop",
            font=("Arial", 17),
            text_color="#d9f3f2"  # soft aqua
        )
        info.pack(pady=5)

        # === Rounded Frame ===
        frame = ctk.CTkFrame(
            self.root,
            fg_color="#098fb8",  # ocean blue
            corner_radius=18
        )
        frame.pack(fill="x", padx=40, pady=25)

        # === Throw Time Slider ===
        self.throw_slider = ctk.CTkSlider(
            frame, from_=0.1, to=5.0, number_of_steps=49,
            fg_color="#50aec5", progress_color="#7bc6d0",
            command=self.update_throwtime
        )
        self.throw_label = ctk.CTkLabel(
            frame,
            text=f"Throw Time: {throwtime:.1f}s",
            text_color="#d9f3f2"
        )
        self.throw_label.pack(pady=5)
        self.throw_slider.set(throwtime)
        self.throw_slider.pack(fill="x", pady=5)

        # === Drag Time Slider ===
        self.drag_slider = ctk.CTkSlider(
            frame, from_=0.1, to=5.0, number_of_steps=49,
            fg_color="#4fa3b8", progress_color="#7bc6d0",
            command=self.update_dragtime
        )
        self.drag_label = ctk.CTkLabel(
            frame,
            text=f"Drag Time: {drag_time:.1f}s",
            text_color="#d9f3f2"
        )
        self.drag_label.pack(pady=5)
        self.drag_slider.set(drag_time)
        self.drag_slider.pack(fill="x", pady=5)

        # === Sleep Time Slider ===
        self.sleep_slider = ctk.CTkSlider(
            frame, from_=0.1, to=5.0, number_of_steps=49,
            fg_color="#4fa3b8", progress_color="#7bc6d0",
            command=self.update_sleeptime
        )
        self.sleep_label = ctk.CTkLabel(
            frame,
            text=f"Sleep Time: {drag_sleep_time:.1f}s",
            text_color="#d9f3f2"
        )
        self.sleep_label.pack(pady=5)
        self.sleep_slider.set(drag_sleep_time)
        self.sleep_slider.pack(fill="x", pady=5)

        self.root.after(100, self.check_thread)
        self.root.mainloop()



    def open_help(self):
        help_win = ctk.CTkToplevel(self.root)
        help_win.title("Instructions")
        help_win.geometry("500x450")
        help_win.resizable(False, False)
        help_win.configure(fg_color="#0b1f2e")

        title = ctk.CTkLabel(
            help_win,
            text="Fishing Bot Instructions",
            font=("Arial", 20, "bold"),
            text_color="#f4c095"
        )
        title.pack(pady=15)

        text = (
            "1. Set the game to Borderless Window mode for the overlay to work.\n\n"
            "2. The game MUST run on your PRIMARY monitor.\n"
            "   PyAutoGUI only interacts reliably with the main display.\n\n"
            "3. Throw Time:\n"
            "   Controls how long the casting drag lasts.\n"
            "   Higher values = longer cast.\n\n"
            "4. Drag Time:\n"
            "   Controls how long the reel-in drag lasts.\n"
            "   Higher values = longer pulling.\n\n"
            "5. Sleep Time:\n"
            "   Delay between each reel-in action.\n"
            "   Lower values = shorter time between dragging.\n\n"
            "6. Press F10 to start or stop the bot at any time.\n\n"
        )

        help_textbox = ctk.CTkTextbox(help_win, width=460, height=330)
        help_textbox.pack(padx=20, pady=10)
        help_textbox.insert("0.0", text)
        help_textbox.configure(state="disabled")

    def update_throwtime(self, val):
        global throwtime
        throwtime = float(val)
        self.throw_label.configure(text=f"Throw Time: {throwtime:.1f}s")

    def update_dragtime(self, val):
        global drag_time
        drag_time = float(val)
        self.drag_label.configure(text=f"Drag Time: {drag_time:.1f}s")

    def update_sleeptime(self, val):
        global drag_sleep_time
        drag_sleep_time = float(val)
        self.sleep_label.configure(text=f"Sleep Time: {drag_sleep_time:.1f}s")

    def check_thread(self):
        global running_thread, start

        if start and (running_thread is None or not running_thread.is_alive()):
            overlay.update_status(True)
            running_thread = threading.Thread(target=self.fish, daemon=True)
            running_thread.start()

        if not start:
            overlay.update_status(False)

        self.root.after(100, self.check_thread)

    def fish(self):
        global rod_in_water, start

        while start:
            if not rod_in_water:
                rod_in_water = True
                print("Casting rod...")

                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(0.3)
                pyautogui.dragTo(100, 100, duration=throwtime)

                print("Rod casted.")

            while rod_in_water and start:
                print("Rod in water...")

                try:
                    if (pyautogui.locateOnScreen(resource_path("img/fish_bite_1.png"), confidence=0.9) or
                        pyautogui.locateOnScreen(resource_path("img/fish_bite_2.png"), confidence=0.9) or
                        pyautogui.locateOnScreen(resource_path("img/fish_bite_3.png"), confidence=0.9)):

                        rod_in_water = False
                        print("Fish detected!")

                        pyautogui.dragTo(100, 100, duration=1)
                        time.sleep(0.5)

                        while pyautogui.locateOnScreen(resource_path("img/catch_process.png"), confidence=0.8) and start:
                            print("Reeling fish...")

                            if drag_time < 0.3:
                                pyautogui.mouseDown()
                                time.sleep(drag_time)
                                pyautogui.mouseUp()
                            else:
                                pyautogui.dragTo(100, 100, duration=drag_time)

                            time.sleep(drag_sleep_time)

                except Exception as e:
                    print("Error:", e)
                    time.sleep(0.1)


overlay = StatusOverlay()
MyGUI()
