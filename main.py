import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
import subprocess
import datetime
from util import Util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Recognition System")
        self.main_window.geometry("700x800")
        self.main_window.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5)

        self.create_widgets()

        self.db_dir = './Data/DataBase' 
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.login_path = './Data/Login.csv'

    def create_widgets(self):
        main_frame = ttk.Frame(self.main_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = Util.get_text_label(main_frame, "Face Recognition System", font_size=24)  # Increase font size here
        title_label.pack(pady=20)

        webcam_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove")
        webcam_frame.pack(pady=10)

        self.webcam_label = Util.get_img_label(webcam_frame)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=20)

        self.login_button = Util.get_button(control_frame, "Login", self.login)
        self.login_button.pack(fill=tk.X, pady=10)

        self.register_button = Util.get_button(control_frame, "Register", self.register_new_user)
        self.register_button.pack(fill=tk.X, pady=10)

        self.add_webcam(self.webcam_label)



    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))

        name = output.split(',')[1][:-5]

        if name in ['unknown_person']:
            Util.msg_box('Access Denied', 'Unknown user. Please register or try again.')
        elif name in ['no_persons_found']:
            Util.msg_box('Error', 'No person detected. Please ensure you are visible to the camera.')
        else:
            Util.msg_box('Welcome', f'Access granted, {name}.')
            with open(self.login_path, 'a') as f:
                f.write(f'{name},{datetime.datetime.now()}\n')

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.title("Register New User")
        self.register_window.geometry("800x700")
        self.register_window.configure(bg="#f0f0f0")

        register_frame = ttk.Frame(self.register_window, padding="20")
        register_frame.pack(fill=tk.BOTH, expand=True)

        self.capture_label = Util.get_img_label(register_frame)
        self.capture_label.pack(fill=tk.BOTH, expand=True, pady=10)

        username_frame = ttk.Frame(register_frame)
        username_frame.pack(fill=tk.X, pady=10)

        Util.get_text_label(username_frame, "Enter Username:").pack(side=tk.LEFT, padx=5)
        self.username_entry = Util.get_entry_text(username_frame)
        self.username_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        button_frame = ttk.Frame(register_frame)
        button_frame.pack(pady=20)

        Util.get_button(button_frame, "Accept", self.accept_register_new_user).pack(side=tk.LEFT, padx=5)
        Util.get_button(button_frame, "Try Again", self.try_again_register_new_user).pack(side=tk.LEFT, padx=5)

        self.add_img_to_label(self.capture_label)

    def try_again_register_new_user(self):
        self.register_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.username_entry.get().strip()
        if not name:
            Util.msg_box('Error', 'Please enter a username.')
            return

        cv2.imwrite(os.path.join(self.db_dir, f'{name}.jpg'), self.register_new_user_capture)
        Util.msg_box('Success', 'User registered successfully.')
        self.register_window.destroy()

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
