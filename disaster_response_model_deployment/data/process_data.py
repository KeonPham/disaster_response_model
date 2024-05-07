import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Load data from two CSV files containing messages and categories, merge them on the 'id' column,
    and return a DataFrame.

    Parameters:
    messages_filepath (str): The file path to the CSV file containing messages.
    categories_filepath (str): The file path to the CSV file containing categories.

    Returns:
    pandas.DataFrame: Merged DataFrame containing messages and their corresponding categories.
    """
    messages =  pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, on = 'id')
    return df

def clean_data(df):
    """
    Cleans the DataFrame by splitting categories into separate category columns and converting category values to binary (0 or 1).

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the raw data with a 'categories' column.

    Returns:
    pandas.DataFrame: The cleaned DataFrame with separate category columns and binary category values.

    Steps:
    1. Split the 'categories' column into separate category columns.
    2. Extract category column names and apply them to the new DataFrame.
    3. Convert category values to binary (0 or 1).
    4. Drop the original 'categories' column.
    5. Combine the cleaned DataFrame with the new category columns.
    6. Drop the 'child_alone' column as it contains only zeros.
    7. Modify 'related' column values: 2s are replaced with 1s to make it binary.
    8. Drop duplicate rows.
    """
    #Step 1
    categories = df['categories'].str.split(pat=';',expand=True)

    #Step 2
    row = categories.iloc[0]
    category_colnames = row.apply(lambda s:s[:-2])
    categories.columns = category_colnames

    #Step 3
    for column in categories:
        categories[column] = categories[column].apply(lambda s:s[-1])
        categories[column] = categories[column].astype(int)

    #Step 4
    df = df.drop(['categories'],axis = 1)

    #Step 5
    df = pd.concat([df,categories],axis = 1)

    #Step 6
    df = df.drop('child_alone',axis = 1)
    
    #Step 7
    df['related'] = df['related'].apply(lambda x: 1 if x==2 else x) 

    #Step 8
    df = df.drop_duplicates()

    return df

def save_data(df, database_filepath):
    """
    Save the DataFrame to a SQLite database.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be saved.
    database_filepath (str): The file path for the SQLite database.

    Returns:
    None

    Steps:
    1. Create a SQLAlchemy Engine object with the specified database filepath.
    2. Save the DataFrame to the specified database with the table name 'DisasterResponse'.
    """
    engine = create_engine('sqlite:///'+database_filepath)
    df.to_sql('DisasterResponse', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()