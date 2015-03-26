__author__ = 'dave'
import re
import csv
import ssl
import datetime
from zipfile import ZipFile
try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO
from datetime import date
from urllib2 import urlopen, URLError
import tempfile
import json
from app.models.sam import Sam
from app.framework.sql import db

class SamCopy:

    def __init__(self, app):
        self.app = app

    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

    sam_fieldnames = ['DUNS', 'DUNS+4', 'CAGE CODE', 'DODAAC', 'SAM EXTRACT CODE', 'PURPOSE OF REGISTRATION', 'REGISTRATION DATE', 'EXPIRATION DATE', 'LAST UPDATE DATE', 'ACTIVATION DATE', 'LEGAL BUSINESS NAME', 'DBA NAME', 'COMPANY DIVISION', 'DIVISION NUMBER', 'SAM ADDRESS 1', 'SAM ADDRESS 2', 'SAM CITY', 'SAM PROVINCE OR STATE', 'SAM ZIP/POSTAL CODE', 'SAM ZIP CODE +4', 'SAM COUNTRY CODE', 'SAM CONGRESSIONAL DISTRICT', 'BUSINESS START DATE', 'FISCAL YEAR END CLOSE DATE', 'CORPORATE URL', 'ENTITY STRUCTURE', 'STATE OF INCORPORATION', 'COUNTRY OF INCORPORATION', 'BUSINESS TYPE COUNTER', 'BUS TYPE STRING', 'PRIMARY NAICS', 'NAICS CODE COUNTER', 'NAICS CODE STRING', 'PSC CODE COUNTER', 'PSC CODE STRING', 'CREDIT CARD USAGE', 'CORRESPONDENCE FLAG', 'MAILING ADDRESS LINE 1', 'MAILING ADDRESS LINE 2', 'MAILING ADDRESS CITY', 'MAILING ADDRESS ZIP/POSTAL CODE', 'MAILING ADDRESS ZIP CODE +4', 'MAILING ADDRESS COUNTRY', 'MAILING ADDRESS STATE OR PROVINCE', 'GOVT BUS POC FIRST NAME', 'GOVT BUS POC MIDDLE INITIAL', 'GOVT BUS POC LAST NAME', 'GOVT BUS POC TITLE', 'GOVT BUS POC ST ADD 1', 'GOVT BUS POC ST ADD 2', 'GOVT BUS POC CITY ', 'GOVT BUS POC ZIP/POSTAL CODE', 'GOVT BUS POC ZIP CODE +4', 'GOVT BUS POC COUNTRY CODE', 'GOVT BUS POC STATE OR PROVINCE', 'GOVT BUS POC U.S. PHONE', 'GOVT BUS POC U.S. PHONE EXT', 'GOVT BUS POC NON-U.S. PHONE', 'GOVT BUS POC FAX U.S. ONLY', 'GOVT BUS POC EMAIL ', 'ALT GOVT BUS POC FIRST NAME', 'ALT GOVT BUS POC MIDDLE INITIAL', 'ALT GOVT BUS POC LAST NAME', 'ALT GOVT BUS POC TITLE', 'ALT GOVT BUS POC ST ADD 1', 'ALT GOVT BUS POC ST ADD 2', 'ALT GOVT BUS POC CITY ', 'ALT GOVT BUS POC ZIP/POSTAL CODE', 'ALT GOVT BUS POC ZIP CODE +4', 'ALT GOVT BUS POC COUNTRY CODE', 'ALT GOVT BUS POC STATE OR PROVINCE', 'ALT GOVT BUS POC U.S. PHONE', 'ALT GOVT BUS POC U.S. PHONE EXT', 'ALT GOVT BUS POC NON-U.S. PHONE', 'ALT GOVT BUS POC FAX U.S. ONLY', 'ALT GOVT BUS POC EMAIL ', 'PAST PERF POC POC  FIRST NAME', 'PAST PERF POC POC  MIDDLE INITIAL', 'PAST PERF POC POC  LAST NAME', 'PAST PERF POC POC  TITLE', 'PAST PERF POC ST ADD 1', 'PAST PERF POC ST ADD 2', 'PAST PERF POC CITY ', 'PAST PERF POC ZIP/POSTAL CODE', 'PAST PERF POC ZIP CODE +4', 'PAST PERF POC COUNTRY CODE', 'PAST PERF POC STATE OR PROVINCE', 'PAST PERF POC U.S. PHONE', 'PAST PERF POC U.S. PHONE EXT', 'PAST PERF POC NON-U.S. PHONE', 'PAST PERF POC FAX U.S. ONLY', 'PAST PERF POC EMAIL ', 'ALT PAST PERF POC FIRST NAME', 'ALT PAST PERF POC MIDDLE INITIAL', 'ALT PAST PERF POC LAST NAME', 'ALT PAST PERF POC TITLE', 'ALT PAST PERF POC ST ADD 1', 'ALT PAST PERF POC ST ADD 2', 'ALT PAST PERF POC CITY ', 'ALT PAST PERF POC ZIP/POSTAL CODE', 'ALT PAST PERF POC ZIP CODE +4', 'ALT PAST PERF POC COUNTRY CODE', 'ALT PAST PERF POC STATE OR PROVINCE', 'ALT PAST PERF POC U.S. PHONE', 'ALT PAST PERF POC U.S. PHONE EXT', 'ALT PAST PERF POC NON-U.S. PHONE', 'ALT PAST PERF POC FAX U.S. ONLY', 'ALT PAST PERF POC EMAIL ', 'ELEC BUS POC FIRST NAME', 'ELEC BUS POC MIDDLE INITIAL', 'ELEC BUS POC LAST NAME', 'ELEC BUS POC TITLE', 'ELEC BUS POC ST ADD 1', 'ELEC BUS POC ST ADD 2', 'ELEC BUS POC CITY ', 'ELEC BUS POC ZIP/POSTAL CODE', 'ELEC BUS POC ZIP CODE +4', 'ELEC BUS POC COUNTRY CODE', 'ELEC BUS POC STATE OR PROVINCE', 'ELEC BUS POC U.S. PHONE', 'ELEC BUS POC U.S. PHONE EXT', 'ELEC BUS POC NON-U.S. PHONE', 'ELEC BUS POC FAX U.S. ONLY', 'ELEC BUS POC EMAIL', 'ALT ELEC POC BUS POC FIRST NAME', 'ALT ELEC POC BUS POC MIDDLE INITIAL', 'ALT ELEC POC BUS POC LAST NAME', 'ALT ELEC POC BUS POC TITLE', 'ALT ELEC POC BUS ST ADD 1', 'ALT ELEC POC BUS ST ADD 2', 'ALT ELEC POC BUS CITY ', 'ALT ELEC POC BUS ZIP/POSTAL CODE', 'ALT ELEC POC BUS ZIP CODE +4', 'ALT ELEC POC BUS COUNTRY CODE', 'ALT ELEC POC BUS STATE OR PROVINCE', 'ALT ELEC POC BUS U.S. PHONE', 'ALT ELEC POC BUS U.S. PHONE EXT', 'ALT ELEC POC BUS NON-U.S. PHONE', 'ALT ELEC POC BUS FAX U.S. ONLY', 'ALT ELEC POC BUS EMAIL ', 'NAICS EXCEPTION COUNTER', 'NAICS EXCEPTION STRING', 'DELINQUENT FEDERAL DEBT FLAG', 'EXCLUSION STATUS FLAG', 'SBA BUSINESS TYPES COUNTER', 'SBA BUSINESS TYPES STRING', 'NO PUBLIC DISPLAY FLAG', 'DISASTER RESPONSE COUNTER', 'DISASTER RESPONSE STRING', 'END OF RECORD INDICATOR']
    sam_table_fields = [re.sub(r'\W+\+*\W*', '_', x.strip().lower()) for x in sam_fieldnames]

    sam_date_fields = ['registration_date',
                       'expiration_date',
                       'last_update_date',
                       'activation_date',
                       'business_start_date']

    url_base = 'https://www.sam.gov/SAMPortal/extractfiledownload?role=WW&version=SAM&filename=SAM_PUBLIC_MONTHLY_'

    def download_and_unzip_latest(self):
        """
        The Sam.gov website uses AJAX and is complicated to scrape, so we just guess the filename until one url succeeds.
        Next we download the datafile to temp file, unzip the file to another temp file and return the absolute path to that
        unzipped file.
        """
        today = date.today()

        #Hack to not verify Sam.gov ssl cert since SAM is currently broken and using weak sha-1 rsa encryption
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        tempdir_path = tempfile.mkdtemp()
        local_zip_file_path = tempfile.mkstemp(dir=tempdir_path)[1]
        local_unzipped_file_path = tempfile.mkstemp(dir=tempdir_path)[1]

        for x in range(today.day+1, 0, -1):
            url = "{0}{1}.ZIP".format(self.url_base, date(today.year, today.month, x).strftime("%Y%m%d"))
            try:
                remote_data = urlopen(url, context=gcontext)

                # Save the large data file to a local temporary file
                with open(local_zip_file_path, 'w') as l:
                    l.write(remote_data.read())

                with ZipFile(local_zip_file_path, 'r') as z:
                    filename = re.search('([a-zA-Z0-9_-]*)\.ZIP', url).group(1)
                    with z.open('{}.dat'.format(filename)) as f:
                        with open(local_unzipped_file_path, 'w') as uz:
                            uz.write(f.read())

                return local_unzipped_file_path

            except URLError:
                continue

        return None

    def read_business(self, file_path):
        """
        Copies all the businesses in the data extract into a postgres table. Note that any existing entries will
        be dropped from this table on load.
        """
        #See tab 2 on https://www.sam.gov/sam/transcript/SAM%20Master%20Extract%20Mapping%20v5.1%20Public%20File%20Layout.xlsx
        with open(file_path, 'r') as f:

            #TODO read first line, which is header, check the version
            header = f.readline()
            header_fields = header.split()
            date_of_data = header_fields[3]
            data_version = header_fields[-1]

            #check data version
            assert '5100' in data_version

            for business in csv.DictReader(f, fieldnames=self.sam_table_fields, dialect='piper'):

                if business['duns'] is 'EOF':
                    break

                for field in self.sam_date_fields:
                    business[field] = datetime.datetime.strptime(business[field], "%Y%m%d").date() \
                        if business[field] else None

                yield business

if __name__ == '__main__':
    from app import create_app
    app = create_app().mounts['/api']
    ctx = app.test_request_context()
    ctx.push()

    s = SamCopy(app=app)

    unzipped_data_path = s.download_and_unzip_latest()
    # unzipped_data_path = '/Users/dave/Downloads/SAM_PUBLIC_MONTHLY_20150301.dat'

    conn = db.engine.connect()
    try:
        db.engine.execute('drop table if exists sam;')
        db.create_all()

        conn.execute(Sam.__table__.insert(), [biz for biz in s.read_business(unzipped_data_path)])

        batch = []

        for biz in s.read_business(unzipped_data_path):
            batch.append(biz)

            if len(batch) >= 100000:
                print 'inserting 100,000 sam entries'
                conn.execute(Sam.__table__.insert(), batch)
                batch = []

        #Insert any remaining
        conn.execute(Sam.__table__.insert(), batch)

    finally:
        conn.close()
        ctx.pop()