import os

class Config():
    def __init__(self):
        self._config = {}

    def get_property(self, property_name, default_value=None):
        if property_name not in self._config.keys():
            _value = None
        _value = self._config[property_name]

        if ((_value is None) and default_value):
            return default_value
        return _value


class PgConfig(Config):
    def __init__(self):
        self._config = {
            'pghost': os.getenv('PGHOST'),
            'pghostaddr': os.getenv('PGHOSTADDR'),
            'pgport': os.getenv('PGPORT'),
            'pgdatabase': os.getenv('PGDATABASE'),
            'pguser': os.getenv('PGUSER'),
            'pgpassword': os.getenv('PGPASSWORD'),
            'pgsslmode': os.getenv('PGSSLMODE'),
            'pgsslcert': os.getenv('PGSSLCERT'),
            'pgsslkey': os.getenv('PGSSLKEY')
        }
    
    @property
    def host(self):
        return self.get_property('pghost', '127.0.0.1')

    @property
    def port(self):
        return self.get_property('pgport', '5432')

    @property
    def database(self):
        return self.get_property('pgdatabase', 'postgres')

    @property
    def user(self):
        return self.get_property('pguser', 'postgres')

    @property
    def hostaddr(self):
        return self.get_property('pghostaddr')

    @property
    def password(self):
        return self.get_property('pgpassword')

    @property
    def sslmode(self):
        return self.get_property('pgsslmode') 

    @property
    def sslcert(self):
        return self.get_property('pgsslcert') 

    @property
    def sslkey(self):
        return self.get_property('pgsslkey') 
    
    def parameters(self, flag=False):
        if flag:
            # include password if flag is True
            return (self.host, self.port, self.database, self.user, self.password)
        else:
            # Usually PGPASSWORD is set on .pgpass file
            return (self.host, self.port, self.database, self.user)

    def create_pgpass(self, path):
        # Create /path/.pgpass for postgres authentication
        try:
            pgpass_path = '/root/.pgpass'
            pgpass = open(pgpass_path,'w+')
            content = '%s:%s:%s:%s:%s' % (self.parameters(True))
            pgpass.write(content)
            pgpass.close()
            os.chmod(pgpass_path, 0o600)
        except Exception as error:
            raise Exception(error)
        return True

class Encryption(Config):
    def __init__(self):
        self._config = {
            'input_file': os.getenv('INPUT_FILE'),
            'output_file': os.getenv('INPUT_FILE') + '.enc',
            'AES_key': os.getenv('AES_KEY')
        }

    @property
    def input_file(self):
        return self.get_property('input_file')

    @property
    def output_file(self):
        return self.get_property('output_file')

    @property
    def AES_key(self):
        return self.get_property('AES_key')        

class AWS_S3(Config):
    def __init__(self):
        self._config = {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'aws_bucket': os.getenv('AWS_BUCKET')
        }
        
    @property
    def aws_access_key_id(self):
        return self.get_property('aws_access_key_id')

    @property
    def aws_secret_access_key(self):
        return self.get_property('aws_secret_access_key') 

    @property
    def aws_bucket(self):
        return self.get_property('aws_bucket') 

class Slack(Config):
    def __init__(self):
        self._config = {
            'slack_api': os.getenv('SLACK_API'),
            'slack_channel': os.getenv('SLACK_CHANNEL')
        }

    @property
    def slack_api(self):
        return self.get_property('slack_api')

    @property
    def slack_channel(self):
        return self.get_property('slack_channel')


if __name__ == "__main__":

    pg = PgConfig()
    pg._config['pghost'] = None
    print(pg.host)
