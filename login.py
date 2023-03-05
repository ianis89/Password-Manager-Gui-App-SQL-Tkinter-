import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('users.db')

conn.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY NOT NULL,
              password TEXT NOT NULL);''')

def register():
    username = username_entry.get()
    password = password_entry.get()

    # Criptarea parolei cu sha256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Adaugarea utilizatorului in baza de date
    try:
        conn.execute("INSERT INTO users (username, password) \
                      VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo(title="Inregistrare", message="Utilizatorul a fost inregistrat cu succes!")
    except:
        conn.rollback()
        messagebox.showerror(title="Eroare de inregistrare",
                             message="Inregistrarea a esuat. Numele de utilizator exista deja.")

def login():
    root.withdraw()
    username = username_entry.get()
    password = password_entry.get()

    # Criptarea parolei cu sha256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor = conn.execute("SELECT username, password FROM users \
                           WHERE username = ? AND password = ?", (username, hashed_password))

    if len(list(cursor)) == 1:
        messagebox.showinfo(title="Autentificare", message="Autentificare reusita!")

        root.destroy()
    else:
        messagebox.showerror(title="Eroare de autentificare", message="Informatiile de autentificare sunt invalide.")


root = tk.Tk()
root.title("Autentificare")


username_label = tk.Label(root, text="Nume de utilizator:")
username_label.grid(row=0, column=0)

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

password_label = tk.Label(root, text="Parola:")
password_label.grid(row=1, column=0)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

register_button = tk.Button(root, text="Inregistrare", command=register)
register_button.grid(row=2, column=0)

login_button = tk.Button(root, text="Logare", command=login)
login_button.grid(row=2, column=1)

