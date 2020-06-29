'''
    Author: William Seagle
    Date: 04/18/2019
    Provides the Actions Tab contents for the Main Window
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Postgres_Handler import DBConnection
import tkcalendar as tkc


class ActionFrame(tk.Frame):
    def __init__(self, parent, dbconn, user):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dbconn = dbconn
        self.user = user

        # Action Menu
        self.menu_frame = tk.Frame(
            self, relief='groove', bd=2, padx=50, pady=100)
        self.menu_frame.place(relx=.5, rely=.5, anchor='center')

        # Create Buttons
        self.add_button = tk.Button(
            self.menu_frame, text="Add Instrument", command=self.add_instrument, width=25, height=2)
        self.transfer_button = tk.Button(
            self.menu_frame, text="Transfer Instrument", command=self.transfer_instrument, width=25, height=2)
        self.calibration_button = tk.Button(
            self.menu_frame, text="Update Calibration", command=self.update_calibration, width=25, height=2)

        # Place Buttons
        self.add_button.pack(fill='x')
        self.transfer_button.pack(fill='x')
        self.calibration_button.pack(fill='x')

    def add_instrument(self):
        self.add_instrument_frame = AddInstrument(self, self.dbconn)
        self.add_instrument_frame.place(
            relx=.5, rely=.5, anchor='center', relwidth=1, relheight=1)

    def transfer_instrument(self):
        self.transfer_instrument_frame = TransferInstrument(self, self.dbconn)
        self.transfer_instrument_frame.place(
            relx=.5, rely=.5, anchor='center', relwidth=1, relheight=1)

    def update_calibration(self):
        self.update_calibration_frame = UpdateCalibration(self, self.dbconn)
        self.update_calibration_frame.place(
            relx=.5, rely=.5, anchor='center', relwidth=1, relheight=1)


class AddInstrument(tk.Frame):
    def __init__(self, parent, dbconn):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dbconn = dbconn

        # Frames
        self.serial_frame = tk.Frame(self)
        self.menu_frame = tk.Frame(self)
        self.date_frame = tk.Frame(self)

        # Menu Buttons
        self.verify_button = tk.Button(
            self.menu_frame, text="Verify", command=self.verify, width=10)
        self.back_button = tk.Button(
            self.menu_frame, text="Back", command=self.back, width=10)

        self.verify_button.pack(side="left")
        self.back_button.pack(side="left")

        # Checkbox
        self.is_new_manuf = tk.IntVar()
        self.new_checkbox = tk.Checkbutton(
            self, text="New From Manufacturer", variable=self.is_new_manuf, command=self.check_press)

        # Cal Date Entry
        self.date_label_subframe = tk.Frame(self.date_frame)
        self.date_entry_subframe = tk.Frame(self.date_frame)
        self.date_label_subframe.pack(side='left')
        self.date_entry_subframe.pack(side='left', fill='y')

        self.cal_label = tk.Label(self.date_label_subframe, text='Calibration Date:  ', anchor='w')
        self.cal_due_label = tk.Label(self.date_label_subframe, text='Calibration Due:  ', anchor='w')
        self.cal_label.pack(fill='x', pady=5)
        self.cal_due_label.pack(fill='x', pady=5)

        self.entry_border_date = tk.Frame(self.date_entry_subframe, relief='sunken', bd=1)
        self.entry_border_due_date = tk.Frame(self.date_entry_subframe, relief='sunken', bd=1)
        self.entry_border_date.pack(pady=5)
        self.entry_border_due_date.pack(pady=6)
        self.cal_date = tkc.DateEntry(self.entry_border_date, width=12)
        self.cal_due_date = tkc.DateEntry(self.entry_border_due_date, width=12)
        self.cal_date.pack()
        self.cal_due_date.pack()

        # List Boxes
        self.instrument_type = ColumnListBox(self, 'instr_type', 'Type')
        self.instrument_manufacturer = ColumnListBox(
            self, 'instr_manu', 'Manufacturer')
        self.instrument_model = ColumnListBox(self, 'instr_modl', 'Model')
        self.cal_provider = ColumnListBox(
            self, 'calib_prvd', 'Calibration Provider')
        self.cal_provider.column_listbox.config(width=40)

        # Binds
        self.instrument_type.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_manufacturer.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_model.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)

        # Serial
        self.serial_label = tk.Label(
            self.serial_frame, text="Serial Number:  ")
        self.serial_entry = ttk.Entry(self.serial_frame)
        self.serial_label.pack(side='left')
        self.serial_entry.pack(side='left', fill='x', expand=True)

        # Disclaimer
        self.disclaimer_label = tk.Label(
            self, text="Please contact your Database Administrator if you are unable to find your instrument")

        # Placements
        self.instrument_type.grid(row=1, column=0, padx=5)
        self.instrument_manufacturer.grid(row=1, column=1, padx=5)
        self.instrument_model.grid(row=1, column=2, padx=5)
        self.cal_provider.grid(row=1, column=3, padx=5)
        self.serial_frame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky='WE')
        self.date_frame.grid(row=3, rowspan=2, column=0, pady=5,
                             padx=5, columnspan=2, sticky='W')
        self.new_checkbox.grid(row=2, column=3, sticky='W')
        self.menu_frame.grid(row=5, column=0, pady=10, columnspan=4)
        self.disclaimer_label.grid(row=6, column=0, pady=10, columnspan=4)

        # Set Default Values
        self.query_unique_values()
        for row_value in self.unique_types:
            self.instrument_type.column_listbox.insert('end', row_value)
        for row_value in self.unique_providers:
            if row_value != 'New from Manufacturer':
                self.cal_provider.column_listbox.insert('end', row_value)

    def check_press(self):
        # Disables Calibration Provider Listbox
        if self.is_new_manuf.get() == 1:
            self.cal_provider.column_listbox.config(state='disabled')
        else:
            self.cal_provider.column_listbox.config(state='normal')

    def query_unique_values(self):
        # Query Database
        column_titles, self.table_values = self.dbconn.get_table_values(
            'instruments')
        calp_titles, self.cal_providers = self.dbconn.get_table_values(
            'cal_providers')

        # Create Unique Lists
        self.unique_types = self.get_unique_list(self.table_values, 4)
        self.unique_manufacturers = self.get_unique_list(self.table_values, 2)
        self.unique_models = self.get_unique_list(self.table_values, 3)
        self.unique_providers = self.get_unique_list(self.cal_providers, 1)

    def get_unique_list(self, column_values, column_num):
        # Generates Unique List from List
        unique_list = []
        for row in column_values:
            if row[column_num] not in unique_list:
                unique_list.append(row[column_num])
        unique_list.sort()
        return unique_list

    def filter_listbox(self, event):
        # Get Name of Listbox
        w = event.widget
        changed_listbox = str(w)[-4:]

        # Recieve Inputs
        self.selected_type = self.instrument_type.column_listbox.curselection()
        self.selected_manufacturer = self.instrument_manufacturer.column_listbox.curselection()

        if changed_listbox == 'type':
            # Clear Manuf/Model
            self.instrument_manufacturer.column_listbox.delete(0, 'end')
            self.instrument_model.column_listbox.delete(0, 'end')
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])

            # Create New Manuf List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type == value[4]:
                    if value[2] not in self.filtered_list:
                        self.filtered_list.append(value[2])

            # Update Manufacturer
            for row_value in self.filtered_list:
                self.instrument_manufacturer.column_listbox.insert(
                    'end', row_value)

        elif changed_listbox == 'manu':
            self.instrument_model.column_listbox.delete(0, 'end')

            # Get Inputs
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])
            self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
                self.selected_manufacturer[0])

            # Create New Filtered List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type == value[4]:
                    if self.selected_manufacturer == value[2]:
                        if value[3] not in self.filtered_list:
                            self.filtered_list.append(value[3])

            # Update Model
            for row_value in self.filtered_list:
                self.instrument_model.column_listbox.insert(
                    'end', row_value)

    def back(self):
        self.destroy()

    def verify(self):
        # Get Entry values
        self.selected_type = self.instrument_type.column_listbox.get('active')
        self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
            'active')
        self.selected_model = self.instrument_model.column_listbox.get(
            'active')
        self.serial_input = self.serial_entry.get()
        self.selected_cal_date = self.cal_date.get_date()
        self.selected_cal_due_date = self.cal_due_date.get_date()
        self.selected_provider = self.cal_provider.column_listbox.curselection()

        # Check Status of Cal Provider
        if self.is_new_manuf.get() == 1:
            self.selected_provider = 'New from Manufacturer'
        else:
            try:
                self.selected_provider = self.cal_provider.column_listbox.get(
                    self.selected_provider[0])
            except:
                self.selected_provider = None

        # Verification Steps
        if self.serial_input != '' and self.selected_provider and "'" not in self.serial_input and '"' not in self.serial_input and len(self.serial_input) < 255:
            # Check if Serial Exists
            possible_serials = self.dbconn.get_serials(
                self.selected_model, self.selected_type, self.selected_manufacturer)
            serial_list_string = ''
            for serial in possible_serials:
                serial_list_string = serial_list_string + serial + '\n'
            serial_exists = self.dbconn.check_exists(
                self.selected_model, self.selected_type, self.selected_manufacturer, self.serial_input)

            if serial_exists:
                tk.messagebox.showerror(
                    'Invalid', 'The serial you have entered already exists. Update Calibration or Contact your Database Manager')
            else:
                if serial_list_string:
                    self.serial_check_pop = tk.messagebox.askyesno(
                        'Verify SN', 'Is your serial number in this list: \n{}'.format(serial_list_string))
                    if self.serial_check_pop:
                        tk.messagebox.showerror(
                            'Invalid', 'Update Calibration or Contact your Database Manager')
                    else:
                        self.verify_pop = tk.messagebox.askyesno(
                            'Verify Information', 'Pending Update: \n    Type: {} \n    Manufacturer: {} \n    Model: {} \n    SN: {} \n    Calibration Provider: {} \n    Calibration Date: {}  \n    Calibration Due Date: {} \n \nUpdate Database?'.format(self.selected_type, self.selected_manufacturer, self.selected_model, self.serial_input, self.selected_provider, str(self.selected_cal_date), str(self.selected_cal_due_date)))
                        if self.verify_pop:
                            self.dbconn.add_instrument(
                                self.selected_manufacturer, self.selected_model, self.selected_type, self.serial_input, self.selected_cal_date, self.selected_cal_due_date, self.selected_provider, self.parent.user)
                            tk.messagebox.showinfo(
                                'Added', 'Instrument Added to the Database')
                        else:
                            tk.messagebox.showinfo(
                                'Nothing Added', 'Nothing was added to the Database')
                else:
                    self.verify_pop = tk.messagebox.askyesno(
                        'Verify Information', 'Pending Update: \n    Type: {} \n    Manufacturer: {} \n    Model: {} \n    SN: {} \n    Calibration Provider: {} \n    Calibration Date: {}  \n    Calibration Due Date: {} \n \nUpdate Database?'.format(self.selected_type, self.selected_manufacturer, self.selected_model, self.serial_input, self.selected_provider, str(self.selected_cal_date), str(self.selected_cal_due_date)))
                    if self.verify_pop:
                        self.dbconn.add_instrument(
                            self.selected_manufacturer, self.selected_model, self.selected_type, self.serial_input, self.selected_cal_date, self.selected_provider, self.parent.user)
                        tk.messagebox.showinfo(
                            'Added', 'Instrument Added to the Database')
                    else:
                        tk.messagebox.showinfo(
                            'Nothing Added', 'Nothing was added to the Database')

        else:
            if self.serial_input == '':
                tk.messagebox.showerror(
                    'Invalid', 'No Serial Entered')
            elif "'" in self.serial_input:
                tk.messagebox.showerror(
                    'Invalid', "' is not a valid character")
            elif '"' in self.serial_input:
                tk.messagebox.showerror(
                    'Invalid', '" is not a valid character')
            elif len(self.serial_input) >= 255:
                tk.messagebox.showerror(
                    'Invalid', 'Serial must be shorter than 255 characters')
            else:
                tk.messagebox.showerror(
                    'Invalid', 'No Calibration Provider Selected')


class TransferInstrument(tk.Frame):
    def __init__(self, parent, dbconn):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dbconn = dbconn

        # Frames
        self.serial_frame = tk.Frame(self)
        self.menu_frame = tk.Frame(self)
        self.halflist_frame = tk.Frame(self)
        self.halflist_frame2 = tk.Frame(self)
        self.lower_entry_frame = tk.Frame(self)
        self.conditions_frame = tk.Frame(self.lower_entry_frame)
        self.notes_frame = tk.Frame(self.lower_entry_frame)

        # Initial Query
        self.query_unique_values()

        # Menu Buttons
        self.verify_button = tk.Button(
            self.menu_frame, text="Verify", command=self.verify, width=10)
        self.back_button = tk.Button(
            self.menu_frame, text="Back", command=self.back, width=10)

        self.verify_button.pack(side="left")
        self.back_button.pack(side="left")

        # Condition Entry
        self.condition_label = tk.Label(
            self.conditions_frame, text='Condition: ')
        self.conditions_dropdown = ttk.Combobox(
            self.conditions_frame, values=self.unique_conditions)
        self.condition_label.pack(side='left')
        self.conditions_dropdown.pack(side='left')
        self.conditions_dropdown.current(2)
        self.conditions_frame.pack(side='left', padx=5)

        # Notes Entry
        self.note_label = tk.Label(self.notes_frame, text='Notes: ')
        self.note_entry = ttk.Entry(self.notes_frame, width=50)
        self.note_label.pack(side='left')
        self.note_entry.pack(side='left')
        self.notes_frame.pack(side='left', padx=5)

        # List Boxes
        self.instrument_type = ColumnListBox(self, 'instr_type', 'Type')
        self.instrument_manufacturer = ColumnListBox(
            self, 'instr_manu', 'Manufacturer')
        self.instrument_model = ColumnListBox(
            self.halflist_frame, 'instr_modl', 'Model')
        self.instrument_serial = ColumnListBox(
            self.halflist_frame, 'instr_serl', 'Serial')
        self.instrument_model.column_listbox.config(height=4)
        self.instrument_serial.column_listbox.config(height=4)
        self.instrument_model.pack(side='top')
        self.instrument_serial.pack(side='bottom')
        self.from_location = ColumnListBox(
            self.halflist_frame2, 'instr_from', 'From Location')
        self.to_location = ColumnListBox(
            self.halflist_frame2, 'instr_from', 'To Location')
        self.from_location.column_listbox.config(height=4)
        self.to_location.column_listbox.config(height=4)
        self.from_location.pack(side='top')
        self.to_location.pack(side='bottom')
        self.from_location.column_listbox.config(width=40)
        self.to_location.column_listbox.config(width=40)

        # Binds
        self.instrument_type.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_manufacturer.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_model.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_serial.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)

        # Disclaimer
        self.disclaimer_label = tk.Label(
            self, text="Please contact your Database Administrator if you are unable to find your instrument")

        # Placements
        self.instrument_type.grid(row=1, column=0, padx=5)
        self.instrument_manufacturer.grid(row=1, column=1, padx=5)
        self.halflist_frame.grid(row=1, column=2, padx=5, sticky='NS')
        self.halflist_frame2.grid(
            row=1, column=3, padx=5, sticky='NS', columnspan=2)
        self.menu_frame.grid(row=5, column=0, pady=10, columnspan=5)
        self.disclaimer_label.grid(row=6, column=0, pady=10, columnspan=5)
        self.lower_entry_frame.grid(row=3, column=0, pady=10,
                                    padx=5, columnspan=4, sticky='W')

        # Set Default Values
        for row_value in self.unique_types:
            self.instrument_type.column_listbox.insert('end', row_value)
        for row_value in self.unique_transfers:
            self.to_location.column_listbox.insert('end', row_value)

        # Existing Instrument Whitelist
        self.existing_whitelist = [
            'CalStand 01', 'CalStand 02', 'CalStand 03'
            ,'CalStand 02', 'CalStand 03', 'CalStand 04'
            ,'CalStand 05', 'CalStand 06', 'CalStand 07'
            ,'CalStand 08', 'CalStand 09'
            ]

    def filter_listbox(self, event):
        # Get Name of Listbox
        w = event.widget
        changed_listbox = str(w)[-4:]

        # Recieve Inputs
        self.selected_type = self.instrument_type.column_listbox.curselection()
        self.selected_manufacturer = self.instrument_manufacturer.column_listbox.curselection()
        self.selected_model = self.instrument_model.column_listbox.curselection()

        if changed_listbox == 'type':
            # Clear Manuf/Model/Serial
            self.instrument_manufacturer.column_listbox.delete(0, 'end')
            self.instrument_model.column_listbox.delete(0, 'end')
            self.instrument_serial.column_listbox.delete(0, 'end')
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])

            # Create New Manuf List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type == value[4]:
                    if value[2] not in self.filtered_list:
                        self.filtered_list.append(value[2])

            # Update Manufacturer
            for row_value in self.filtered_list:
                self.instrument_manufacturer.column_listbox.insert(
                    'end', row_value)

        elif changed_listbox == 'manu':
            # Clear Model/Serial Dropbox
            self.instrument_model.column_listbox.delete(0, 'end')
            self.instrument_serial.column_listbox.delete(0, 'end')

            # Get Inputs
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])
            self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
                self.selected_manufacturer[0])

            # Create New Filtered List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type in value[4]:
                    if self.selected_manufacturer in value[2]:
                        if value[3] not in self.filtered_list:
                            self.filtered_list.append(value[3])

            # Update Model
            for row_value in self.filtered_list:
                self.instrument_model.column_listbox.insert(
                    'end', row_value)

        elif changed_listbox == 'modl':
            # Clear Serial Dropbox
            self.instrument_serial.column_listbox.delete(0, 'end')

            # Get Inputs
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])
            self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
                self.selected_manufacturer[0])
            self.selected_model = self.instrument_model.column_listbox.get(
                self.selected_model[0])

            # Create New Filtered List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type == value[4]:
                    if self.selected_manufacturer == value[2]:
                        if self.selected_model == value[3]:
                            self.filtered_list.append(value[5])

            # Update Serial
            for row_value in self.filtered_list:
                self.instrument_serial.column_listbox.insert(
                    'end', row_value)

        elif changed_listbox == 'serl':
            # Clear From Location Dropbox
            self.from_location.column_listbox.delete(0, 'end')

            # Get Inputs
            self.selected_serial = self.instrument_serial.column_listbox.curselection()
            self.selected_serial = self.instrument_serial.column_listbox.get(
                self.selected_serial[0])
            last_location = self.dbconn.get_last_location(self.selected_serial)

            # Update From
            if last_location:
                self.from_location.column_listbox.insert('end', last_location)
            else:
                warning = tk.messagebox.showerror(
                    'Warning', 'This instrument does not have any previous transfers. \n\nThis is an error in the Database.\nPlease contact your Database administrator')

    def query_unique_values(self):
        # Query Database
        column_titles, self.table_values = self.dbconn.get_table_values(
            'instruments')
        trnsfer_titles, self.transfer_locations = self.dbconn.get_table_values(
            'locations')
        condit_titles, self.condition_values = self.dbconn.get_table_values(
            'conditions')

        # Create Unique Lists
        self.unique_conditions = self.get_unique_list(self.condition_values, 1)
        self.unique_types = self.get_unique_list(self.table_values, 4)
        self.unique_manufacturers = self.get_unique_list(self.table_values, 2)
        self.unique_models = self.get_unique_list(self.table_values, 3)
        self.unique_transfers = self.get_unique_list(
            self.transfer_locations, 2)

    def get_unique_list(self, column_values, column_num):
        # Generates Unique List from List
        unique_list = []
        for row in column_values:
            if row[column_num] not in unique_list:
                unique_list.append(row[column_num])
        unique_list.sort()
        return unique_list

    def verify(self):
        # Get Entry values
        self.selected_type = self.instrument_type.column_listbox.get('active')
        self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
            'active')
        self.selected_model = self.instrument_model.column_listbox.get(
            'active')
        self.selected_serial = self.instrument_serial.column_listbox.get(
            'active')
        self.selected_from_location = self.from_location.column_listbox.get(
            'active')
        self.selected_to_location = self.to_location.column_listbox.get(
            'active')
        self.selected_condition = self.conditions_dropdown.get()
        self.entered_notes = self.note_entry.get()

        if "'" in self.entered_notes or '"' in self.entered_notes or len(self.entered_notes) > 255:
            if "'" in self.entered_notes or '"' in self.entered_notes:
                tk.messagebox.showerror(
                    'Invalid', """ ' and " are invalid characters.""")
            elif len(self.entered_notes) > 255:
                tk.messagebox.showerror(
                    'Invalid', "Notes must be shorter than 255 characters")
        else:
            allowed = self.dbconn.check_daily_transfer_limit(
                self.selected_type, self.selected_to_location)
            if allowed:
                self.verify_pop = tk.messagebox.askyesno(
                    'Verify Information', 'Pending Update: \n    Type: {} \n    Manufacturer: {} \n    Model: {} \n    SN: {} \n    From: {} \n    To: {} \n \nUpdate Database?'.format(self.selected_type, self.selected_manufacturer, self.selected_model, self.selected_serial, self.selected_from_location, self.selected_to_location))
                if self.verify_pop:
                    if self.selected_to_location in self.existing_whitelist:
                        existing_instruments = self.dbconn.check_transfer(
                            self.selected_to_location, self.selected_type)
                        if existing_instruments:
                            for instrument in existing_instruments:
                                move_response = tk.messagebox.askyesno(
                                    'Existing Instruments', '{} already exists in {}. \nMove it to spare?'.format(instrument[3], self.selected_to_location))
                                if move_response:
                                    self.dbconn.transfer_instrument(
                                        instrument[3], self.selected_to_location, 'Spare equipment - in calibration', 'In Tolerance',  self.parent.user)     
                
                    self.dbconn.transfer_instrument(self.selected_serial, self.selected_from_location,
                                                    self.selected_to_location, self.selected_condition, self.parent.user, self.entered_notes)
                    tk.messagebox.showinfo(
                        'Added', 'Calibration updated in the Database')
                else:
                    tk.messagebox.showinfo(
                        'Nothing Added', 'Nothing was added to the Database')
            else:
                tk.messagebox.showerror(
                    'Invalid', 'An Instrument of that type has been transferred to that location already today.\nIf this is required, please contact the Quality Manager')

    def back(self):
        self.destroy()


class UpdateCalibration(tk.Frame):
    def __init__(self, parent, dbconn):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dbconn = dbconn

       # Frames
        self.serial_frame = tk.Frame(self)
        self.menu_frame = tk.Frame(self)
        self.date_frame = tk.Frame(self)
        self.halflist_frame = tk.Frame(self)
        self.condition_frame = tk.Frame(self)

        # Initial Query
        self.query_unique_values()

        # Menu Buttons
        self.verify_button = tk.Button(
            self.menu_frame, text="Verify", command=self.verify, width=10)
        self.back_button = tk.Button(
            self.menu_frame, text="Back", command=self.back, width=10)

        self.verify_button.pack(side="left")
        self.back_button.pack(side="left")

        # Cal Date Entry
        self.date_label_subframe = tk.Frame(self.date_frame)
        self.date_entry_subframe = tk.Frame(self.date_frame)
        self.date_label_subframe.pack(side='left')
        self.date_entry_subframe.pack(side='left', fill='y')

        self.cal_label = tk.Label(
            self.date_label_subframe, text='Calibration Date:  ', anchor='w')
        self.cal_due_label = tk.Label(
            self.date_label_subframe, text='Calibration Due:  ', anchor='w')
        self.cal_label.pack(fill='x', pady=5)
        self.cal_due_label.pack(fill='x', pady=5)

        self.entry_border_date = tk.Frame(
            self.date_entry_subframe, relief='sunken', bd=1)
        self.entry_border_due_date = tk.Frame(
            self.date_entry_subframe, relief='sunken', bd=1)
        self.entry_border_date.pack(pady=5)
        self.entry_border_due_date.pack(pady=6)
        self.cal_date = tkc.DateEntry(self.entry_border_date, width=12)
        self.cal_due_date = tkc.DateEntry(self.entry_border_due_date, width=12)
        self.cal_date.pack()
        self.cal_due_date.pack()

        # Condition Entry
        self.condition_label = tk.Label(
            self.condition_frame, text='Condition: ')
        self.conditions_dropdown = ttk.Combobox(
            self.condition_frame, values=self.unique_conditions)
        self.condition_label.pack(side='left')
        self.conditions_dropdown.pack(side='left')
        self.conditions_dropdown.current(2)

        # List Boxes
        self.instrument_type = ColumnListBox(self, 'instr_type', 'Type')
        self.instrument_manufacturer = ColumnListBox(
            self, 'instr_manu', 'Manufacturer')
        self.instrument_model = ColumnListBox(
            self.halflist_frame, 'instr_modl', 'Model')
        self.instrument_serial = ColumnListBox(
            self.halflist_frame, 'instr_serl', 'Serial')
        self.instrument_model.column_listbox.config(height=4)
        self.instrument_serial.column_listbox.config(height=4)
        self.instrument_model.pack(side='top')
        self.instrument_serial.pack(side='bottom')
        self.cal_provider = ColumnListBox(
            self, 'calib_prvd', 'Calibration Provider')
        self.cal_provider.column_listbox.config(width=40)

        # Binds
        self.instrument_type.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_manufacturer.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_model.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)
        self.instrument_serial.column_listbox.bind(
            '<<ListboxSelect>>', self.filter_listbox)

        # Disclaimer
        self.disclaimer_label = tk.Label(
            self, text="Please contact your Database Administrator if you are unable to find your instrument")

        # Placements
        self.instrument_type.grid(row=1, column=0, padx=5)
        self.instrument_manufacturer.grid(row=1, column=1, padx=5)
        self.halflist_frame.grid(row=1, column=2, padx=5, sticky='NS')
        self.cal_provider.grid(row=1, column=3, padx=5)
        self.date_frame.grid(row=3, rowspan=2, column=0, pady=5,
                             padx=5, columnspan=2, sticky='W')
        self.condition_frame.grid(row=5, column=0, pady=3,
                                  padx=5, columnspan=2, sticky='W')
        self.menu_frame.grid(row=6, column=0, pady=10, columnspan=4)
        self.disclaimer_label.grid(row=7, column=0, pady=10, columnspan=4)

        # Set Default Values
        for row_value in self.unique_types:
            self.instrument_type.column_listbox.insert('end', row_value)
        for row_value in self.unique_providers:
            if row_value != 'New from Manufacturer':
                self.cal_provider.column_listbox.insert('end', row_value)

    def filter_listbox(self, event):
        # Get Name of Listbox
        w = event.widget
        changed_listbox = str(w)[-4:]

        # Recieve Inputs
        self.selected_type = self.instrument_type.column_listbox.curselection()
        self.selected_manufacturer = self.instrument_manufacturer.column_listbox.curselection()
        self.selected_model = self.instrument_model.column_listbox.curselection()

        if changed_listbox == 'type':
            # Clear Manuf/Model
            self.instrument_manufacturer.column_listbox.delete(0, 'end')
            self.instrument_model.column_listbox.delete(0, 'end')
            self.instrument_serial.column_listbox.delete(0, 'end')
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])

            # Create New Manuf List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type == value[4]:
                    if value[2] not in self.filtered_list:
                        self.filtered_list.append(value[2])

            # Update Manufacturer
            for row_value in self.filtered_list:
                self.instrument_manufacturer.column_listbox.insert(
                    'end', row_value)

        elif changed_listbox == 'manu':
            self.instrument_model.column_listbox.delete(0, 'end')
            self.instrument_serial.column_listbox.delete(0, 'end')

            # Get Inputs
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])
            self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
                self.selected_manufacturer[0])

            # Create New Filtered List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type == value[4]:
                    if self.selected_manufacturer == value[2]:
                        if value[3] not in self.filtered_list:
                            self.filtered_list.append(value[3])

            # Update Model
            for row_value in self.filtered_list:
                self.instrument_model.column_listbox.insert(
                    'end', row_value)

        elif changed_listbox == 'modl':
            self.instrument_serial.column_listbox.delete(0, 'end')

            # Get Inputs
            self.selected_type = self.instrument_type.column_listbox.get(
                self.selected_type[0])
            self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
                self.selected_manufacturer[0])
            self.selected_model = self.instrument_model.column_listbox.get(
                self.selected_model[0])

            # Create New Filtered List
            self.filtered_list = []
            for value in self.table_values:
                if self.selected_type in value[4]:
                    if self.selected_manufacturer in value[2]:
                        if self.selected_model in value[3]:
                            self.filtered_list.append(value[5])

            # Update Serial
            for row_value in self.filtered_list:
                self.instrument_serial.column_listbox.insert(
                    'end', row_value)

    def query_unique_values(self):
        # Query Database
        column_titles, self.table_values = self.dbconn.get_table_values(
            'instruments')
        condit_titles, self.condition_values = self.dbconn.get_table_values(
            'conditions')
        calp_titles, self.cal_providers = self.dbconn.get_table_values(
            'cal_providers')

        # Create Unique Lists
        self.unique_conditions = self.get_unique_list(self.condition_values, 1)
        self.unique_types = self.get_unique_list(self.table_values, 4)
        self.unique_manufacturers = self.get_unique_list(self.table_values, 2)
        self.unique_models = self.get_unique_list(self.table_values, 3)
        self.unique_providers = self.get_unique_list(self.cal_providers, 1)

    def get_unique_list(self, column_values, column_num):
        # Generates Unique List from List
        unique_list = []
        for row in column_values:
            if row[column_num] not in unique_list:
                unique_list.append(row[column_num])
        unique_list.sort()
        return unique_list

    def verify(self):
        # Get Entry values
        self.selected_type = self.instrument_type.column_listbox.get('active')
        self.selected_manufacturer = self.instrument_manufacturer.column_listbox.get(
            'active')
        self.selected_model = self.instrument_model.column_listbox.get(
            'active')
        self.selected_serial = self.instrument_serial.column_listbox.get(
            'active')
        self.selected_cal_date = self.cal_date.get_date()
        self.selected_cal_due_date = self.cal_due_date.get_date()
        self.selected_provider = self.cal_provider.column_listbox.curselection()
        self.selected_provider = self.cal_provider.column_listbox.get(
            self.selected_provider[0])
        self.selected_condition = self.conditions_dropdown.get()

        if self.selected_condition not in self.unique_conditions:
            tk.messagebox.showerror(
                'Invalid', 'Please select a condition.')
        else:
            self.verify_pop = tk.messagebox.askyesno(
                'Verify Information', 'Pending Update: \n    Type: {} \n    Manufacturer: {} \n    Model: {} \n    SN: {} \n    Calibration Provider: {} \n    Calibration Date: {} \n    Calibration Due Date: {} \n \nUpdate Database?'.format(self.selected_type, self.selected_manufacturer, self.selected_model, self.selected_serial, self.selected_provider, str(self.selected_cal_date), str(self.selected_cal_due_date)))
            if self.verify_pop:
                passed = self.dbconn.update_calibration(self.selected_manufacturer, self.selected_model, self.selected_type,
                                                        self.selected_serial, self.selected_cal_date, self.selected_cal_due_date, self.selected_provider, self.selected_condition, self.parent.user)
                if passed:
                    tk.messagebox.showinfo(
                        'Added', 'Calibration updated in the Database')
                else:
                    tk.messagebox.showerror(
                        'Invalid', 'Serial has never been calibrated. \nPlease contact your Database Administrator')
            else:
                tk.messagebox.showinfo(
                    'Nothing Added', 'Nothing was added to the Database')

    def back(self):
        self.destroy()


class ColumnListBox(tk.Frame):
    def __init__(self, parent, name, label):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = name

        # Label
        self.listbox_label = tk.Label(self, text=label)
        self.listbox_label.pack(side='top')

        # Column Listbox
        self.column_listbox = tk.Listbox(
            self, selectmode='single', name=self.name)
        self.column_listbox.configure(exportselection=False)
        self.column_listbox.pack(side='left')

        # Scrollbars
        self.hsb = tk.Scrollbar(self, orient="horizontal",
                                command=self.column_listbox.xview)
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.column_listbox.yview)
        self.vsb.pack(side='left', fill='y')
        self.column_listbox.configure(yscrollcommand=self.vsb.set)
        # self.hsb.pack() This is not going at bottom >:(


if __name__ == "__main__":
    root = tk.Tk()
    ActionFrame(root).pack(side="top", fill="both", expand=True)
    root.geometry("750x400")
    root.title("Database Manager")
    root.mainloop()
