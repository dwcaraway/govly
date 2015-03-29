__author__ = 'dave'
import pytest
import sure
from app.tasks import fbo
from moto import mock_s3
from app.tasks.fbo import FBOTask
from mock import MagicMock
from tempfile import mkstemp, mkdtemp

@pytest.fixture
def fbo():
    return FBOTask()


class TestFBO:

    def test_generate_daily_filenames(self, fbo):
        """
        Verifies that we can generate the daily files that we need from FTP
        """
        from datetime import datetime, timedelta

        #The date modified of the FBOFullXML is 1 day in the past
        yesterday = datetime.today() - timedelta(days=1)
        modifiedstr = yesterday.strftime(format="%Y%m%d%H%M%S")

        #Mock the FTP calls
        fbo.ftp.connect = MagicMock()
        fbo.ftp.login = MagicMock()
        fbo.ftp.sendcmd = MagicMock(return_value='213 '+modifiedstr)
        fbo.ftp.close = MagicMock()

        filenames = fbo.generate_daily_filenames()

        fbo.ftp.sendcmd.assert_called_with('MDTM datagov/FBOFullXML.xml')
        fbo.ftp.close.assert_called_with()

        #daily files are always off by 1, so
        #if fbofull was produced yesterday, we'd
        #expect to have the daily file from yesterday
        #however we would not have a daily file today
        filenames.should.have.length_of(1)
        filenames[0].should.contain(yesterday.strftime("%Y%m%d"))

    @mock_s3
    def test_find_ftp_files_to_sync(self, fbo):
        """
        Verifies that we can compare the FTP and S3 repos and generate
        a list of file differences that should be synchronized
        """

        #Mock FTP calls
        fbo.generate_daily_filenames = MagicMock(return_value=['somefbofeed'])
        fbo.ftp.connect = MagicMock()
        fbo.ftp.login = MagicMock()
        fbo.ftp.size = MagicMock(return_value=500)
        fbo.ftp.close = MagicMock()

        filenames = fbo.find_ftp_files_to_sync()

        fbo.generate_daily_filenames.assert_called_once_with()
        fbo.ftp.size.assert_called_with('somefbofeed')

        filenames.should.have.length_of(1)
        filenames[0].should.equal('somefbofeed')

    def test_sync_ftp_to_local_dir(self, fbo):

        fbo.ftp.connect = MagicMock()
        fbo.ftp.login = MagicMock()
        fbo.ftp.retrbinary = MagicMock()
        fbo.ftp.close = MagicMock()

        dir = mkdtemp()

        try:
            synced_files = fbo.sync_ftp_to_local_dir(filenames=['SomeFBOFeed'], storage=dir)
        finally:
            import shutil
            shutil.rmtree(dir)

        synced_files.should.have.length_of(1)
        synced_files[0].should.contain('SomeFBOFeed.xml.gz')

    @mock_s3
    def test_sync_local_files_to_s3(self, fbo):
        try:
            f, path = mkstemp()
            fbo.sync_local_files_to_s3(files=[path])
        finally:
            import os
            os.remove(path)

