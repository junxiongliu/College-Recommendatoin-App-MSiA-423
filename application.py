from flask import Flask, flash, redirect, render_template, request, session, abort
import sys
import os
from app import application, db
from app.db_models import college

sys.path.insert(0, 'develop/modeling')
import model as modeling
 
@application.route("/home",methods=['GET','POST'])
def home_page():
	if request.method == 'GET':
		return render_template('layout_homepage.html')

#	elif request.method == 'POST':
#		return render_template('layout_homepage.html') 

@application.route("/recommendation",methods=['GET','POST'])
def recommendation_page():
	# get the usesr input
	p_region = list(map(int, request.form.getlist('pr')))
	p_degree = list(map(int, request.form.getlist('pd')))
	p_schooltype = list(map(int, request.form.getlist('pst')))
	p_schoolsize = list(map(int, request.form.getlist('psz')))
	SAT = list(map(int, request.form.getlist('SAT')))
	p_major = list(map(int, request.form.getlist('pmajor')))
	strict_criteria = [p_region, p_degree, p_schoolsize, p_schooltype]
	clustering_info = [SAT, p_major]

	# now do the recommendation model
	# old method without rds
	# path = 'develop/data/data_2013.csv' #select * from db
	# df = modeling.read(path)

	# new method with rds
	statement = 'SELECT * FROM college'
	host='msiawebapp.cg96n7rbldvk.us-east-1.rds.amazonaws.com'
	dbname='msiawebappdb'
	port=5432
	user='collegeconnect'
	password='collegeahead'
	connection = [host,dbname,port,user,password]
	df = modeling.read_sql(statement,connection)
	df_filtered = modeling.filter(df,strict_criteria)
	result = modeling.modeling(df_filtered,clustering_info)

	# BELOW are code specific for output
	# insert an empty column just for output
	num_rows = len(result.index)
	inserted_vals = ['']*num_rows
	result.insert(loc=7, column='Proportion of majors',value=inserted_vals)

	# rename
	output_rename = {'INSTNM': 'Name', 'CITY': 'City', 'state': 'State', 'ADM_RATE': 'Admission rate', 'SATVRMID': 'Median SAT Verbal', 
	'SATMTMID': 'Median SAT Math', 'num_undergrad': 'Number of undergraduates', 'prop_arts_human': 'Arts and Humanities', 'prop_business': 'Business',
	'prop_health_med': 'Health and Medicine', 'prop_interdiscip': 'Multi-/Interdisciplinary Studies', 'prop_public_svce': 'Public and Social Services', 'prop_sci_math_tech': 'Science, Math, and Technology',
	'prop_social_sci': 'Social Sciences', 'prop_trades_personal_svce': 'Trades and Personal Services'}
	result_output = result.rename(index=str, columns=output_rename)

	# fill na with '' and format numbers in [0,1] to %
	names_to_format = ['Admission rate', 'Arts and Humanities', 'Business', 'Health and Medicine', 'Multi-/Interdisciplinary Studies', 'Public and Social Services', 'Science, Math, and Technology', 'Social Sciences', 'Trades and Personal Services']
	for name in names_to_format:
		result_output[name] = result_output[name].map('{:,.2%}'.format)

	# also fill na with ''
	result_output = result_output.fillna('N/A')
	result_output['Admission rate'] = result_output['Admission rate'].str.replace('nan%', 'N/A')

	# transpose to output
	result_output = result_output.set_index('Name').T

	if request.method == 'POST':
		return render_template('layout_predictionpage.html',data=result_output.to_html())

	# if request.method == 'GET':
	# 	print ("hi")
	# return render_template('layout_predictionpage.html',**locals())

if __name__ == "__main__":
	application.run(host = '0.0.0.0', use_reloader=True, debug=True)
