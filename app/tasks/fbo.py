__author__ = 'dave'

# Celery task to process the notices from FedBizOpps
# It downloads the FBO xml files and converts them to JSON-LD format
# and stores them into Amazon S3 for later processing

import xmltodict

class FBOProcessWeekly:

    output_file = None

    def convert_xml_to_jsonld(self):

        with open('./FBOFullXML.xml', 'r') as f:
            xmltodict.parse(f, item_depth=2, item_callback=process_notice)

    def process_notice(self, _, notice):

        #write notice to the open data stream

        return True