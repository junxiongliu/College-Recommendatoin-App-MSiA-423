# College Recommendation Flask App

## Objective 
This repo can be used to produce a U.S. college recommendation web app. The app is written with Python 3.

## Data
The data is downloaded from [Kaggle](https://www.kaggle.com/jpico6/predicting-college-graduation/data). The cleaned format is stored in `develop/data/data_2013.csv`.

## Pivotal Tracker
[Link to Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2144165)

## Package requirements
* [conda](https://anaconda.org/): Either Anaconda or Miniconda is fine for this project.
* [git](https://git-scm.com/): You will most likely need version control.

## Steps to set up
Below is a brief tutorial to set up the conda environment in a AWS EC2 or Linux. For other systems, the general steps are same, but small changes might be needed. 

1. Update. Install git and conda if you have not done so.

    `sudo yum update`

    `sudo yum install git`

    `wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
    bash Anaconda3-5.1.0-Linux-x86_64.sh`

2. Clone this GitHub repository to local.

3. Go into the directory, and use the `collegeapp.yml` file to create a conda environment with all required packages and dependecies.

    `conda env create -f collegeapp.yml`

4. In the same directory as `collegeapp.yml`, create a file called `config` and paste the following information into the file to configure your database.

    `SECRET_KEY = 'development_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://collegeconnect:collegeahead@msiawebapp.cg96n7rbldvk.us-east-1.rds.amazonaws.com:5432/msiawebappdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True`

5. `app/__init__.py` should have included the line of code: 

    `application.config.from_envvar('APP_SETTINGS', silent=True)`
    
    which tells the application to look at the environmental variable `APP_SETTINGS` for the path to your config file. 
    This means you need to set this environmental variable yourself by going to command line and entering:
    
    `export MSIA_SETTINGS="path/to/where/your/config/file/is.config`

6. The database should have been initialized, so you may skip this step and go to next step. If it is the case that the database has not been initialized, use `python create_collegedb.py` to initialize.

7. Now run the application by typing `python application.py`. The webapp should be running on `http://ec2-52-91-59-235.compute-1.amazonaws.com:5000/home`. Have fun!

## Logging
There are two sets of logging performed. 

1. `application.log` stores the logs of any user interaction with the EC2 application.

2. `createdb.log` stores the logs of database initialization.

## Unit Testing
We performed unit testing for the `develop/modeling/model.py` file. The `model.py` functions we tested are
* `filter()`
* `modeling()`
* `major_pref_transformation()`