'''
    Author: William Seagle
    Date: 04/23/2019
    Provides the Admin Tab contents for the Main Window
'''

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import subprocess


class AdminFrame(tk.Frame):
    def __init__(self, parent, dbconn):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dbconn = dbconn

        # Admin Menu
        self.menu_frame = tk.Frame(
            self, relief='groove', bd=2, padx=50, pady=100)
        self.menu_frame.place(relx=.5, rely=.5, anchor='center')

        # Create Buttons
        self.backup_button = tk.Button(
            self.menu_frame, text="Database Backup", command=self.backup_database)
        self.restore_button = tk.Button(
            self.menu_frame, text="Database Restore", command=self.restore_database)

        # Place Buttons
        self.backup_button.pack(fill='x')
        self.restore_button.pack(fill='x')

        # Warning
        self.disclaimer_label = tk.Label(
            self, text="Warning: PostgreSQL\\bin must be in environmental variables")
        self.disclaimer_label.place(relx=.5, rely=.9, anchor='center')

    def backup_database(self):
        # Get Filepath From User
        filepath_bckp = tk.filedialog.asksaveasfilename(defaultextension=".sql", filetypes=(
            ("sql files", "*.sql"), ("all files", "*.*")))

        # Backup
        if filepath_bckp:
            process = subprocess.Popen(
                'pg_dump -h {} -U postgres --clean --file="{}" calibration_instruments'.format(self.dbconn.host, filepath_bckp))
            exit_code = process.wait()
            if exit_code == 0:
                tk.messagebox.showinfo('Finished', 'Backup Complete')
            else:
                tk.messagebox.showinfo('Finished', 'Backup Failed')

        
    def restore_database(self):
        # Get Filepath From User
        filepath_rest = tk.filedialog.askopenfilename(defaultextension=".sql", filetypes=(
            ("sql files", "*.sql"), ("all files", "*.*")))

        # Restore
        if filepath_rest:
            restore_thread = Thread(target=self.threader, args=(filepath_rest,))
            restore_thread.start()

    def threader(self, filepath):
        self.host = self.dbconn.host
        print(self.host)
        self.dbconn.disconnect()
        process = subprocess.Popen(
            'psql -h {} -U postgres -W -d calibration_instruments -f "{}"'.format(self.dbconn.host, filepath))
        exit_code = process.wait()
        stdout, stderr = process.communicate()
        if exit_code == 0:
            tk.messagebox.showinfo('Finished', 'Restore Complete')
        else:
            tk.messagebox.showinfo('Finished', 'Restore Failed')
        self.dbconn.connect(self.host)


if __name__ == "__main__":
    root = tk.Tk()
    AdminFrame(root).pack(side="top", fill="both", expand=True)
    root.geometry("750x400")
    root.title("Database Manager")
    root.mainloop()
