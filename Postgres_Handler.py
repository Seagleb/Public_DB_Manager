'''
    Author: William Seagle
    Date: 04/11/2019
    Handles Postgres Queries and Database Communication
'''

import psycopg2
from datetime import datetime

TABLE_NAME_QUERY = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_SCHEMA = 'calibration_instruments' OR TABLE_SCHEMA = 'public') ORDER BY TABLE_NAME"

instrument_preset = {
    "Burster": {'print': True, 'setup_id': 21, 'pce_name': 'burster'},
    "CAN comm for PCE": {'print': False, 'setup_id': 3, 'pce_name': 'cancomm'},
    "CAN comm for PCE CITC-BURSTER": {'print': False, 'setup_id': 3, 'pce_name': 'cancomm'},
    "DC Source": {'print': False, 'setup_id': 6, 'pce_name': 'dcsource'},
    "DMM": {'print': True, 'setup_id': 8, 'pce_name': 'dmm'},
    "Digital Multimeter/Switcher": {'print': True, 'setup_id': 16, 'pce_name': 'switchmatrix'},
    "Dual Output DC Power Supply": {'print': True, 'setup_id': 14, 'pce_name': 'dcsource'},
    "Electronic Load": {'print': False, 'setup_id': 28, 'pce_name': 'eload'},
    "External Reference": {'print': True, 'setup_id': 31, 'pce_name': 'exreference'},
    "Frequency Counter": {'print': True, 'setup_id': 32, 'pce_name': 'fcount'},
    "Function Generator": {'print': True, 'setup_id': 12, 'pce_name': 'fgen'},
    "Multimeter / Data Acquisition System": {'print': True, 'setup_id': 8, 'pce_name': 'dmm'},
    "Power Supply": {'print': False, 'setup_id': 14, 'pce_name': 'powersupply'},
    "Rubidium Clock": {'print': True, 'setup_id': 30, 'pce_name': 'rclock'},
    "Temp/Humidity Sensor": {'print': True, 'setup_id': 18, 'pce_name': 'thSensor'},
    "Thermistor Probe": {'print': True, 'setup_id': 18, 'pce_name': 'thSensor'},
    "Virtual DC Source": {'print': False, 'setup_id': 7, 'pce_name': 'dcsource'},
    "Virtual DMM": {'print': False, 'setup_id': 9, 'pce_name': 'dmm'},
    "Virtual Eload": {'print': False, 'setup_id': 11, 'pce_name': 'eload'},
    "Virtual Function Generator": {'print': False, 'setup_id': 13, 'pce_name': 'fgen'},
    "Virtual Power Supply": {'print': False, 'setup_id': 15, 'pce_name': 'powersupply'},
    "Virtual Switch Matrix": {'print': False, 'setup_id': 17, 'pce_name': 'switchmatrix'},
    "Virtual Widget Comm": {'print': False, 'setup_id': 23, 'pce_name': 'widgetcomm'},
    "Virtual eDAQ Comm": {'print': False, 'setup_id': 22, 'pce_name': 'edaqcomm'},
    "Virtual temperature/humidity sensor": {'print': False, 'setup_id': 19, 'pce_name': 'thSensor'},
    "eDAQ comm for PCE": {'print': False, 'setup_id': 4, 'pce_name': 'edaqcomm'},
    "widget comm for PCE": {'print': False, 'setup_id': 5, 'pce_name': 'widgetcomm'}
}


class DBConnection:
    def __init__(self, host='localhost'):
        self.DATABASE = 'calibration_instruments'
        self.USER = 'postgres'
        self.PASSWORD = 'password'
        self.host = host
        self.conn = None
        self.error = None
        self.connect(self.host)

    def connect(self, host):
        try:
            # Connect
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(
                host=self.host, database=self.DATABASE, user=self.USER, password=self.PASSWORD)

            # Initialize Query Cursor
            self.cur = self.conn.cursor()

            # Test A Query
            print('PostgreSQL database version:')
            self.cur.execute('SELECT version()')
            db_version = self.cur.fetchone()
            print(db_version)
            print(self.conn)

        except (Exception, psycopg2.DatabaseError) as error:
            self.error = error

    def disconnect(self):
        self.cur.close()
        self.conn.close()
        print('Database connection closed.')

    def get_tables(self):
        self.cur.execute(TABLE_NAME_QUERY)
        tables = self.cur.fetchall()
        return tables

    def get_privilege(self, user):
        self.cur.execute(
            "SELECT privilege FROM user_privs WHERE (username = '{}')".format(user))
        privilege = self.cur.fetchone()
        try:
            return privilege[0]
        except:
            return privilege

    def get_stand_equip(self, stand):
        self.cur.execute(
            """SELECT * FROM Public."current_calequip" WHERE (name='{}')""".format(stand))
        equipment = self.cur.fetchall()

        self.cur.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'current_calequip'")
        column_names = self.cur.fetchall()

        return column_names, equipment

    def get_table_values(self, tbname=None, filtcol1=None, filtvalue1=None, filtcol2=None, filtval2=None):
        if tbname is not None:
            if filtcol1 and not filtcol2:
                self.cur.execute(
                    """SELECT * FROM Public."{}" WHERE ({}='{}')""".format(tbname, filtcol1, filtvalue1))
            elif filtcol1 and filtcol2:
                self.cur.execute(
                    """SELECT * FROM Public."{}" WHERE ({}='{}') AND ({}='{}')""".format(tbname, filtcol1, filtvalue1, filtcol2, filtval2))
            else:
                self.cur.execute('SELECT * FROM Public."{}"'.format(tbname))

            values = self.cur.fetchall()
            self.cur.execute(
                "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'".format(tbname))
            column_names = self.cur.fetchall()
            return column_names, values
        else:
            print("Nothing was entered")

    def year_add(self, date):
        list_date = date.split('-')
        list_date[0] = str(int(list_date[0]) + 1)
        year_added = list_date[0] + '-' + list_date[1] + '-' + list_date[2]
        return year_added

    def get_new_pkey(self, table):
        if table == 'pce_instr_def':
            self.cur.execute('SELECT max(def_id) FROM {}'.format(table))
        else:
            self.cur.execute('SELECT max(key) FROM {}'.format(table))
        max_pkey = self.cur.fetchone()
        new_pkey = max_pkey[0] + 1
        return new_pkey

    def get_last_location(self, serial):
        try:
            self.cur.execute(
                "SELECT key FROM instruments WHERE(manuf_sn='{}')".format(serial))
            instr_key = self.cur.fetchone()
            self.cur.execute(
                "SELECT max(key) FROM transfers WHERE(instr_key='{}')".format(str(instr_key[0])))
            last_known_key = self.cur.fetchone()
            self.cur.execute("SELECT to_loc_key FROM transfers WHERE(key='{}')".format(
                str(last_known_key[0])))
            last_known_loc_id = self.cur.fetchone()
            self.cur.execute("SELECT dscr FROM locations WHERE(key='{}')".format(
                str(last_known_loc_id[0])))
            last_known_loc = self.cur.fetchone()
            return last_known_loc[0]
        except:
            self.cur.execute("rollback")
            return False

    def check_daily_transfer_limit(self, instr_type, to_loc):
        date = datetime.today().strftime('%Y-%m-%d')
        location_exceptions = [4, 5, 11, 13, 16, 23 ,24 ,25]

        self.cur.execute(
            "SELECT key FROM locations WHERE(dscr='{}')".format(to_loc))
        to_id = self.cur.fetchone()

        # Check Exceptions
        if to_id[0] in location_exceptions:
            print('Instrument found in Location Exceptions')
            return True

        self.cur.execute(
            "SELECT instr_key FROM transfers WHERE(date='{}') AND (to_loc_key='{}')".format(date, str(to_id[0])))
        instr_ids = self.cur.fetchall()

        instr_descripts = []
        for instr_id in instr_ids:
            self.cur.execute(
                "SELECT dscr FROM instruments WHERE(key='{}')".format(str(instr_id[0])))
            instr_descripts.append(self.cur.fetchone())

        for itype in instr_descripts:
            if itype[0] == instr_type:
                return False
        return True

    def check_transfer(self, location, itype):
        self.cur.execute(
            "SELECT name FROM locations WHERE(dscr='{}')".format(location))
        loc_name = self.cur.fetchone()

        self.cur.execute(
            "SELECT * FROM current_calequip WHERE(name='{}') AND (dscr='{}')".format(loc_name[0], itype))
        existing_instruments = self.cur.fetchall()
        return existing_instruments

    def transfer_instrument(self, serial, from_loc, to_loc, condition, user, notes='None'):
        # Update Transfers Table
        new_trnsfr_pkey = self.get_new_pkey('transfers')
        sep = "', '"
        date = datetime.today().strftime('%Y-%m-%d')

        self.cur.execute(
            "SELECT key FROM instruments WHERE(manuf_sn='{}')".format(serial))
        instr_id = self.cur.fetchone()

        self.cur.execute(
            "SELECT key FROM locations WHERE(dscr='{}')".format(from_loc))
        from_id = self.cur.fetchone()

        self.cur.execute(
            "SELECT key FROM locations WHERE(dscr='{}')".format(to_loc))
        to_id = self.cur.fetchone()

        self.cur.execute(
            "SELECT key FROM conditions WHERE(name='{}')".format(condition))
        cond_key = self.cur.fetchone()

        if notes == '':
            notes = 'None'

        values = "'" + str(new_trnsfr_pkey) + sep + str(instr_id[0]) + sep + str(from_id[0]) + \
            sep + str(to_id[0]) + sep + str(cond_key[0]) + \
            sep + date + sep + notes + sep + date + "'"

        self.cur.execute(
            "INSERT INTO {} VALUES ({})".format('transfers', values))

        new_history_pkey = self.get_new_pkey('user_history')

        values = "'" + str(new_history_pkey) + sep + user + \
            sep + str(serial) + sep + 'Transfer' + "'"

        self.cur.execute(
            "INSERT INTO user_history VALUES ({})".format(values))

        self.conn.commit()

    def update_calibration(self, manuf_name, model_name, instr_type, serial, cal_date, cal_due_date, cal_provider, condition, user):
        # Update Calibrations Table
        sep = "', '"
        new_cal_pkey = self.get_new_pkey('calibrations')

        self.cur.execute(
            "SELECT key FROM instruments WHERE(manuf_sn='{}')".format(serial))
        instr_id = self.cur.fetchone()

        self.cur.execute(
            "SELECT key FROM cal_providers WHERE(name='{}')".format(cal_provider))
        cal_prov_key = self.cur.fetchone()

        try:
            self.cur.execute(
                "SELECT max(key) FROM calibrations WHERE(instr_key='{}')".format(instr_id[0]))
            prev_cal_key = self.cur.fetchone()

            self.cur.execute(
                "SELECT end_cond_key FROM calibrations WHERE(key='{}')".format(prev_cal_key[0]))
            start_cond_key = self.cur.fetchone()

            self.cur.execute(
                "SELECT key FROM conditions WHERE(name='{}')".format(condition))
            cond_end_key = self.cur.fetchone()

            CERT_LOC = 'HBMI'
            NOTES = 'None'
            date = datetime.today().strftime('%Y-%m-%d')

            values = "'" + str(new_cal_pkey) + sep + str(instr_id[0]) + sep + str(cal_prov_key[0]) + sep + str(start_cond_key[0]) + \
                sep + str(cond_end_key[0]) + sep + str(cal_date) + sep + str(cal_due_date) + \
                sep + CERT_LOC + sep + NOTES + sep + date + sep + date + "'"

            self.cur.execute(
                "INSERT INTO {} VALUES ({})".format('calibrations', values))

            new_history_pkey = self.get_new_pkey('user_history')

            values = "'" + str(new_history_pkey) + sep + user + \
                sep + str(serial) + sep + 'Update Calibration' + "'"

            self.cur.execute(
                "INSERT INTO user_history VALUES ({})".format(values))

            self.conn.commit()
            return True
        except:
            self.cur.execute("rollback")
            return False

    def add_instrument(self, manuf_name, model_name, instr_type, serial, cal_date, cal_due_date, cal_provider, user):
        # Update Instrument Table
        new_instrument_pkey = self.get_new_pkey('instruments')
        date = datetime.today().strftime('%Y-%m-%d')
        prnt_on_crt = instrument_preset[instr_type]['print']
        sep = "', '"
        values = "'" + str(new_instrument_pkey) + sep + str(prnt_on_crt) + sep + manuf_name + \
            sep + model_name + sep + instr_type + sep + \
            serial + sep + date + sep + date + "'"
        self.cur.execute(
            "INSERT INTO {} VALUES ({})".format('instruments', values))

        # Update Transfer Table
        new_transfer_pkey = self.get_new_pkey('transfers')
        values = "'" + str(new_transfer_pkey) + sep + str(new_instrument_pkey) + sep + "5" + sep + \
            "24" + sep + "1" + sep + \
            date + sep + date + "'"
        self.cur.execute(
            "INSERT INTO {} VALUES ({})".format('transfers (key, instr_key, from_loc_key, to_loc_key, cond_key, date, date_created) ', values))

        # Update pce_intsr_def Table
        new_pce_pkey = self.get_new_pkey('pce_instr_def')
        setup_id = instrument_preset[instr_type]['setup_id']
        values = "'" + str(new_pce_pkey) + sep + \
            str(new_instrument_pkey) + sep + str(setup_id) + "'"
        self.cur.execute(
            "INSERT INTO {} VALUES ({})".format('pce_instr_def', values))

        # Update instrument_identifier table
        if instr_type == 'Digital Multimeter/Switcher':
            # Applies to Keithley DMM/Switches Because Two In One
            new_identifier_pkey_one = self.get_new_pkey(
                'instrument_identifier')
            new_identifier_pkey_two = new_identifier_pkey_one + 1
            pce_name_one = 'dmm'
            pce_name_two = 'switchmatrix'

            # DMM Entry
            values = "'" + str(new_instrument_pkey) + sep + pce_name_one + \
                sep + serial + sep + str(new_identifier_pkey_one) + "'"
            self.cur.execute(
                "INSERT INTO {} VALUES ({})".format('instrument_identifier', values))

            # Switch Entry
            values = "'" + str(new_instrument_pkey) + sep + pce_name_two + \
                sep + serial + sep + str(new_identifier_pkey_two) + "'"
            self.cur.execute(
                "INSERT INTO {} VALUES ({})".format('instrument_identifier', values))

        else:
            new_identifier_pkey = self.get_new_pkey('instrument_identifier')
            new_pce_name = instrument_preset[instr_type]['pce_name']
            values = "'" + str(new_instrument_pkey) + sep + new_pce_name + \
                sep + serial + sep + str(new_identifier_pkey) + "'"
            self.cur.execute(
                "INSERT INTO {} VALUES ({})".format('instrument_identifier', values))

        # Update calibrations Table
        new_cal_pkey = self.get_new_pkey('calibrations')
        self.cur.execute(
            "SELECT key FROM cal_providers WHERE(name = '{}')".format(cal_provider))
        cal_prov_key = self.cur.fetchone()
        values = "'" + str(new_cal_pkey) + sep + str(new_instrument_pkey) + sep + str(cal_prov_key[0]) + sep + '1' + sep + '1' + sep + str(
            cal_date) + sep + str(cal_due_date) + sep + 'HBMI' + sep + 'None' + sep + date + "'"
        self.cur.execute(
            "INSERT INTO {} VALUES ({})".format('calibrations', values))

        new_history_pkey = self.get_new_pkey('user_history')

        values = "'" + str(new_history_pkey) + sep + user + \
            sep + str(serial) + sep + 'Added Instrument' + "'"

        self.cur.execute(
            "INSERT INTO user_history VALUES ({})".format(values))

        self.conn.commit()

    def get_serials(self, model, itype, manufacturer):
        self.cur.execute("SELECT manuf_sn FROM instruments WHERE (manuf_name = '{}') AND (model_name = '{}') AND (dscr = '{}')".format(
            manufacturer, model, itype))
        values = self.cur.fetchall()
        serials = []
        for value in values:
            serials.append(value[0])
        return serials

    def check_exists(self, model, itype, manufacturer, serial):
        self.cur.execute("SELECT * FROM instruments WHERE (manuf_name = '{}') AND (model_name = '{}') AND (dscr = '{}') AND (manuf_sn = '{}')".format(
            manufacturer, model, itype, serial))
        response = self.cur.fetchone()
        if response:
            return True
        else:
            return False


if __name__ == '__main__':
    c = DBConnection('localhost')
    # check = c.check_daily_transfer_limit('DMME', 'CalStand 01')
    # print(check)
    # c.check_exists(
    #     '5665', 'Thermistor Probe', 'HBM-Urbana', '06054')

    # c.get_privilege("seagle")
    # instruments_columns, instruments_values = c.get_table_values("instruments")

    # MODELNAME = '8842A'
    # MANUFACTURER = 'Keithley'
    # INSTRTYPE = 'DMM'
    # SERIAL = 'LASTESTENTRY312'
    # c.add_instrument(MANUFACTURER, MODELNAME, INSTRTYPE, SERIAL)

    # column_titles, column_values = c.get_table_values('instruments')
    # for value in column_values:
    #     print (value[0])

    # print(cal_providers_columns)
    # for i in range(len(tables)):
    #     print(tables[i][0])
    #c.insert_entry('instruments', values)

    c.disconnect()
