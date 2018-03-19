"""

This is a Unit Testing file for model.py. This file tests most important functions in model.py

Author: Junxiong Liu

"""

import pandas as pd
import model as mod
import numpy as np

def test_filter():
    """Testing filter function."""

    # initialize for testing
    # df
    df_inputs = {
        'region': [1, 3, 2, 8, 9, 7, 1, 6, 5, 4],
        'degree_offered': [2, 1, 2, 3, 3, 1, 2, 3, 2, 1],
        'num_undergrad': [1000, 500, 330, 7999, 8295, 16532, 11000, 42131, 500, 66],
        'CONTROL': [1, 2, 1, 2, 2, 1, 2, 1, 2, 1]
    }   
    df_testing = pd.DataFrame(data=df_inputs)
    # strict criteria
    region = [1, 2, 3, 5, 7, 8, 9]
    degree = [1, 2]
    size_range = [1, 100000]
    CONTROL = [1]
    strict_criteria_testing = [region, degree, size_range, CONTROL]

    # actual output
    actual = mod.filter(df_testing, strict_criteria_testing)

    # expected output
    col = ['CONTROL', 'degree_offered', 'num_undergrad', 'region']
    idx = [0, 2, 5]
    expected = pd.DataFrame([[1, 2, 1000, 1], [1, 2, 330, 2], [1, 1, 16532, 7]], index=idx, columns=col)

    try:
        # check type
        assert isinstance(expected, pd.DataFrame)
        # check expected output
        assert actual.equals(expected)
        print ('Test for filter function passed!')
    except:
        print ('Test for filter function FAILED!')
    print ('-----------------------------------------------------------')        
    print ('')

def test_modeling():
    """Testing modeling function (two situations: with or without SAT scores）."""

    # initialize for testing
    # df
    df_inputs = {
        'INSTNM': ['Academy', 'Glenview', 'Magic', 'Random', 'Mac', 'Sleeping Beauty', 'Quasi'],
        'CITY': ['Chicago', 'New York City', 'Los Angeles', 'Houston', 'San Diego', 'Minneapolis', 'Chicago'],
        'state': ['IL', 'NY', 'CA', 'TX', 'CA', 'MN', 'IL'],
        'ADM_RATE': [0.335, 0.221, 0.972, 0.885, 0.047, 0.552, 0.603],
        'SATVRMID': [570, 620, np.nan, np.nan, 770, np.nan, 410],
        'SATMTMID': [583, 633, np.nan, np.nan, 770, np.nan, 450],
        'num_undergrad': [3201, 2244, 688, 7555, 10203, 15666, 8828],
        'prop_arts_human': [0.1, 0.1, 0, 0, 0.3, 0.22, 0.17],
        'prop_business': [0, 0.3, 1, 0, 0.02, 0.11, 0.3],
        'prop_health_med': [0.33, 0, 0, 1, 0.03, 0.03, 0],
        'prop_interdiscip': [0.15, 0.1, 0, 0, 0.05, 0.05, 0],
        'prop_public_svce': [0.12, 0, 0, 0, 0, 0.03, 0],
        'prop_sci_math_tech': [0.05, 0.4, 0, 0, 0.37, 0.47, 0.48],
        'prop_social_sci': [0.24, 0.1, 0, 0, 0.23, 0.04, 0.05],
        'prop_trades_personal_svce': [0.01, 0, 0, 0, 0, 0.01, 0]
    }   
    df_testing = pd.DataFrame(data=df_inputs)
    # cluster info (testing both with SAT scores and no SAT scores)
    SAT_score_0 = [420, 550]
    SAT_score_1 = [0, 0] # no SAT
    desired_majors = [2, 3, 1, 4, 5, 6, 7, 8]
    clustering_info_testing_0 = [SAT_score_0, desired_majors]
    clustering_info_testing_1 = [SAT_score_1, desired_majors]

    # actual output
    actual_0 = mod.modeling(df_testing, clustering_info_testing_0)
    actual_1 = mod.modeling(df_testing, clustering_info_testing_1)

    # expected output
    col = ['INSTNM', 'CITY', 'state', 'ADM_RATE', 'SATVRMID', 'SATMTMID', 'num_undergrad', 'prop_arts_human', 'prop_business', 'prop_health_med', 'prop_interdiscip',
                    'prop_public_svce', 'prop_sci_math_tech', 'prop_social_sci', 'prop_trades_personal_svce']
    idx_0 = [6]
    expected_0 = pd.DataFrame([['Quasi', 'Chicago', 'IL', 0.603, 410.0, 450.0, 8828, 0.17, 0.3, 0.0, 0.0, 0.0, 0.48, 0.05, 0.0]], index=idx_0, columns=col)
    idx_1 = [0, 3]
    expected_1 = pd.DataFrame([['Academy', 'Chicago', 'IL', 0.335, 570.0, 583.0, 3201, 0.1, 0.0, 0.33, 0.15, 0.12, 0.05, 0.24, 0.01],
                               ['Random', 'Houston', 'TX', 0.885, np.nan, np.nan, 7555, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]], index=idx_1, columns=col)

    # check type and expected output
    try:
        assert isinstance(expected_0, pd.DataFrame)
        assert actual_0.equals(expected_0)
        print ('Test for modeling function (with SAT scores) passed!')
    except:
        print ('Test for modeling function (with SAT scores) FAILED!')
    print ('---------------------')

    try:
        assert isinstance(expected_1, pd.DataFrame)
        assert actual_1.equals(expected_1)
        print ('Test for modeling function (without SAT scores) passed!') 
    except:
        print ('Test for modeling function (without SAT scores) FAILED!')
    print ('-----------------------------------------------------------')
    print('')

def test_major_pref_transformation():
    """Testing major_pref_transformation function."""

    # initialize an array for test
    array_testing = [3, 2, 1, 5, 6, 4, 7, 8]

    # actual output
    actual = mod.major_pref_transformation(array_testing)

    # expected output
    expected = [1/6, 1/3, 1/2, 0, 0, 0, 0, 0]

    try:
        # check type
        assert isinstance(expected, list)
        # check expected output
        assert actual == expected
        print ('Test for major_pref_transformation function passed!')
    except:
        print ('Test for major_pref_transformation function FAILED!')
    print ('-----------------------------------------------------------')
    print ('')          

def main():
    """Main function"""

    # Unit testing (all good)
    test_filter()
    test_modeling()
    test_major_pref_transformation()
    

if __name__== "__main__":
    main()