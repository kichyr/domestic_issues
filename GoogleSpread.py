import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'domesticissuesmiptbot-5f079ab8d247.json'  # имя файла с закрытым ключом


class Spreadsheet:
    def __init__(self, jsonKeyFileName):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonKeyFileName, [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.driveService = None  # Needed only for sharing
        self.spreadsheetId = None
        self.sheetId = None
        self.sheetTitle = []
        self.requests = []
        self.valueRanges = []

    # Creates new spreadsheet
    def create(self, title="Бытовые проблемы", sheetTitle = ["Сводка"], rows=1000, cols=7, locale='ru_RU',
               timeZone='Etc/GMT'):
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': title, 'locale': locale, 'timeZone': timeZone},
            'sheets': [{'properties': {'sheetType': 'GRID', 'sheetId': 0, 'title': sheetTitle[0],
                                       'gridProperties': {'rowCount': rows, 'columnCount': cols}}}]
        }).execute()
        self.spreadsheetId = spreadsheet['spreadsheetId']
        self.sheetId = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheetTitle= spreadsheet['sheets'][0]['properties']['title']

    def share(self, shareRequestBody):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()
        if self.driveService is None:
            self.driveService = apiclient.discovery.build('drive', 'v3', http=self.httpAuth)
        shareRes = self.driveService.permissions().create(
            fileId=self.spreadsheetId,
            body=shareRequestBody,
            fields='id'
        ).execute()



    def shareWithEmailForReading(self, email):
        self.share({'type': 'user', 'role': 'reader', 'emailAddress': email})

    def shareWithEmailForWriting(self, email):
        self.share({'type': 'user', 'role': 'writer', 'emailAddress': email})

    def shareWithAnybodyForReading(self):
        self.share({'type': 'anyone', 'role': 'reader'})

    def shareWithAnybodyForWriting(self):
        self.share({'type': 'anyone', 'role': 'writer'})

    def getSheetURL(self):
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheetId + '/edit#gid=' + str(self.sheetId)

    def setSpreadsheetById(self, spreadsheetId):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
        self.spreadsheetId = spreadsheet['spreadsheetId']
        self.sheetId = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheetTitle = spreadsheet['sheets']['properties']['title']

    def prepare_setDimensionPixelSize(self, dimension, startIndex, endIndex, pixelSize):
        self.requests.append({"updateDimensionProperties": {
            "range": {"sheetId": self.sheetId,
                      "dimension": dimension,
                      "startIndex": startIndex,
                      "endIndex": endIndex},
            "properties": {"pixelSize": pixelSize},
            "fields": "pixelSize"}})

    def prepare_setColumnsWidth(self, startCol, endCol, width):
        self.prepare_setDimensionPixelSize("COLUMNS", startCol, endCol + 1, width)

    def prepare_setColumnWidth(self, col, width):
        self.prepare_setColumnsWidth(col, col, width)

    def prepare_setValues(self, st, cellsRange, values, majorDimension="ROWS"):
        self.valueRanges.append(
            {"range": st + "!" + cellsRange, "majorDimension": majorDimension, "values": values})

        # spreadsheets.batchUpdate and spreadsheets.values.batchUpdate

    def runPrepared(self, valueInputOption="USER_ENTERED"):
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1Res = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                  body={"requests": self.requests}).execute()
            if len(self.valueRanges) > 0:
                upd2Res = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                           body={
                                                                               "valueInputOption": valueInputOption,
                                                                               "data": self.valueRanges}).execute()
        finally:
            self.requests = []
            self.valueRanges = []
        return (upd1Res['replies'], upd2Res['responses'])

    def prepare_addSheet(self, st, rows=1000, cols=7):
        self.requests.append({"addSheet": {
            "properties": {"title": st, 'gridProperties': {'rowCount': rows, 'columnCount': cols}}}})

    # Adds new sheet to current spreadsheet, sets as current sheet and returns it's id
    def addSheet(self, st, rows=1000, cols=7):
        self.prepare_addSheet(st, rows, cols)
        addedSheet = self.runPrepared()[0][0]['addSheet']['properties']
        self.sheetId = addedSheet['sheetId']
        self.sheetTitle = addedSheet['title']
        return self.sheetId


ss = Spreadsheet(CREDENTIALS_FILE)
p = str(input("Таблица, в которую вы хотите собирать данные введите spreadsheetId или 0"))

if p == '0':
    ss.create()
    ss.prepare_setValues("Сводка","A1:G1", [["Login", "Почта", "Здание", "Специфика", "Проблема", "Комментарии", "Выполнено"]])
    ss.prepare_setColumnWidth(4, 500)
    places = ['№1', '№2', "№3", "№4", "Зюзино", "№6", "№7", "№8", "№9", "№10", "№11", "№12", "ФАЛТ МФТИ", 'НК', 'ГК',
              "ЛК", "АК", "Физтех-Био", "Радиокорпус", "Цифра", "Арктика", "КПМ", "СK №1", "СK №2", "СK Бассейн", "КСП"]
    for place in places:
        ss.prepare_addSheet(place)
        ss.prepare_setValues(place, "A1:G1",
                             [["Login", "Почта", "Здание", "Специфика", "Проблема", "Комментарии", "Выполнено"]])
else:
    ss.setSpreadsheetById(p)

ss.shareWithAnybodyForReading()
ss.shareWithEmailForWriting('kichyr13@gmail.com')


ss.runPrepared()

print(ss.getSheetURL())
