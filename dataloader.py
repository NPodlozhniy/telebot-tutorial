import sqlalchemy
from sqlalchemy.dialects.mssql import pymssql
import os

import datetime
import urllib.parse

import numpy as np
import pandas as pd

HOSTNAME = "sql-live.i.zelf.bot"
USERNAME = 'n.podlozhniy@zelf.co'
PASSWORD = urllib.parse.quote_plus(os.environ['PASSWORD'])

engine = sqlalchemy.create_engine(f'mssql+pymssql://{USERNAME}:{PASSWORD}@{HOSTNAME}')

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import gspread2df as g2d

KEYFILE = os.environ['KEYFILE']

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scopes=scope)
gc = gspread.authorize(credentials)
spreadsheet_key = "1pp01qoxMGsS7oCIwf83eOI0W_Wo6vYhhlBcXlmcGKL8"

selects = ["""
    select count(CustomerID) as value
    from
            card.dbo.Wallet wt
    where 1 = 1
        and convert(date, CreateDate) = dateadd(day, -1, convert(date, getdate()))
        and wt.WalletTypeID = 9
        and wt.IsHold = 0
    group by convert(date, CreateDate)
    ;""",
    """
    select count(CustomerID) as value
    from (
        select se.CustomerID
            ,convert(date, min(TransactionDate)) as first_transaction_dt
        from
                card.dbo.Wallet wt
        left join
                statement.dbo.StatementEntry as se
            on wt.CustomerID = se.CustomerID
        where 1 = 1
            and wt.IsHold = 0
            and wt.WalletTypeID = 9
            and se.StateID in (0, 1)
            and se.TransactionAmount > 0
         group by se.CustomerID
         having convert(date, min(TransactionDate)) = dateadd(day, -1, convert(date, getdate()))
     ) temp
    ;""",
    """
    select count(*) as value
    from
            statement.dbo.StatementEntry as se
    inner join
            statement.dbo.Payin pi
        on se.ExternalTransactionID = pi.ExternalPayinID
    where 1 = 1
        and convert(date, se.TransactionDate) = dateadd(day, -1, convert(date, getdate()))
        and se.StateID in (0, 1)
        and se.FeeAmount > 0
    group by convert(date, se.TransactionDate)
    ;""",
    """
    select count(AccountAmount) as value
    from
            statement.dbo.StatementEntry
    where 1 = 1
        and StateID in (0, 1)
        and Direction = -1
        and TypeID = 3
        and TransactionAmount > 0
        and convert(date, TransactionDate) = dateadd(day, -1, convert(date, getdate()))
    group by convert(date, TransactionDate)
    ;"""]

def stats():    
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    ref_dict, fact_dict = {}, {}
    for idx, wks_name in enumerate(["card", "activation", "topup", "purchase"]):
        df = g2d.download(spreadsheet_key,
                          wks_name=wks_name,
                          col_names=True,
                          row_names=False,
                          credentials=credentials)
        ref_dict[wks_name] = int(df[df["date"] == yesterday].iloc[:, 1].values[0])
        fact_dict[wks_name] = pd.read_sql(selects[idx], engine)["value"][0]
    text = "Hello, dear colleague! \n Statistics for yesterday: \n" + \
    '\n'.join([f" -> {key}s: expectation = {ref_dict[key]}, reality = {fact_dict[key]}"
               for key in ref_dict.keys()])
    return text