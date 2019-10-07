import sys
from sqlalchemy import create_engine
class ConnectDatabase:
    def __init__(self, dbname, userid, passwd, hostname = "localhost", port = "3306"):
        self.dbname     = dbname
        self.userid     = userid
        self.passwd     = passwd
        self.hostname   = hostname
        self.port       = port
        self.conn       = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(userid, passwd,
                                                            hostname, port, dbname)
        self.engine     = None
        self.stocks     = None
        self.min_date   = None
        self.max_date   = None

        self.setup()

    # Create DB engine
    def create_db_engine(self):
        try:
            engine = create_engine(self.conn)
        except Exception as e:
            print("Create DB engine Failed")
            sys.exit(1)
        return engine

    # Connect to DB
    def connect_db(self):
        engine = self.create_db_engine()
        try:
            engine.connect()
            self.engine = engine
            print("Database Connection is successful")
        except Exception as e:
            print("Connection to Database Failed")
            sys.exit(1)
    
    # Get all the stocks in underwatch_list
    def stocks_underwatch(self):
        result = self.run("SHOW TABLES")
        stocks = set()
        for each_row in result:
            stocks.add(each_row[0])
        self.stocks = stocks

    # Set minimum and maximum date
    def set_min_max_date(self):
        pass

    # Create table for New Stock
    def create_table(self, stock_name):
        query = ('CREATE TABLE {} (date DATE NOT NULL PRIMARY KEY, open DOUBLE NOT NULL, \
                  high DOUBLE NOT NULL, low DOUBLE NOT NULL, \
                  close DOUBLE NOT NULL, volume DOUBLE NOT NULL)'.format(stock_name))
        try:
            self.run(query, False)
            self.stocks.add(stock_name)
        except:
            print ('{} addition in database failed'.format(stock_name))

    # Database Connection Setup
    def setup(self):
        self.create_db_engine()
        self.connect_db()
        self.stocks_underwatch()

    # Run query
    def run(self, query, result_needed = True):
        if self.engine is None:
            self.connect_db()
        try:
            if (result_needed):
                result = self.engine.execute(query).fetchall()
                return result
            else:
               self.engine.execute(query)
        except Exception as e:
            print ('Query: {}\nQuery execution failed'.format(query))
            sys.exit(1)

    # Is Stock in underwatch list
    def is_underwatch(self, stock_name):
        return stock_name in self.stocks

    # Delete Stock
    def add_stock(self, stock_name):
        if self.is_underwatch(stock_name):
            try:
                query = ('DROP TABLE {}'.format(stock_name))
                self.run(query, False)
                self.stocks.discard(stock_name)
            except:
                print ('{} deletion from db failed'.format(stock_name))

    # Add Stock
    def add_stock(self, stock_name):
        if not self.is_underwatch(stock_name):
            try:
                self.create_table(stock_name)
            except:
                print('{} addition in db failed'.format(stock_name))

    # Update Stock
    def update_stock(self, stock_name):
        # Fill the data based on the number of rows and ignore if any data pre-exists
        pass

    # Upgrade Stock
    def upgrade_stock(self, stock_name):
        # Download data
        # Pre-process data
        # Truncate the table and then refill the data
        pass

    # Sync DB
    def sync_db(self):
        for stock in list(self.stocks):
            self.upgrade_stock(stock)

    # Print the stocks underwatch
    def print_stocks(self):
        for stock in list(self.stocks):
            print(stock)

if __name__ == "__main__":
    # This is a code to test ConnectDatabase class working
    dbname = 'nifty50'
    uid    = 'root'
    pwd    = 'root'
    conn = ConnectDatabase(dbname, uid, pwd)
    # Test Query Execution
    # query = ("SELECT max(date) FROM zeel")
    # print(conn.run(query))
    # conn.print_stocks()
    # Test db operations
    print (conn.is_underwatch('upl'))
    conn.add_stock('upl')
    print (conn.is_underwatch('upl'))
