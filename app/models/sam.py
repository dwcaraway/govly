from marshmallow import Schema, fields

from ..framework.sql import (
    db,
    Model
)

sam_fieldnames = ['DUNS', 'DUNS+4', 'CAGE CODE', 'DODAAC', 'SAM EXTRACT CODE', 'PURPOSE OF REGISTRATION',
                  'REGISTRATION DATE', 'EXPIRATION DATE', 'LAST UPDATE DATE', 'ACTIVATION DATE', 'LEGAL BUSINESS NAME',
                  'DBA NAME', 'COMPANY DIVISION', 'DIVISION NUMBER', 'SAM ADDRESS 1', 'SAM ADDRESS 2', 'SAM CITY',
                  'SAM PROVINCE OR STATE', 'SAM ZIP/POSTAL CODE', 'SAM ZIP CODE +4', 'SAM COUNTRY CODE',
                  'SAM CONGRESSIONAL DISTRICT', 'BUSINESS START DATE', 'FISCAL YEAR END CLOSE DATE', 'CORPORATE URL',
                  'ENTITY STRUCTURE', 'STATE OF INCORPORATION', 'COUNTRY OF INCORPORATION', 'BUSINESS TYPE COUNTER',
                  'BUS TYPE STRING', 'PRIMARY NAICS', 'NAICS CODE COUNTER', 'NAICS CODE STRING', 'PSC CODE COUNTER',
                  'PSC CODE STRING', 'CREDIT CARD USAGE', 'CORRESPONDENCE FLAG', 'MAILING ADDRESS LINE 1',
                  'MAILING ADDRESS LINE 2', 'MAILING ADDRESS CITY', 'MAILING ADDRESS ZIP/POSTAL CODE',
                  'MAILING ADDRESS ZIP CODE +4', 'MAILING ADDRESS COUNTRY', 'MAILING ADDRESS STATE OR PROVINCE',
                  'GOVT BUS POC FIRST NAME', 'GOVT BUS POC MIDDLE INITIAL', 'GOVT BUS POC LAST NAME',
                  'GOVT BUS POC TITLE', 'GOVT BUS POC ST ADD 1', 'GOVT BUS POC ST ADD 2', 'GOVT BUS POC CITY ',
                  'GOVT BUS POC ZIP/POSTAL CODE', 'GOVT BUS POC ZIP CODE +4', 'GOVT BUS POC COUNTRY CODE',
                  'GOVT BUS POC STATE OR PROVINCE', 'GOVT BUS POC U.S. PHONE', 'GOVT BUS POC U.S. PHONE EXT',
                  'GOVT BUS POC NON-U.S. PHONE', 'GOVT BUS POC FAX U.S. ONLY', 'GOVT BUS POC EMAIL ',
                  'ALT GOVT BUS POC FIRST NAME', 'ALT GOVT BUS POC MIDDLE INITIAL', 'ALT GOVT BUS POC LAST NAME',
                  'ALT GOVT BUS POC TITLE', 'ALT GOVT BUS POC ST ADD 1', 'ALT GOVT BUS POC ST ADD 2',
                  'ALT GOVT BUS POC CITY ', 'ALT GOVT BUS POC ZIP/POSTAL CODE', 'ALT GOVT BUS POC ZIP CODE +4',
                  'ALT GOVT BUS POC COUNTRY CODE', 'ALT GOVT BUS POC STATE OR PROVINCE', 'ALT GOVT BUS POC U.S. PHONE',
                  'ALT GOVT BUS POC U.S. PHONE EXT', 'ALT GOVT BUS POC NON-U.S. PHONE',
                  'ALT GOVT BUS POC FAX U.S. ONLY', 'ALT GOVT BUS POC EMAIL ', 'PAST PERF POC POC  FIRST NAME',
                  'PAST PERF POC POC  MIDDLE INITIAL', 'PAST PERF POC POC  LAST NAME', 'PAST PERF POC POC  TITLE',
                  'PAST PERF POC ST ADD 1', 'PAST PERF POC ST ADD 2', 'PAST PERF POC CITY ',
                  'PAST PERF POC ZIP/POSTAL CODE', 'PAST PERF POC ZIP CODE +4', 'PAST PERF POC COUNTRY CODE',
                  'PAST PERF POC STATE OR PROVINCE', 'PAST PERF POC U.S. PHONE', 'PAST PERF POC U.S. PHONE EXT',
                  'PAST PERF POC NON-U.S. PHONE', 'PAST PERF POC FAX U.S. ONLY', 'PAST PERF POC EMAIL ',
                  'ALT PAST PERF POC FIRST NAME', 'ALT PAST PERF POC MIDDLE INITIAL', 'ALT PAST PERF POC LAST NAME',
                  'ALT PAST PERF POC TITLE', 'ALT PAST PERF POC ST ADD 1', 'ALT PAST PERF POC ST ADD 2',
                  'ALT PAST PERF POC CITY ', 'ALT PAST PERF POC ZIP/POSTAL CODE', 'ALT PAST PERF POC ZIP CODE +4',
                  'ALT PAST PERF POC COUNTRY CODE', 'ALT PAST PERF POC STATE OR PROVINCE',
                  'ALT PAST PERF POC U.S. PHONE', 'ALT PAST PERF POC U.S. PHONE EXT',
                  'ALT PAST PERF POC NON-U.S. PHONE', 'ALT PAST PERF POC FAX U.S. ONLY', 'ALT PAST PERF POC EMAIL ',
                  'ELEC BUS POC FIRST NAME', 'ELEC BUS POC MIDDLE INITIAL', 'ELEC BUS POC LAST NAME',
                  'ELEC BUS POC TITLE', 'ELEC BUS POC ST ADD 1', 'ELEC BUS POC ST ADD 2', 'ELEC BUS POC CITY ',
                  'ELEC BUS POC ZIP/POSTAL CODE', 'ELEC BUS POC ZIP CODE +4', 'ELEC BUS POC COUNTRY CODE',
                  'ELEC BUS POC STATE OR PROVINCE', 'ELEC BUS POC U.S. PHONE', 'ELEC BUS POC U.S. PHONE EXT',
                  'ELEC BUS POC NON-U.S. PHONE', 'ELEC BUS POC FAX U.S. ONLY', 'ELEC BUS POC EMAIL',
                  'ALT ELEC POC BUS POC FIRST NAME', 'ALT ELEC POC BUS POC MIDDLE INITIAL',
                  'ALT ELEC POC BUS POC LAST NAME', 'ALT ELEC POC BUS POC TITLE', 'ALT ELEC POC BUS ST ADD 1',
                  'ALT ELEC POC BUS ST ADD 2', 'ALT ELEC POC BUS CITY ', 'ALT ELEC POC BUS ZIP/POSTAL CODE',
                  'ALT ELEC POC BUS ZIP CODE +4', 'ALT ELEC POC BUS COUNTRY CODE', 'ALT ELEC POC BUS STATE OR PROVINCE',
                  'ALT ELEC POC BUS U.S. PHONE', 'ALT ELEC POC BUS U.S. PHONE EXT', 'ALT ELEC POC BUS NON-U.S. PHONE',
                  'ALT ELEC POC BUS FAX U.S. ONLY', 'ALT ELEC POC BUS EMAIL ', 'NAICS EXCEPTION COUNTER',
                  'NAICS EXCEPTION STRING', 'DELINQUENT FEDERAL DEBT FLAG', 'EXCLUSION STATUS FLAG',
                  'SBA BUSINESS TYPES COUNTER', 'SBA BUSINESS TYPES STRING', 'NO PUBLIC DISPLAY FLAG',
                  'DISASTER RESPONSE COUNTER', 'DISASTER RESPONSE STRING', 'END OF RECORD INDICATOR']

class SamSchema(Schema):
    pass


class Sam(Model):
    """An entry in the SAM database"""

    __tablename__ = 'sam'

    duns = db.Column(db.Integer)
    duns_4 = db.Column(db.String(4))
    cage_code = db.Column(db.String(5))
    dodaac = db.Column(db.String(9))
    sam_extract_code = db.Column(db.String(1))
    purpose_of_registration = db.Column(db.String(2))
    registration_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    last_update_date = db.Column(db.Date)
    activation_date = db.Column(db.Date)
    legal_business_name = db.Column(db.String(120))
    dba_name = db.Column(db.String(120))
    company_division = db.Column(db.String(60))
    division_number = db.Column(db.String(10))
    sam_address_1 = db.Column(db.String(150))
    sam_address_2 = db.Column(db.String(150))
    sam_city = db.Column(db.String(40))
    sam_province_or_state = db.Column(db.String(55))
    sam_zip_postal_code = db.Column(db.String(50))
    sam_zip_code_4 = db.Column(db.String(4))
    sam_country_code = db.Column(db.String(3))
    sam_congressional_district = db.Column(db.String(10))
    business_start_date = db.Column(db.Date)
    fiscal_year_end_close_date = db.Column(db.String(4))
    corporate_url = db.Column(db.String(200))
    entity_structure = db.Column(db.String(2))
    state_of_incorporation = db.Column(db.String(2))
    country_of_incorporation = db.Column(db.String(3))
    business_type_counter = db.Column(db.String(4))
    bus_type_string = db.Column(db.String(220))
    primary_naics = db.Column(db.String(6))
    naics_code_counter = db.Column(db.String(4))
    naics_code_string = db.Column(db.String(12000))
    psc_code_counter = db.Column(db.String(4))
    psc_code_string = db.Column(db.String(2500))
    credit_card_usage = db.Column(db.String(1))
    correspondence_flag = db.Column(db.String(1))
    mailing_address_line_1 = db.Column(db.String(150))
    mailing_address_line_2 = db.Column(db.String(150))
    mailing_address_city = db.Column(db.String(40))
    mailing_address_zip_postal_code = db.Column(db.String(50))
    mailing_address_zip_code_4 = db.Column(db.String(4))
    mailing_address_country = db.Column(db.String(3))
    mailing_address_state_or_province = db.Column(db.String(55))
    govt_bus_poc_first_name = db.Column(db.String(65))
    govt_bus_poc_middle_initial = db.Column(db.String(3))
    govt_bus_poc_last_name = db.Column(db.String(65))
    govt_bus_poc_title = db.Column(db.String(50))
    govt_bus_poc_st_add_1 = db.Column(db.String(150))
    govt_bus_poc_st_add_2 = db.Column(db.String(150))
    govt_bus_poc_city = db.Column(db.String(40))
    govt_bus_poc_zip_postal_code = db.Column(db.String(50))
    govt_bus_poc_zip_code_4 = db.Column(db.String(4))
    govt_bus_poc_country_code = db.Column(db.String(30))
    govt_bus_poc_state_or_province = db.Column(db.String(55))
    govt_bus_poc_u_s_phone = db.Column(db.String(30))
    govt_bus_poc_u_s_phone_ext = db.Column(db.String(25))
    govt_bus_poc_non_u_s_phone = db.Column(db.String(30))
    govt_bus_poc_fax_u_s_only = db.Column(db.String(30))
    govt_bus_poc_email = db.Column(db.String(80))
    alt_govt_bus_poc_first_name = db.Column(db.String(65))
    alt_govt_bus_poc_middle_initial = db.Column(db.String(3))
    alt_govt_bus_poc_last_name = db.Column(db.String(65))
    alt_govt_bus_poc_title = db.Column(db.String(50))
    alt_govt_bus_poc_st_add_1 = db.Column(db.String(150))
    alt_govt_bus_poc_st_add_2 = db.Column(db.String(150))
    alt_govt_bus_poc_city = db.Column(db.String(40))
    alt_govt_bus_poc_zip_postal_code = db.Column(db.String(50))
    alt_govt_bus_poc_zip_code_4 = db.Column(db.String(4))
    alt_govt_bus_poc_country_code = db.Column(db.String(3))
    alt_govt_bus_poc_state_or_province = db.Column(db.String(55))
    alt_govt_bus_poc_u_s_phone = db.Column(db.String(30))
    alt_govt_bus_poc_u_s_phone_ext = db.Column(db.String(25))
    alt_govt_bus_poc_non_u_s_phone = db.Column(db.String(30))
    alt_govt_bus_poc_fax_u_s_only = db.Column(db.String(30))
    alt_govt_bus_poc_email = db.Column(db.String(80))
    past_perf_poc_poc_first_name = db.Column(db.String(65))
    past_perf_poc_poc_middle_initial = db.Column(db.String(3))
    past_perf_poc_poc_last_name = db.Column(db.String(65))
    past_perf_poc_poc_title = db.Column(db.String(50))
    past_perf_poc_st_add_1 = db.Column(db.String(150))
    past_perf_poc_st_add_2 = db.Column(db.String(150))
    past_perf_poc_city = db.Column(db.String(40))
    past_perf_poc_zip_postal_code = db.Column(db.String(50))
    past_perf_poc_zip_code_4 = db.Column(db.String(4))
    past_perf_poc_country_code = db.Column(db.String(3))
    past_perf_poc_state_or_province = db.Column(db.String(55))
    past_perf_poc_u_s_phone = db.Column(db.String(30))
    past_perf_poc_u_s_phone_ext = db.Column(db.String(25))
    past_perf_poc_non_u_s_phone = db.Column(db.String(30))
    past_perf_poc_fax_u_s_only = db.Column(db.String(30))
    past_perf_poc_email = db.Column(db.String(80))
    alt_past_perf_poc_first_name = db.Column(db.String(65))
    alt_past_perf_poc_middle_initial = db.Column(db.String(3))
    alt_past_perf_poc_last_name = db.Column(db.String(65))
    alt_past_perf_poc_title = db.Column(db.String(50))
    alt_past_perf_poc_st_add_1 = db.Column(db.String(150))
    alt_past_perf_poc_st_add_2 = db.Column(db.String(150))
    alt_past_perf_poc_city = db.Column(db.String(40))
    alt_past_perf_poc_zip_postal_code = db.Column(db.String(50))
    alt_past_perf_poc_zip_code_4 = db.Column(db.String(4))
    alt_past_perf_poc_country_code = db.Column(db.String(3))
    alt_past_perf_poc_state_or_province = db.Column(db.String(55))
    alt_past_perf_poc_u_s_phone = db.Column(db.String(30))
    alt_past_perf_poc_u_s_phone_ext = db.Column(db.String(25))
    alt_past_perf_poc_non_u_s_phone = db.Column(db.String(30))
    alt_past_perf_poc_fax_u_s_only = db.Column(db.String(30))
    alt_past_perf_poc_email = db.Column(db.String(80))
    elec_bus_poc_first_name = db.Column(db.String(65))
    elec_bus_poc_middle_initial = db.Column(db.String(3))
    elec_bus_poc_last_name = db.Column(db.String(65))
    elec_bus_poc_title = db.Column(db.String(50))
    elec_bus_poc_st_add_1 = db.Column(db.String(150))
    elec_bus_poc_st_add_2 = db.Column(db.String(150))
    elec_bus_poc_city_ = db.Column(db.String(40))
    elec_bus_poc_zip_postal_code = db.Column(db.String(50))
    elec_bus_poc_zip_code_4 = db.Column(db.String(4))
    elec_bus_poc_country_code = db.Column(db.String(3))
    elec_bus_poc_state_or_province = db.Column(db.String(55))
    elec_bus_poc_u_s_phone = db.Column(db.String(30))
    elec_bus_poc_u_s_phone_ext = db.Column(db.String(25))
    elec_bus_poc_non_u_s_phone = db.Column(db.String(30))
    elec_bus_poc_fax_u_s_only = db.Column(db.String(30))
    elec_bus_poc_email = db.Column(db.String(80))
    alt_elec_poc_bus_poc_first_name = db.Column(db.String(65))
    alt_elec_poc_bus_poc_middle_initial = db.Column(db.String(3))
    alt_elec_poc_bus_poc_last_name = db.Column(db.String(65))
    alt_elec_poc_bus_poc_title = db.Column(db.String(50))
    alt_elec_poc_bus_st_add_1 = db.Column(db.String(150))
    alt_elec_poc_bus_st_add_2 = db.Column(db.String(150))
    alt_elec_poc_bus_city = db.Column(db.String(40))
    alt_elec_poc_bus_zip_postal_code = db.Column(db.String(50))
    alt_elec_poc_bus_zip_code_4 = db.Column(db.String(4))
    alt_elec_poc_bus_country_code = db.Column(db.String(3))
    alt_elec_poc_bus_state_or_province = db.Column(db.String(55))
    alt_elec_poc_bus_u_s_phone = db.Column(db.String(30))
    alt_elec_poc_bus_u_s_phone_ext = db.Column(db.String(25))
    alt_elec_poc_bus_non_u_s_phone = db.Column(db.String(30))
    alt_elec_poc_bus_fax_u_s_only = db.Column(db.String(30))
    alt_elec_poc_bus_email = db.Column(db.String(80))
    naics_exception_counter = db.Column(db.String(4))
    naics_exception_string = db.Column(db.String(1100))
    delinquent_federal_debt_flag = db.Column(db.String(1))
    exclusion_status_flag = db.Column(db.String(1))
    sba_business_types_counter = db.Column(db.String(4))
    sba_business_types_string = db.Column(db.String(125))
    no_public_display_flag = db.Column(db.String(4))
    disaster_response_counter = db.Column(db.String(4))
    disaster_response_string = db.Column(db.String(75))

    def __repr__(self):
        return "{}"


