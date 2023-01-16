import os
import gspread
import datetime
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor

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

def gspread_authorize(create_keyfile_dict):
    scopes = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        create_keyfile_dict(), scopes=scopes)
    gspread.authorize(credentials)
    return credentials

def authorize_decorator(stats):
    def wrapper(*kwargs):
        return stats(gspread_authorize(create_keyfile_dict), *kwargs)
    return wrapper

@authorize_decorator
def stats(credentials, button):
    """get statistics for yesterday"""

    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    ref_dict, fact_dict = {}, {}

    def wks_names(button) -> list:
        if button.lower() == 'cards':
            return ["wallet", "wallets (exclude on-demand)", "card", "tokenization"]
        elif button.lower() == 'transactions':
            return ["activation", "topup", "paid topup", "purchase"]
        elif button.lower() == 'verifications':
            return ["kyc", "junior-parent"]

    def get_expectation(wks_name, *kwargs) -> int:
        df = g2d.download("1pp01qoxMGsS7oCIwf83eOI0W_Wo6vYhhlBcXlmcGKL8",
                          wks_name=wks_name,
                          col_names=True,
                          row_names=False,
                          credentials=credentials)
        return str(df[df["date"] == yesterday].iloc[:, 1].values[0])

    def get_reality(wks_name, *kwargs) -> list:
        df = g2d.download("19Lt8Bf0xglLDNcEjMBLV08r6UNmvAlRC3Z_tsOV1OUQ",
                          wks_name=wks_name,
                          col_names=False,
                          row_names=False,
                          credentials=credentials)
        return [str(x) for x in df.values[0]]
    
    # Threading to request concurrently
    with ThreadPoolExecutor(max_workers=8) as pool:
        future_expectation = {}
        future_reality = {}
        for wks_name in wks_names(button):
            try:
                future_expectation[wks_name] = pool.submit(get_expectation, (wks_name))
            except:
                pass
            future_reality[wks_name] = pool.submit(get_reality, (wks_name))
    
    # get results from threads
    ref_dict = {wks_name: task.result() for wks_name, task in future_expectation.items()}
    fact_dict = {wks_name: task.result() for wks_name, task in future_reality.items()}

    text = f"Hello, dear colleague! \n\n Statistics for yesterday by {button}: \n" + \
    '\n'.join([f" - {key}" + \
               f"{'s:' if key != 'wallets (exclude on-demand)' else ':'}" + \
               f"{f' expectation = {ref_dict[key]},' if key in ref_dict.keys() else ''}" + \
               f"{' new potential' if key == 'junior-parent' else ''}" + \
               f"{' new' if key in ['tokenization', 'kyc'] else ''}" + \
               f"{' reality' if key not in ['tokenization','junior-parent','kyc'] else ''}" + \
               f" = {fact_dict[key][0]}" + \
               f"{f', per month = {fact_dict[key][1]}' if key in ['wallet', 'card', 'wallets (exclude on-demand)'] else ''}" + \
               f"{f', total = {fact_dict[key][1]}' if key == 'kyc' else ''}"
               f"{f', total confirmed = {fact_dict[key][1]}' if key == 'junior-parent' else ''}" + \
               f"{f', unique = {fact_dict[key][1]}' if key == 'tokenization' else ''}"
               for key in fact_dict.keys()])
    return text


@authorize_decorator
def lifetime(credentials):
    """get statistics for all the time"""
    df = g2d.download("19Lt8Bf0xglLDNcEjMBLV08r6UNmvAlRC3Z_tsOV1OUQ",
                  wks_name="lifetime",
                  col_names=False,
                  row_names=False,
                  credentials=credentials)
    text = "Hello, dear colleague! \n\n Lifetime statistics:"
    for idx, name in enumerate(["card holders",
                                "cards opened",
                                "wallets holders",
                                "wallets opened",
                                "wallets (include on-demand)",
                                "pre-ordered cards",
                                "total customers"]):
        text += f"\n - {name} = {int(df.iloc[0, idx]):,}"
    return text