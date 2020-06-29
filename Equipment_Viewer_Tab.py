'''
    Author: William Seagle
    Date: 05/08/2019
    Provides the Equipment Viewer Tab contents for the Main Window
'''

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from Postgres_Handler import DBConnection


class EquipmentViewerFrame(tk.Frame):
    def __init__(self, parent, dbconn):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dbconn = dbconn

        # Frame Parameters
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(padx=8)

        # Buttons Frame
        self.button_row = tk.Frame(self)
        self.button_row.grid(row=2, columnspan=2, sticky='W')

        # Table Select Dropdown
        self.query_unique_values()

        self.selected_equipment = tk.StringVar(self)
        self.selected_equipment.set(self.unique_stands[0])
        self.table_select_dropdown = tk.OptionMenu(
            self.button_row, self.selected_equipment, *self.unique_stands, command=self.refresh_data)
        self.table_select_dropdown.pack(side='left')

        # Refresh Button
        self.refresh_button = tk.Button(
            self.button_row, text="Refresh", command=self.refresh_data)
        self.refresh_button.pack(side='left', padx=1, pady=2, fill='y')

        # Initial Tree Placeholder
        self.tree = ttk.Treeview(self, height=15)
        self.tree.heading('#0', text='Press Refresh')
        self.tree.column('#0', stretch=True)
        self.tree.grid(row=5, columnspan=2, sticky='nsew')
        self.treeview = self.tree

        # Initial Scrollbar Placeholder
        self.hsb = tk.Scrollbar(self, orient="horizontal",
                                command=self.treeview.xview)
        self.hsb.grid(sticky='ew', columnspan=2)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.treeview.yview)
        self.vsb.grid(row=5, column=3, sticky='ns')

    def treeview_autosize_columns(self, tv):
        column_list = []
        column_list.clear()
        for col in range(self.num_of_cols):
            max_len = 0
            for k in tv.get_children(''):
                value = tv.set(k, col)
                width = (tkfont.Font().measure(value))
                if width > max_len:
                    max_len = width
            # Checks Font Size In Pixels
            if tkfont.Font().measure(self.col_titles[col]) > max_len:
                max_len = tkfont.Font().measure(self.col_titles[col])
            tv.column(col, width=max_len)

    def query_unique_values(self):
        # Query Database
        column_titles, self.table_values = self.dbconn.get_table_values(
            'current_calequip')

        # Create Unique Lists
        self.unique_stands = self.get_unique_list(self.table_values, 0)

    def get_unique_list(self, column_values, column_num):
        # Generates Unique List from List
        unique_list = []
        for row in column_values:
            if row[column_num] not in unique_list:
                unique_list.append(row[column_num])
        unique_list.sort()
        return unique_list

    def refresh_data(self, event=None):
        # Remove Previous Objects
        self.tree.destroy()
        self.hsb.destroy()
        self.vsb.destroy()
        self.col_titles = []
        self.col_titles.clear()

        # Query Database
        column_titles, column_values = self.dbconn.get_stand_equip(
            self.selected_equipment.get())
        self.num_of_cols = len(column_titles)
        for col in column_titles:
            self.col_titles.append(col[0])

        # Generate New Table
        self.tree = ttk.Treeview(
            self, columns=column_titles, show="headings", height=15)
        for i in range(len(column_titles)):
            self.tree.heading(column_titles[i][0], text=column_titles[i][0],
                              command=lambda _col=column_titles[i][0]: self.treeview_sort_column(self.tree, _col, False))
            self.tree.column(column_titles[i][0], stretch=True)
        col_one_name = self.tree.column(0, option='id')
        if col_one_name[0] == 'key':
            self.tree.column(0, width=50)
        self.tree.grid(row=5, columnspan=2, sticky='nsew')
        self.treeview = self.tree

        # Insert the Table Values
        for i in range(len(column_values)):
            try:
                column_values[i][0] = int(column_values[i][0])
            except:
                pass
            self.treeview.insert('', 'end', text=i, values=column_values[i])

        # Initial Sort
        if self.selected_equipment.get() == 'instrument_identifier':
            self.treeview_sort_column(self.tree, 3, False)
        else:
            self.treeview_sort_column(self.tree, 0, False)

        # Generate New Scrollbars
        self.hsb = tk.Scrollbar(self, orient="horizontal",
                                command=self.treeview.xview)
        self.hsb.grid(sticky='ew', columnspan=2)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.treeview.yview)
        self.vsb.grid(row=5, column=3, sticky='ns')
        self.treeview.configure(
            yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.treeview_autosize_columns(self.treeview)

    def treeview_sort_column(self, tv, col, reverse):
        # Initialize and Clear list
        column_list = []
        column_list.clear()

        # If it is an integer column, convert
        for k in tv.get_children(''):
            try:
                column_list.append([int(tv.set(k, col)), k])
            except:
                column_list.append([tv.set(k, col), k])
        try:
            column_list.sort(reverse=reverse)
        except:
            column_list.clear()
            for k in tv.get_children(''):
                column_list.append([tv.set(k, col), k])
            column_list.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(column_list):
            tv.move(k, '', index)
        col_one_name = self.tree.column(0, option='id')
        if col_one_name[0] == 'key':
            self.tree.column(0, width=50)

        # Reverse sort next time
        tv.heading(col, command=lambda:
                   self.treeview_sort_column(tv, col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    DataTable(root).pack(side="top", fill="both", expand=True)
    root.geometry("750x400")
    root.title("Database Manager")
    root.mainloop()
