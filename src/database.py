import psycopg2

class PgDatabase():
    def __init__(self, **kwargs):

        if 'database' not in kwargs.keys():
            # if database name missing then rise exception
            raise Exception('Database name is mandatory! user, port, host, password are optional.')

        # defines default values for database connection
        self._param = {'user':'postgres',
                        'port':'5432',
                        'host':'127.0.0.1',
                        'password':'password',
                        'database':''}

        # fills empty arguments with default values
        for key, value in self._param.items():
            kwargs[key] = kwargs[key] if key in kwargs.keys() else value

        try:

            # creates an object for postgresql database connection
            self.conn = psycopg2.connect(user = kwargs['user'],
                                         password = kwargs['password'],
                                         host = kwargs['host'],
                                         port = kwargs['port'],
                                         database = kwargs['database'])

            self.cur = self.conn.cursor()

        except (Exception) as error:
            print(error)
            self.cur = None
            self.conn = None

    def query(self, query):
        try:

            # executes a single query command and returns all rows
            self.cur.execute(query)
            self.result = self.cur.fetchall()

        except (Exception) as error :
            print(error)
            self.result = None

        finally:
            return self.result

    def close(self):
        self.cur.close()
        self.conn.close()