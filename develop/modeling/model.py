"""

This is the main modeling file for the college recommendation system.

Author: Junxiong Liu

"""

import pandas as pd
import numpy as np
import copy
import random
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import sqlalchemy

def read(path):
    """Read data (csv format)

    Args:
        param1 (str): data path

    Returns:
        df: the readed dataframe
        
    """

    df = pd.read_csv(path,encoding='ISO-8859-1')
    return df

def read_sql(query,uri):
    """Read data (db returned format, array of string of arrays)

    Args:
        param1 (string): sql statement
        param2 (string): uri containing connection details passed from application.py

    Returns:
        df: the corresponding dataframe

    """

    engine = sqlalchemy.engine.create_engine(uri)
    connection = engine.connect()
    df = pd.read_sql(query, con=connection)

    return df

def filter(df,strict_criteria):
    """Criteria for initial filtering based on user input

    Args:
        param1 (array[4]): Criteria for initial filtering; input of array of length 4: [preferred region,preferred degree, preferred school type, preferred school size range]

    Returns:
        df: the filtered dataframe

    """

    filtered_df = df[(df['region'].isin(strict_criteria[0])) & (df['degree_offered'].isin(strict_criteria[1])) &
                    (df['num_undergrad'] > strict_criteria[2][0]) & (df['num_undergrad'] < strict_criteria[2][1]) & 
                    (df['CONTROL'].isin(strict_criteria[3]))]
    return filtered_df


def modeling(df,clustering_info):
    """Function for clustering

    Args:
        param1 (array[2]): Criteria for clustering input of array of length 2: [SAT scores, preferrd majors]

    Returns:
        array[5]: five recommended colleges to apply to

    """

    output_cols = ['INSTNM','CITY','state','ADM_RATE','SATVRMID','SATMTMID','num_undergrad','prop_arts_human','prop_business','prop_health_med','prop_interdiscip',
                    'prop_public_svce','prop_sci_math_tech','prop_social_sci','prop_trades_personal_svce']
    
    # fit a model (just 12 clusters)
    num_clusters = 12
    km = KMeans(n_clusters = num_clusters,random_state=666)

    if clustering_info[0][0] != 0 and clustering_info[0][1] != 0: # have SAT scores
        cols = ['SATVRMID','SATMTMID','prop_arts_human','prop_business','prop_health_med','prop_interdiscip',
                    'prop_public_svce','prop_sci_math_tech','prop_social_sci','prop_trades_personal_svce']
        # filter out na
        df_SAT = df.dropna(subset = cols,axis=0)
        df_SAT_modeling = df_SAT[cols]
        
        # scale (standardize)
        scaler = StandardScaler()
        df_SAT_modeling_scaled = pd.DataFrame(scaler.fit_transform(df_SAT_modeling[cols]))
        df_SAT_modeling_scaled.iloc[:, 0] = df_SAT_modeling_scaled.iloc[:, 0].apply(lambda x: x*6) # put more weight on SAT scores
        df_SAT_modeling_scaled.iloc[:, 1] = df_SAT_modeling_scaled.iloc[:, 1].apply(lambda x: x*6)
        
        # prediction on raw
        km.fit(df_SAT_modeling_scaled)
        prediction=km.predict(df_SAT_modeling_scaled)
        df_SAT = df_SAT.assign(predicted_cluster=prediction)
        
        # transform the desired major list of new observation to between 0 and 1
        major_list = major_pref_transformation(clustering_info[1])

        # predict the new observation
        new_obs = copy.deepcopy(clustering_info[0])
        new_obs.extend(major_list)
        
        # append to the original and standardize
        df_SAT_modeling_appended = df_SAT_modeling.append(pd.Series(new_obs, index=df_SAT_modeling.columns, name='e'))
        new_scaled = pd.DataFrame(scaler.fit_transform(df_SAT_modeling_appended[cols]))
        new_scaled.iloc[:, 0] = new_scaled.iloc[:, 0].apply(lambda x: x*6) # put more weight on SAT scores
        new_scaled.iloc[:, 1] = new_scaled.iloc[:, 1].apply(lambda x: x*6)
        
        # get the prediction
        new_obs_scaled = new_scaled.tail(1)
        new_obs_prediction = km.predict(pd.DataFrame(new_obs_scaled))[0]
        
        # get the centroid distance to predicted cluster
        # get the distance of new observation to each observation in cluster
        df_SAT_modeling_scaled_appended = df_SAT_modeling_scaled.append(new_obs_scaled)
        d_all = km.transform(df_SAT_modeling_scaled_appended)[:, new_obs_prediction]
        d_new = d_all[-1]
        d = np.delete(d_all,-1)
        
        df_SAT = df_SAT.assign(centroid_dist=d,dist_to_obs=abs(d_new-d))
        
        # get the schools
        output_cols.append('dist_to_obs')
        df_SAT_schools = df_SAT[df_SAT.predicted_cluster == new_obs_prediction][output_cols]
        # sort by distance to centroid and output
        if len(df_SAT_schools.index) <= 5:
            df_SAT_output = df_SAT_schools
        else:
            df_SAT_output = df_SAT_schools.sort_values(by='dist_to_obs').head(5)
        
        df_SAT_output = df_SAT_output.drop('dist_to_obs', 1)
        df_SAT_output.rename_axis(None)
        return df_SAT_output
        
    else: # no SAT scores
        cols = ['prop_arts_human','prop_business','prop_health_med','prop_interdiscip',
                    'prop_public_svce','prop_sci_math_tech','prop_social_sci','prop_trades_personal_svce']
        # filter out na
        df_no_SAT = df.dropna(subset = cols,axis=0)
        df_no_SAT_modeling = df_no_SAT[cols]
        
        # prediction on raw
        km.fit(df_no_SAT_modeling)
        prediction=km.predict(df_no_SAT_modeling)
        df_no_SAT = df_no_SAT.assign(predicted_cluster=prediction)
        
        # predict the new observation
        new_obs = major_pref_transformation(clustering_info[1])
        new_obs_prediction = km.predict(pd.DataFrame([new_obs]))[0]
        
        # get the schools
        df_no_SAT_output = df_no_SAT[df_no_SAT.predicted_cluster == new_obs_prediction][output_cols]
        df_no_SAT_output.rename_axis(None)
        return df_no_SAT_output.head(5)

def major_pref_transformation(input_array):
    """A helper function of modeling function to transform the major preference array
    
    Args:
        param1 (array[8]): User input (1-8) of rank

    Returns:
        array[8]: probabilities assigned to user input

    """ 

    # initialize output and weights
    output_array =[]
    weight_1 = 1/2
    weight_2 = 1/3
    weight_3 = 1/6

    for index in range(0,len(input_array)):
        if input_array[index] == 1:
            output_array.append(weight_1)
        elif input_array[index] == 2:
            output_array.append(weight_2)
        elif input_array[index] == 3:
            output_array.append(weight_3)
        else:
            output_array.append(0)

    return output_array

def main():
    """Main Function (not going to be directly called when deployed)

    """

    path = ('../data/data_2013.csv')
    df = read(path)
    
    region_pref = [1,2,3,4,5,6,7,8,9]
    pred_degree = [1,2,3]
    size_range = [1,100000]# school size
    school_type = [1,2]
    strict_criteria = [region_pref,pred_degree,size_range,school_type] # user-input "strict" criteria
    df_filtered = filter(df,strict_criteria)
    
    SAT_score = [750,750] # verbal, math
    # SAT_score = []
    desired_majors = [1,3,2,4,5,6,7,8] # (1/2,1/3,1/6)
    clustering_info = [SAT_score, desired_majors] # user-input "clustering" info
    
    output = modeling(df_filtered,clustering_info)
    print (output)

if __name__== "__main__":
    main()

