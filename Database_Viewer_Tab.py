'''
    Author: William Seagle
    Date: 04/18/2019
    Provides the Viewer Tab contents for the Main Window
'''

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from Postgres_Handler import DBConnection


class DatabaseViewerFrame(tk.Frame):
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
        tables = [
            'cal_providers',
            'cal_standards',
            'calibrations',
            'calprov_standards',
            'conditions',
            'instrument_identifier',
            'instruments',
            'locations',
            'pce_instr_def',
            'pce_instr_setup',
            'pce_switch',
            'transfers',
            'calhistory',
            'current_calequip',
            'pce_setup',
            'out_of_cal',
            'user_history'
        ]
        self.selected_table = tk.StringVar(self)
        self.selected_table.set(tables[0])
        self.table_select_dropdown = tk.OptionMenu(
            self.button_row, self.selected_table, *tables, command=self.refresh_data)
        self.table_select_dropdown.pack(side='left')

        # Refresh Button
        self.refresh_button = tk.Button(
            self.button_row, text="Refresh", command=self.refresh_data)
        self.refresh_button.pack(side='left', padx=1, pady=2, fill='y')

        # Search Frame
        # self.search_frame = tk.Frame(self)
        # self.search_label = tk.Label(self.search_frame, text='Search: ')
        # self.search_entry = ttk.Entry(self.search_frame)
        # self.search_button = tk.Button(self.search_frame, command=None)
        # self.search_label.pack(side='left')
        # self.search_entry.pack(side='left')
        # self.search_button.pack(side='left')
        # self.search_frame.pack(side='left')

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

    def refresh_data(self, event=None):
        # Remove Previous Objects
        self.tree.destroy()
        self.hsb.destroy()
        self.vsb.destroy()
        self.col_titles = []
        self.col_titles.clear()

        # Query Database
        column_titles, column_values = self.dbconn.get_table_values(
            self.selected_table.get())
        self.num_of_cols = len(column_titles)
        for col in column_titles:
            self.col_titles.append(col[0])

        # Generate New Table
        self.tree = ttk.Treeview(
            self, columns=column_titles, show="headings", height=15)
        for i in range(self.num_of_cols):
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
        if self.selected_table.get() == 'instrument_identifier':
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
            if tkfont.Font().measure(self.col_titles[col]) > max_len:
                max_len = tkfont.Font().measure(self.col_titles[col])
            tv.column(col, width=max_len)

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
