'''
    Author: William Seagle
    Date: 04/04/2019
    Provides Main Window for the Database Manager
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Postgres_Handler import DBConnection
from Database_Viewer_Tab import DatabaseViewerFrame
from Equipment_Viewer_Tab import EquipmentViewerFrame
from Actions_Tab import ActionFrame
from Admin_Tab import AdminFrame

ip_to_name = {
    "172.26.128.53": "Iris",
    "172.22.30.1": "Aello",
    "192.168.138.4": "Ocypete",
    "localhost": "Local Host"
}


class MainPage(tk.Frame):
    def __init__(self, parent, admin_rights, user, dbconn):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.isAdmin = admin_rights
        self.dbconn = dbconn
        self.user = user
        self.VERSION = '2.1.0'

        # Create Navbar
        self.navbar = ttk.Notebook(self)
        self.navbar.pack(fill='x')

        # Lower Statusbar
        self.statusbar_frame = tk.Frame(self, relief='flat', border=1)
        self.statusbar_frame.pack(side='bottom', fill='x')
        self.logout_button = tk.Button(
            self.statusbar_frame, text='Logout', command=self.logout)
        self.logout_button.pack(side='right', padx=5)
        self.status_label = tk.Label(
            self.statusbar_frame, text='User: {}    Database: {}'.format(user, ip_to_name[dbconn.host]))
        self.status_label.pack(side='right', fill='x')
        self.version_label = tk.Label(
            self.statusbar_frame, text='Version: {}'.format(self.VERSION))
        self.version_label.pack(side='left')

        # Create Tabs
        self.action_tab = ActionFrame(self.navbar, self.dbconn, self.user)
        self.database_viewer_tab = DatabaseViewerFrame(
            self.navbar, self.dbconn)
        self.equipment_viewer_tab = EquipmentViewerFrame(
            self.navbar, self.dbconn)
        self.admin_tab = AdminFrame(self.navbar, self.dbconn)

        self.navbar.add(self.action_tab, text="Actions")
        self.navbar.add(self.database_viewer_tab, text="Database Viewer")
        self.navbar.add(self.equipment_viewer_tab, text="Equipment Viewer")
        if self.isAdmin:
            self.navbar.add(self.admin_tab, text="Admin")
        # self.database_select_frame.pack(side="top", fill="x")
        # self.data_table.pack(fill='both', padx='5', pady='5')

    def logout(self):
        self.destroy()
        self.parent.create_login_page()


if __name__ == "__main__":
    root = tk.Tk()
    MainPage(root, True).pack(side="left", fill="both", expand=True)
    root.geometry("750x400")
    root.title("Database Manager")
    root.mainloop()
