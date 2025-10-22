import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import sys
import subprocess
from PIL import Image, ImageTk

# Global variables
selected_points = []
selected_images = []
data_file = "password_data.json"
user_data_file = "user_data.json"
current_image_index = 0
canvas = None
window = None
TOLERANCE = 10
locked_file_path = None
locked_folder_path = None

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)





def save_user_credentials(email, password):
    data = {"email": email, "password": password}
    with open(user_data_file, "w") as f:
        json.dump(data, f)


def validate_user(email, password):
    try:
        with open(user_data_file, "r") as f:
            stored_data = json.load(f)
        return stored_data["email"] == email and stored_data["password"] == password
    except FileNotFoundError:
        return False


def show_home():
    for widget in app.winfo_children():
        widget.destroy()

    home_frame = tk.Frame(app)
    home_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(home_frame, text="Graphical Password Authentication", font=("Arial", 35, "bold")).pack(pady=10)

    try:
        image_path = resource_path("C:\FINAL-PROJECT\lock.PNG")  # Adjust filename if needed
        lock_image = tk.PhotoImage(file=image_path)
        lock_image = lock_image.subsample(4, 4)
        image_label = tk.Label(home_frame, image=lock_image)
        image_label.image = lock_image  # Keep a reference
        image_label.pack()
    except Exception as e:
        tk.Label(home_frame, text="[Image missing: lock.png]", font=("Arial", 12), fg="red").pack(pady=5)

    tk.Button(home_frame, text="Register", command=show_register, font=("Arial", 16),
              width=15, height=2, bg="#4CAF50", fg="white").pack(pady=10)

    tk.Button(home_frame, text="Login", command=show_login, font=("Arial", 16),
              width=15, height=2, bg="#008CBA", fg="white").pack(pady=10)

    tk.Button(home_frame, text="Exit", command=app.quit, font=("Arial", 16),
              width=15, height=2, bg="red", fg="white").pack(pady=10)



def show_register():
    for widget in app.winfo_children():
        widget.destroy()

    frame = tk.Frame(app)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Register With Mail", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(frame, text="Email:", font=("Arial", 15)).pack(pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 15)).pack(pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 12), show="*", width=30)
    password_entry.pack(pady=5)

    def submit():
        email = email_entry.get()
        password = password_entry.get()
        if not email or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return
        save_user_credentials(email, password)
        messagebox.showinfo("Success", "Registration Successful! Now set your graphical password.")
        select_images()

    tk.Button(frame, text="Submit", font=("Arial", 12), command=submit, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(frame, text="Exit", font=("Arial", 12), command=app.quit, bg="red", fg="white").pack(pady=10)


def show_login():
    for widget in app.winfo_children():
        widget.destroy()

    frame = tk.Frame(app)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(frame, text="Email:", font=("Arial", 12)).pack(pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(frame, font=("Arial", 12), show="*", width=30)
    password_entry.pack(pady=5)

    def submit():
        email = email_entry.get()
        password = password_entry.get()
        if validate_user(email, password):
            authenticate()
        else:
            messagebox.showerror("Error", "Invalid credentials! Try again.")

    tk.Button(frame, text="Submit", font=("Arial", 12), command=submit, bg="#008CBA", fg="white").pack(pady=10)
    tk.Button(frame, text="Exit", font=("Arial", 12), command=app.quit, bg="red", fg="white").pack(pady=10)


def select_images():
    global selected_images
    files = filedialog.askopenfilenames(title="Select 5 Images", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if len(files) != 5:
        messagebox.showerror("Error", "You must select exactly 5 images!")
        return
    selected_images = list(files)
    show_image_selection()


def show_image_selection():
    global current_image_index, selected_points, window, canvas
    selected_points = []
    current_image_index = 0

    window = tk.Toplevel(app)
    window.title("Select Cued Points")
    window.attributes('-fullscreen', True)

    top_frame = tk.Frame(window, bg="white")
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Select cued points", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=10)

    canvas = tk.Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    tk.Button(window, text="Exit", font=("Arial", 14), bg="red", fg="white", command=window.destroy).pack(pady=10, side="bottom")

    def next_image(event):
        global current_image_index
        x, y = event.x, event.y
        selected_points.append((x, y))
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
        canvas.update()

        if len(selected_points) == 5:
            data = {"image_paths": selected_images, "password_points": selected_points}
            with open(data_file, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "Graphical password set successfully!")
            window.destroy()
            show_file_folder_window(lock_mode=True)
            return

        current_image_index += 1
        if current_image_index < 5:
            load_image()

    def load_image():
        canvas.delete("all")
        img = Image.open(selected_images[current_image_index])
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_rectangle(0, 0, img_tk.width(), img_tk.height(), outline="blue", width=5)
        canvas.create_image(img_tk.width()//2, img_tk.height()//2, image=img_tk)
        canvas.image = img_tk
        canvas.bind("<Button-1>", next_image)

    load_image()


def authenticate():
    try:
        with open(data_file, "r") as f:
            stored_data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "No password setup found!")
        return

    selected_images = stored_data["image_paths"]
    stored_points = stored_data["password_points"]

    global current_image_index, selected_points, window, canvas
    selected_points = []
    current_image_index = 0

    window = tk.Toplevel(app)
    window.title("Authenticate")
    window.attributes('-fullscreen', True)

    top_frame = tk.Frame(window, bg="white")
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Select cued points", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=10)

    canvas = tk.Canvas(window, bg="white")
    canvas.pack(fill="both", expand=True)

    tk.Button(window, text="Exit", font=("Arial", 14), bg="red", fg="white", command=window.destroy).pack(pady=10, side="bottom")

    def next_image(event):
        global current_image_index
        x, y = event.x, event.y
        selected_points.append((x, y))
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
        canvas.update()

        if len(selected_points) == 5:
            for i in range(5):
                sx, sy = stored_points[i]
                cx, cy = selected_points[i]
                if not (abs(sx - cx) <= TOLERANCE and abs(sy - cy) <= TOLERANCE):
                    messagebox.showerror("Error", "Authentication Failed!")
                    window.destroy()
                    show_home()
                    return

            messagebox.showinfo("Success", "Authentication Successful!")
            window.destroy()
            show_file_folder_window(lock_mode=False)
            return

        current_image_index += 1
        if current_image_index < 5:
            load_image()

    def load_image():
        canvas.delete("all")
        img = Image.open(selected_images[current_image_index])
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_rectangle(0, 0, img_tk.width(), img_tk.height(), outline="blue", width=5)
        canvas.create_image(img_tk.width()//2, img_tk.height()//2, image=img_tk)
        canvas.image = img_tk
        canvas.bind("<Button-1>", next_image)

    load_image()


def show_file_folder_window(lock_mode=True):
    global locked_file_path, locked_folder_path

    window = tk.Toplevel(app)
    window.attributes('-fullscreen', True)
    window.title("File/Folder Access")

    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title = "Lock File/Folder" if lock_mode else "Unlock File/Folder"
    tk.Label(frame, text=title, font=("Arial", 18, "bold")).pack(pady=10)

    def lock_file():
        global locked_file_path
        file_path = filedialog.askopenfilename(title="Select File to Lock")
        if file_path:
            try:
                subprocess.run(["attrib", "+h", file_path], shell=True)
                locked_file_path = file_path
                messagebox.showinfo("Locked", f"File locked: {file_path}")
                window.destroy()
                show_home()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to lock file: {str(e)}")

    def lock_folder():
        global locked_folder_path
        folder_path = filedialog.askdirectory(title="Select Folder to Lock")
        if folder_path:
            try:
                subprocess.run(["attrib", "+h", folder_path], shell=True)
                locked_folder_path = folder_path
                messagebox.showinfo("Locked", f"Folder locked: {folder_path}")
                window.destroy()
                show_home()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to lock folder: {str(e)}")

    def unlock_file():
        global locked_file_path
        if locked_file_path:
            try:
                subprocess.run(["attrib", "-h", locked_file_path], shell=True)
                messagebox.showinfo("Unlocked", f"File unlocked: {locked_file_path}")
                locked_file_path = None
                window.destroy()
                show_home()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to unlock file: {str(e)}")
        else:
            messagebox.showwarning("No File", "No file has been locked in this session.")

    def unlock_folder():
        global locked_folder_path
        if locked_folder_path:
            try:
                subprocess.run(["attrib", "-h", locked_folder_path], shell=True)
                messagebox.showinfo("Unlocked", f"Folder unlocked: {locked_folder_path}")
                locked_folder_path = None
                window.destroy()
                show_home()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to unlock folder: {str(e)}")
        else:
            messagebox.showwarning("No Folder", "No folder has been locked in this session.")

    if lock_mode:
        tk.Button(frame, text="Lock File", font=("Arial", 14), bg="#FFA500", fg="white", command=lock_file).pack(pady=10)
        tk.Button(frame, text="Lock Folder", font=("Arial", 14), bg="#FFA500", fg="white", command=lock_folder).pack(pady=10)
    else:
        tk.Button(frame, text="Unlock File", font=("Arial", 14), bg="#32CD32", fg="white", command=unlock_file).pack(pady=10)
        tk.Button(frame, text="Unlock Folder", font=("Arial", 14), bg="#32CD32", fg="white", command=unlock_folder).pack(pady=10)

    tk.Button(frame, text="Exit", font=("Arial", 14), bg="red", fg="white", command=window.destroy).pack(pady=20)


# Run the app
app = tk.Tk()
app.attributes('-fullscreen', True)
app.title("Graphical Password Authentication")
show_home()
app.mainloop()
