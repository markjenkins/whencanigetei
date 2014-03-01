PROVINCES_AND_TERITORIES_ABREV_TO_NAME = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador', 
    'NT': 'Northwest Territories',
    'NS': 'Nova Scotia',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon',
    }

# use dictionary comprehension to reverse the above
PROVINCES_AND_TERITORIES_NAME_TO_ABREV = {
    name: abrev
    for abrev, name in PROVINCES_AND_TERITORIES_ABREV_TO_NAME.iteritems()
    }
