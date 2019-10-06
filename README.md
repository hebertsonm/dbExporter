# dbExporter

This tool was developed in Python 3, and intended to run as a Docker container.

This tool runs a postgres (mysql will be covered as well) database dump and store it on AWS S3 as a encrypted file.

Also, it makes database recovery and integrity test (intended to run as CronJob on Kubernetes).

It contains two features: Exporter and Importer. The first one generates a compressed dump file from a local/remote server, encrypts with AES algorithym, and upload the file to an AWS S3 bucket. The second feature consists of downloading the latest file from AWS S3 encrypted bucket, decrypt files, import to local database server, run tests, then submit a report to a specific Slack channel.

Be aware the Importer feature will be released soon.

## Compatibility

This current version was tested with Azure Database for Posgtresql, and self hosted servers on versions 9, 10, 11.

## Configure Slack 

Check the Slack's documentation to configure the API that will be used by this container for sendind messages to Slack channel.

https://api.slack.com/messaging/sending

## Configure and run the container

Then, ensure `env/var.txt` is set properly.

At least, build and run the container.

`docker build -t dbexporter .`

`docker run -d --rm --env-file env/var.txt --name dbexporter hebertsonm/dbexporter`

## Kubernetes manifest

To be updated.
