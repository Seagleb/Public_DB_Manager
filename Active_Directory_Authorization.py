'''
    Author: William Seagle
    Date: 04/04/2019
    Provides Active Directory Authentication
'''

from ldap3 import Server, Connection, ALL, NTLM, core, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
import subprocess

# -List of servers-
# hbm.com = Germany
# hbm3.hbm.com = Champaign
# hbmm3.hbm.com = Marlboro

CHAMPAIGN_SERVER = '###.##.#.###'
MARLBORO_SERVER = '###.##.#.###'
DOMAIN = 'HIDDEN'
adserver_to_dbserver = {
    "SERVER1": "###.##.##.##",
    "SERVER2": "###.##.##.##",
    "SERVER3": "###.##.##.##"
}


class ADConnection:
    def __init__(self, user, pswd):
        self.error = None
        self.user = user

        # Retrieve Domain Server from Host
        cmd = "echo %logonserver%"
        bytecode_response = subprocess.check_output(cmd, shell=True)
        dirty_response = bytecode_response.decode('ascii')
        dirty_response = dirty_response.strip()
        dynamic_server = dirty_response.strip('\\')
        try:
            self.db_server = adserver_to_dbserver[dynamic_server]
        except:
            self.db_server = 'Error'

        dynamic_server = dynamic_server + '.hbm.com'
        self.dynamic_server = dynamic_server

        # Server Setup
        self.server = Server(dynamic_server, get_info=ALL)

        # Server Connection
        try:
            self.connection = Connection(self.server, user='{}\\{}'.format(
                DOMAIN, user), password=pswd, raise_exceptions=True, authentication=NTLM)
            self.connection.bind()
        except core.exceptions.LDAPSocketOpenError as error:
            self.error = error
        except core.exceptions.LDAPInvalidCredentialsResult as error:
            self.error = error
        except core.exceptions.LDAPUnknownAuthenticationMethodError as error:
            self.error = error

    def get_user(self):
        return self.user


if __name__ == "__main__":
    c = ADConnection('sasdasd', 'asds')
    c.connection.unbind()
