# Disaster Response Pipeline Project
Disaster events often bring chaos, but effective communication can be a lifeline. By building a machine learning pipeline, creating an API capable of categorizing these messages, ensuring they reach the appropriate relief agencies promptly.
In a world increasingly affected by natural and man-made disasters, this project isn't just valuable—it's essential. By mapping data science concept with real-world impact, we are not only advancing our skills but also contributing to the greater good. 

### Dependencies
    Name                    Version                  
    flask                     2.2.5             
    joblib                    1.4.0             
    nltk                      3.8.1             
    numpy                     1.26.4            
    numpy-base                1.26.4            
    pandas                    2.2.1             
    pip                       23.3.1            
    plotly                    5.19.0            
    python                    3.11.7                 
    pytz                      2024.1            
    readline                  8.2                    
    regex                     2023.10.3         
    scikit-learn              1.4.2             
    sqlalchemy                2.0.25            
    sqlite                    3.45.3                 
    tk                        8.6.12                  
    xgboost                   2.0.3             

### Code Structure
    - app
    | - template
    | |- master.html  # main page of web app
    | |- go.html  # classification result page of web app
    |- run.py  # Flask file that runs app

    - data
    |- disaster_categories.csv  # data to process 
    |- disaster_messages.csv  # data to process
    |- process_data.py
    |- DisasterResponse.db   # database to save clean data to

    - models
    |- train_classifier.py
    |- classifier.pkl  # saved model 

    - README.md

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

### Video Demo on my linkedin blog's post: https://www.linkedin.com/feed/update/urn:li:activity:7193287060659585024/

### Evaluation Report
![ScreenShot](evaluation_report.png)
