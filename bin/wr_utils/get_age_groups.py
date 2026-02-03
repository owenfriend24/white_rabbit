import pandas as pd

def get_age_years(subject):
    ref = pd.read_csv('/home1/09123/ofriend/analysis/white_rabbit/templates/randomise_measures.csv')
    sub_ref = ref[ref['subject'] == subject]
    age = sub_ref.age.values[0]
    return age

def get_age_group(subject):
    age = get_age_years(subject)

    if age < 10:
        return 'child'
    elif (age >= 10) & (age < 13):
        return 'adolescent'
    else:
        return 'adult'




