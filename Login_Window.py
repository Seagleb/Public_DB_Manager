'''
    Author: William Seagle
    Date: 04/04/2019
    Provides Login Window for the Database Manager
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Active_Directory_Authorization import ADConnection
from Postgres_Handler import DBConnection


class LoginScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.VERSION = '2.1.0'

        # Create Frames
        self.entry_frame = tk.Frame(self)
        self.button_frame = tk.Frame(self)

        # Create Labels/Entries
        self.user_label = tk.Label(self.entry_frame, text="Username ")
        self.pass_label = tk.Label(self.entry_frame, text="Password ")
        self.user_entry = ttk.Entry(self.entry_frame)
        self.pass_entry = ttk.Entry(self.entry_frame, show="*")
        self.data_drop = DatabaseSelect(self)
        self.version_label = tk.Label(self, text='Version: {}'.format(self.VERSION))

        # Place Frames
        self.entry_frame.pack()
        self.data_drop.pack()
        self.button_frame.pack()
        self.version_label.pack(side='left')

        # Place Labels/Entries
        self.user_label.grid(row=1, column=1, pady=5)
        self.user_entry.grid(row=1, column=2, pady=5)
        self.pass_label.grid(row=2, column=1, pady=5)
        self.pass_entry.grid(row=2, column=2, pady=5)

        # Create Buttons
        self.login_button = tk.Button(
            self.button_frame, text="Login", command=lambda: self.attempt_login(), width=8)
        self.cancel_button = tk.Button(
            self.button_frame, text="Cancel", command=self.parent.on_closing, width=8)

        # Place Buttons
        self.login_button.pack(side="left", padx=5, pady=5)
        self.cancel_button.pack(side="left", padx=5, pady=5)

        # Window Parameters
        self.user_entry.focus_set()
        self.update_disable('None')

    def update_disable(self, evnt):
        if self.data_drop.selected_db.get() == 'Remote':
            self.user_entry.config(state='normal')
            self.pass_entry.config(state='normal')
        else:
            self.user_entry.config(state='disable')
            self.pass_entry.config(state='disable')

    def attempt_login(self, event=None):
        # Creds from Button
        user = self.user_entry.get()
        pswd = self.pass_entry.get()
        domain = self.data_drop.selected_db.get()

        if domain == 'Remote':
            # Establish Connection
            ac = ADConnection(user, pswd)
            # Switch Windows upon Success
            if (ac.connection.last_error == None) and (ac.error == None):
                self.parent.host = ac.db_server
                self.parent.dbconnection = DBConnection(self.parent.host)
                if self.parent.dbconnection.error:
                    tk.messagebox.showerror('Error', 'Unable to connect to Remote \n\n{}'.format(
                        self.parent.dbconnection.error))
                else:
                    # Check Privileges
                    priv = self.parent.dbconnection.get_privilege(user)
                    if priv == 3:
                        isAdmin = True
                        print("Is an Admin")
                    else:
                        isAdmin = False

                    self.destroy()
                    self.parent.create_main_page(
                        isAdmin, user, self.parent.dbconnection)
            elif ac.connection.last_error is not None:
                tk.messagebox.showerror("Error", ac.connection.last_error)
            elif ac.error is not None:
                tk.messagebox.showerror(
                    "Error", ac.connection.result['description'])

            # Disconnect
            ac.connection.unbind()
        else:
            isAdmin = True
            user = 'Local'
            self.parent.dbconnection = DBConnection("localhost")
            if self.parent.dbconnection.error:
                tk.messagebox.showerror('Error', 'Unable to connect to Localhost \nEnsure you have a server hosted \n\n{}'.format(
                    self.parent.dbconnection.error))
            else:
                self.destroy()
                self.parent.create_main_page(
                    isAdmin, user, self.parent.dbconnection)


class DatabaseSelect(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='black')
        self.parent = parent

        #databases = ['Local Host', 'Iris - Champaign', 'Aello - Marlborough', 'Ocypete - UK']
        databases = ['Remote', 'Local Host']
        self.selected_db = tk.StringVar(self)
        self.selected_db.set(databases[0])
        self.database_select_dropdown = tk.OptionMenu(
            self, self.selected_db, *databases, command=self.parent.update_disable)
        self.database_select_dropdown.pack()

    def get(self):
        return self.selected_db.get()


if __name__ == "__main__":
    root = tk.Tk()
    LoginScreen(root).pack(side="left", fill="both", expand=True)
    root.geometry("300x100")
    root.title("Database Manager Login")
    root.mainloop()
