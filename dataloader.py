import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import gspread2df as g2d

def create_keyfile_dict():
    return {
        "type": os.environ.get("SHEET_TYPE"),
        "project_id": os.environ.get("SHEET_PROJECT_ID"),
        "private_key_id": os.environ.get("SHEET_PRIVATE_KEY_ID"),
        "private_key": "\n".join(os.environ.get("SHEET_PRIVATE_KEY").split("\\n")),
        "client_email": os.environ.get("SHEET_CLIENT_EMAIL"),
        "client_id": os.environ.get("SHEET_CLIENT_ID"),
        "auth_uri": os.environ.get("SHEET_AUTH_URI"),
        "token_uri": os.environ.get("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.environ.get("SHEET_CLIENT_X509_CERT_URL")
    }

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    create_keyfile_dict(), scopes=scope)
gc = gspread.authorize(credentials)


def stats():
    # statistics for yesterday
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    ref_dict, fact_dict = {}, {}
    for idx, wks_name in enumerate(["card", "activation", "topup", "purchase"]):
        df = g2d.download("1pp01qoxMGsS7oCIwf83eOI0W_Wo6vYhhlBcXlmcGKL8",
                          wks_name=wks_name,
                          col_names=True,
                          row_names=False,
                          credentials=credentials)
        ref_dict[wks_name] = int(df[df["date"] == yesterday].iloc[:, 1].values[0])
        df = g2d.download("19Lt8Bf0xglLDNcEjMBLV08r6UNmvAlRC3Z_tsOV1OUQ",
                          wks_name=wks_name,
                          col_names=False,
                          row_names=False,
                          credentials=credentials)
        fact_dict[wks_name] = int(df.iloc[0, 0])
        if wks_name == 'card':
            total = int(df.iloc[0, 1])
    text = "Hello, dear colleague! \n\n Statistics for yesterday: \n" + \
    '\n'.join([f" - {'paid ' if key == 'topup' else ''}{key}s: expectation = {ref_dict[key]}, reality = {fact_dict[key]}{f', total for a month = {total}' if key == 'card' else ''}"
               for key in ref_dict.keys()])
    # all time statistics
    df = g2d.download("19Lt8Bf0xglLDNcEjMBLV08r6UNmvAlRC3Z_tsOV1OUQ",
                  wks_name="lifetime",
                  col_names=False,
                  row_names=False,
                  credentials=credentials)
    text += "\n\n Lifetime statistics:"
    for i, name in enumerate(["card holders", "wallets created", "pre-ordered cards", "total customers"]):
        text += f"\n - {name} = {int(df.iloc[0, i]):,}"
    return text