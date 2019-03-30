from generic.utils import *
from sqlalchemy import create_engine

class ConnectDatabase:
    def __init__(self, dbname, userid, passwd, hostname = "localhost", port = "3306"):
        self.dbname     = dbname
        self.userid     = userid
        self.passwd     = passwd
        self.hostname   = hostname
        self.port       = port
        self.conn       = ""

    def get_userid(self):
        return self.userid

    def get_passwd(self):
        return self.passwd

    def get_dbname(self):
        return self.dbname

    def get_hostname(self):
        return self.hostname

    def get_port(self):
        return self.port

    def get_conn(self):
        return self.conn

    # Create DB engine
    def create_db_engine(self):
        self.conn = 'mysql+pymysql://' + str(self.get_userid()) + ":" + str(self.get_passwd()) + \
                     '@' + str(self.get_hostname()) + ":" + str(self.get_port()) + "/" + str(self.get_dbname())
        try:
            engine = create_engine(self.get_conn())
        except Exception as e:
            msg = "Create DB engine Failed"
            print(e)
            print_err_exit(msg)
        return engine

    # Run query
    def run(self, query, result_needed = True):
        engine = self.create_db_engine()
        try:
            engine.connect()
        except Exception as e:
            msg = "Connection to Database Failed"
            print(e)
            print_err_exit(msg)

        try:
            if (result_needed):
                result = engine.execute(query).fetchall()
                return result
            else:
                engine.execute(query)
        except Exception as e:
            print ("Query:")
            print (query)
            msg = "Query execution failed"
            print(e)
            print_err_exit(msg)

if __name__ == "__main__":
    pass