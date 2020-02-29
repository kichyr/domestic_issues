import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'domesticissuesmiptbot-5f079ab8d247.json'  # имя файла с закрытым ключом

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
p = str(input("Таблица, в которую вы хотите собирать данные введите spreadsheetId или 0"))
if p == '0':
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'DomesticIssues', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Сводка',
                                   'gridProperties': {'rowCount': 8, 'columnCount': 5}}}]
    }).execute()

    driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
    shareRes = driveService.permissions().create(
        fileId=spreadsheet['spreadsheetId'],
        body={'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
        fields='id'
    ).execute()
else:
    # ranges = []
    # include_grid_data = False
    spreadsheet = service.spreadsheets().get(spreadsheetId=p).execute()

results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet['spreadsheetId'], body={
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "Сводка!B2:C3",
         "majorDimension": "ROWS",
         # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
         "values": [["This is B2", "This is C2"], ["This is B3", "This is C3"]]},

        {"range": "Сводка!D5:E6",
         "majorDimension": "COLUMNS",
         # сначала заполнять столбцы, затем ряды (т.е. самые внутренние списки в values - это столбцы)
         "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
    ]
}).execute()

print(spreadsheet)
