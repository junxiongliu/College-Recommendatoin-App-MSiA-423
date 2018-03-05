"""

This is the database creation file for the college recommendation system. Most likely, you will not need this as the database has been created.

Author: Junxiong Liu

"""

from app import db
from app.db_models import college
import pandas as pd

def create_db():
    """Create the database and table using defined db_models in SQLAlchemy. configuration parameter in __init__.py with the schema defined by models.college()

    Args:
        Null

    Returns:
        Null

    """

    # initialize db
    db.create_all()

    # add information from the existing csv
    path = 'develop/data/data_2013.csv'
    df = pd.read_csv(path,encoding='ISO-8859-1')

    # change to None to add to db
    df = df.where((pd.notnull(df)), None)

	# add to db
    for index,row in df.iterrows():
    	cur_college = college(INSTNM=row['INSTNM'], CITY=row['CITY'], state=row['state'], degree_offered=row['degree_offered'],CONTROL=row['CONTROL'],region=row['region'],
    		ADM_RATE=row['ADM_RATE'], SATVRMID=row['SATVRMID'], SATMTMID=row['SATMTMID'], num_undergrad=row['num_undergrad'], prop_arts_human=row['prop_arts_human'],prop_business=row['prop_business'],
    		prop_health_med=row['prop_health_med'], prop_interdiscip=row['prop_interdiscip'], prop_public_svce=row['prop_public_svce'], prop_sci_math_tech=row['prop_sci_math_tech'], prop_social_sci=row['prop_social_sci'], prop_trades_personal_svce=row['prop_trades_personal_svce'])
    	db.session.add(cur_college)
    
    # commit
    db.session.commit()

if __name__ == "__main__":
	create_db()
