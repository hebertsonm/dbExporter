import database
import helpers
import config
import sys
import boto3
import os
import cryptography
import pyAesCrypt
import datetime

print('DBexporter has started..')

# Create config objects
db = config.PgConfig()
aws = config.AWS_S3()
enc = config.Encryption()

# Create /root/.pgpass for postgres authentication
pgpass_path = '/root/.pgpass'
db.create_pgpass(pgpass_path)

# Execute pg_dump with -Fc parameter
cmd = 'pg_dump -Fc --host=%s --port=%s --dbname=%s --username=%s -w' % (db.parameters())
cmd += ' > %s' % enc.input_file 
helpers.call_command(cmd)
if not os.path.exists(enc.input_file):
    print('Failure on dump file creation!')
    sys.exit(1)
print('Database dump generated for %s' % db.database)

# Dump file encryption
bufferSize = 64 * 1024
pyAesCrypt.encryptFile(enc.input_file, enc.output_file, enc.AES_key, bufferSize)
print('Dump file encrypted successfully! %s' % enc.output_file)

# Upload file into AWS S3
client = boto3.client('s3', 'us-west-2',
                       aws_access_key_id=aws.aws_access_key_id,
                       aws_secret_access_key=aws.aws_secret_access_key)
transfer = boto3.s3.transfer.S3Transfer(client)
transfer.upload_file(enc.output_file, aws.aws_bucket, helpers.basename(enc.output_file))
print('File %s has been uploaded to AWS S3 bucket!' % enc.output_file)

# List file on AWS S3 Bucktet
# Only return the contenst if we found some keys
bucket = client.list_objects_v2(Bucket=aws.aws_bucket)
obj = client.get_object(Bucket=aws.aws_bucket, Key=enc.output_file)
if obj is None:
    print('%s cannot be found on AWS S3 bucket.')
    sys.exit(1)

now = datetime.datetime.now()
print('End of application. Date: %s' % now.strftime('%Y/%h/%d, %H:%M:%S'))
