__author__ = 'dave'

# Celery task to process the notices from FedBizOpps
# It downloads the FBO xml files and converts them to JSON-LD format
# and stores them into Amazon S3 for later processing

from ftplib import FTP
from tempfile import mkdtemp
from boto.s3.connection import S3Connection
from boto.utils import parse_ts
from boto.s3.key import Key
from os import path
import os
import math
from datetime import timedelta, datetime
from filechunkio import FileChunkIO
import gzip
import xmltodict


from ..framework.extensions import celery

# Important: This task REQUIRES the following environmental keys to be set
# AWS_ACCESS_KEY_ID - Your AWS Access Key ID
# AWS_SECRET_ACCESS_KEY - Your AWS Secret Access Key

S3_ARCHIVE_FORMAT = '.gz'
S3_EXTRACT_PREFIX = '/extract/fbo/'
S3_TRANSFORM_STAGING_PREFIX = '/transform/fbo/staging' #place where the JSON-LD files are stored

def convert_xml_to_jsonld(self):
    #TODO not fully implemented
    with open('./FBOFullXML.xml', 'r') as f:
        xmltodict.parse(f, item_depth=2, item_callback=self.process_notice)

def process_notice(self, _, notice):
    #TODO not fully implemented
    #write notice to the open data stream

    return True

@celery.task()
def sync_fbo_daily():
    """
    This task will sync the FBO's latest weekly intermediary files. We make a personal s3 copy of the data since the
    FBO ftp service is unreliable and tends to get hammered during peak hours. Files are stored to S3 in gzip format.
    """
    temp_dir = mkdtemp()

    conn = S3Connection()
    vitals_bucket = conn.get_bucket('fogmine-data')

    ftp = FTP('ftp.fbo.gov')
    ftp.login()

    try:

        # Take a look at the FBOFullXML.xml file. It contains a summary of all data up to the
        # date that it was created. So, we see when created and then look for the daily files published afterwards.
        # These are the updates. We can ignore all the daily files before the FBOFullXML.xml was created.

        sourceModifiedTime = ftp.sendcmd('MDTM datagov/FBOFullXML.xml')[4:]
        sourceModifiedDateTime = datetime.strptime(sourceModifiedTime, "%Y%m%d%H%M%S")

        delta = sourceModifiedDateTime - datetime.today()
        daily_files = []
        for delta in range(-1, delta.days+1, -1):
            file_date = datetime.today()+timedelta(days=delta)
            daily_files.append("FBOFeed{0}".format(file_date.strftime("%Y%m%d")))

        local_daily_files = []
        for f in daily_files:
            local_file_path = path.join(temp_dir, f+'.xml')

            #See if key already exists in S3, if so, move on
            k = vitals_bucket.get_key(path.basename(local_file_path)+S3_ARCHIVE_FORMAT)
            if k:
                continue

            #Save the FTP file locally
            try:
                with open(local_file_path, 'wb') as fileObj:
                    ftp.retrbinary('RETR ' + f, fileObj.write)
            except:
                #if exception happens, we weren't able to retrieve from the server (not found) so continue
                continue

            #Compress the file
            zipped_storage_path = path.join(temp_dir, path.basename(local_file_path)+S3_ARCHIVE_FORMAT)
            with open(local_file_path, 'rb') as f_in:
                with gzip.GzipFile(zipped_storage_path, 'wb') as myzip:
                    myzip.writelines(f_in)

            local_daily_files.append(zipped_storage_path)

    finally:
        ftp.close()

    for d in local_daily_files:
        # Put the daily files in S3
        k = Key(vitals_bucket)
        k.key = S3_EXTRACT_PREFIX+os.path.basename(d)
        k.set_contents_from_filename(d)

@celery.task
def sync_fbo_weekly():
    """
    This task will sync the latest full copy of FBO's xml and any intermediary files. It will overwrite the weekly file.
    We make a personal s3 copy of the data since the FBO ftp service is unreliable and tends to get hammered
    during peak hours. Files are stored to S3 in a gzipped format.

    Working files are stored in temp_dir and can be processed in other processes.
    """
    temp_dir = mkdtemp()
    storage_path = None

    conn = S3Connection()
    vitals_bucket = conn.get_bucket('fogmine-data')

    ftp = FTP('ftp.fbo.gov')
    ftp.login()

    try:
        sourceModifiedTime = ftp.sendcmd('MDTM datagov/FBOFullXML.xml')[4:]
        sourceModifiedDateTime = datetime.strptime(sourceModifiedTime, "%Y%m%d%H%M%S")
        filename = 'FBOFullXML'+sourceModifiedDateTime+'.xml'
        fullFBOKey = vitals_bucket.get_key(S3_EXTRACT_PREFIX+filename+S3_ARCHIVE_FORMAT)

        if not fullFBOKey or parse_ts(fullFBOKey.last_modified) < sourceModifiedDateTime:
            #Update S3 copy with latest

            print "downloading the latest full xml from repository"
            storage_path = path.join(temp_dir, filename)

            with open(storage_path, 'wb') as local_file:
                # Download the file a chunk at a time using RET
                ftp.retrbinary('RETR datagov/FBOFullXML.xml', local_file.write)

    finally:
        ftp.close()

    if not storage_path:
        return

    print "zipping the fbo full file"
    zipped_storage_path = path.join(temp_dir, 'FBOFullXML.xml'+S3_ARCHIVE_FORMAT)
    with open(storage_path, 'rb') as f_in:
        with gzip.GzipFile(zipped_storage_path, 'wb') as myzip:
            myzip.writelines(f_in)

    print "uploading the latest full xml to S3"
    # Put file to S3
    source_size = os.stat(zipped_storage_path).st_size

    # Create a multipart upload request
    mp = vitals_bucket.initiate_multipart_upload(S3_EXTRACT_PREFIX+os.path.basename(zipped_storage_path))

    # Use a chunk size of 50 MiB (feel free to change this)
    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / chunk_size))

    # Send the file parts, using FileChunkIO to create a file-like object
    # that points to a certain byte range within the original file. We
    # set bytes to never exceed the original file size.
    try:
        for i in range(chunk_count + 1):
            print "uploading chunk {0} of {1}".format(i+1, chunk_count+1)
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(zipped_storage_path, 'r', offset=offset,
                                 bytes=bytes) as fp:
                 mp.upload_part_from_file(fp, part_num=i + 1)
    finally:
        # Finish the upload
        mp.complete_upload()

        print "clearing any delta files from s3"
        keys_to_delete = vitals_bucket.list(prefix=S3_EXTRACT_PREFIX)
        for key in keys_to_delete:
            if 'FBOFeed' in key:
                vitals_bucket.delete_key(key)

        print "daily keys removed"

