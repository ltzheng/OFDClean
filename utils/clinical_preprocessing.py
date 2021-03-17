import pandas as pd


column_names = ['id', 'facility_address_country', 'download_date', 'org_study_id', 'nct_id', 
                'brief_title', 'acronym', 'official_title', 'lead_sponsor_agency', 'source', 
                'overall_status', 'why_stopped', 'phase', 'study_type', 'study_design', 
                'number_of_arms', 'number_of_groups', 'enrollment', 'biospec_retention', 
                'eligibility_sampling_method', 'eligibility_gender', 'eligibility_minimum_age', 
                'eligibility_maximum_age', 'eligibility_healthy_volunteers', 'condition', 
                'measure', 'time_frame', 'safety_issue', 'drug_name']


def read_data(data_path):
    data = pd.read_csv(data_path, delimiter='::', names=column_names, header=None)

    return data
# data, sense_dict = read_data(data_path, senses_path)

# print('\nsense_dict:\n', sense_dict)  # sense->synonym