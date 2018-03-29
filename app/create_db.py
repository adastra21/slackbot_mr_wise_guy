from __future__ import print_function
import httplib2
import os
import json

from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd
import gspread
from sqlalchemy import create_engine
import psycopg2

# env vars
FILENAME = os.environ["FILENAME"]
SCOPE = os.environ["SCOPE"]
SHEET_ID_1 = os.environ["SHEET_ID_1"]
SHEET_ID_2 = os.environ["SHEET_ID_2"]
DATABASE_URL = os.environ["DATABASE_URL"]


def get_connected_to_api():
    """
    Use service account for authenticating and authorizing access
    to Google Sheets API
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(FILENAME), SCOPE)
    gc = gspread.authorize(credentials)
    return gc


def clean_main_data(gc):
    """
    Clean main sheet data and convert it into a df
    """
    sheet = gc.open_by_key(SHEET_ID_1)
    worksheet = sheet.get_worksheet(0)
    sheet_data = worksheet.get_all_values()

    # remove spaces from col names
    col_names = []
    for name in sheet_data[0]:
        name = name.replace(' ','')
        name = name.lower()
        col_names.append(name)

    df_main = pd.DataFrame.from_records(sheet_data[1:], columns=col_names)
    df_main = df_main[['name', 'email', 'phone', 'committee', 'committeerole', 'dayjob']]

    # lowercase everything
    df = df_main.apply(lambda x: x.str.lower())

    # split name into two cols
    df['firstname'], df['lastname'] = df['name'].str.split(' ', n=1).str

    # get company from dayjob
    df['dayjob'] = df['dayjob'].str.replace('(\sat\s|-)', ', ')
    df[['dayjob', 'company']] = df['dayjob'].str.rsplit(', ', expand=True, n=1)

    # clean dayjob col
    df['dayjob'] = df['dayjob'].map(lambda x: str(x).split('.')[0])
    df['dayjob'] = df['dayjob'].map(lambda x: str(x).split('/')[0])
    df['dayjob'] = df['dayjob'].map(lambda x: str(x).split(',')[0])
    df['dayjob'] = df['dayjob'].map(lambda x: str(x).strip())
    df['company'] = df['company'].map(lambda x: str(x).strip())

    # clean phone nos
    df['phone'] = df['phone'].map(lambda x: str(x).replace('.',''))
    df['phone'] = df['phone'].map(lambda x: str(x).replace('-',''))
    df['phone'] = df['phone'].map(lambda x: x[:3]+"-"+x[3:6]+"-"+x[6:] if len(x) > 0 else x)

    # clear duplicates
    df.drop_duplicates(subset='email', keep='last', inplace=True)

    return df


def clean_add_data(gc):
    """
    Prepare additional data into a df
    """
    sheet = gc.open_by_key(SHEET_ID_2)
    worksheet = sheet.get_worksheet(0)
    sheet_data = worksheet.get_all_values()
    df_addendum = pd.DataFrame.from_records(sheet_data[1:], columns=sheet_data[0])
    return df_addendum


def create_db():
    gc = get_connected_to_api()
    df1 = clean_main_data(gc)
    df2 = clean_add_data(gc)

    # combine datasets
    df = df1.merge(df2[['email','gender','tag']], on='email')
    df.fillna(value="", inplace=True)

    # connect to db
    # db = psycopg2.connect(DATABASE_URL, sslmode='require')
    db = create_engine(DATABASE_URL)
    c = db.connect()
    query_to_clean_db = """
        DROP TABLE IF EXISTS volunteer_info;
    """
    query_to_create_table = """
        CREATE TABLE IF NOT EXISTS volunteer_info (
            email VARCHAR(30) NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            firstname VARCHAR(30) NOT NULL,
            lastname VARCHAR(30) NOT NULL,
            gender VARCHAR(6),
            phone VARCHAR(12),
            committee VARCHAR(12) NOT NULL,
            committeerole VARCHAR(30) NOT NULL,
            dayjob VARCHAR(30) NOT NULL,
            company VARCHAR(30) NOT NULL,
            tag VARCHAR(50)
            );"""

    # c = db.cursor()
    q1 = c.execute(query_to_clean_db)
    q2 = c.execute(query_to_create_table)

    # add df to db
    df.to_sql('volunteer_info', c,
                if_exists='replace',
                index=False)

 # if __name__ == '__main__':
 #    get_sheet_data()