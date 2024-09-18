import requests,json
from pymongo.mongo_client import MongoClient

#MongoAtlas

class emailChecker:

    def __init__(self):
        self.listEmails = []
        self.listEmailsPhishing = []

    def requestDataFromApi(self):
        responseAPIEmails = requests.get("https://www.datos.gov.co/resource/jtnk-dmga.json")
        dataJson = responseAPIEmails.json()
        for email in range(len(dataJson)):
            self.listEmails.append(dataJson[email]["email_address"])

    def validateEmail(self):
        for email in self.listEmails:
            responseEmail = requests.get(f"https://mailscrap.com/api/verifier-lookup/{email}")
            dataEmailsJson = responseEmail.json()
            if dataEmailsJson["deliverable"] == "true":
                self.listEmailsPhishing.append(email)
            else:
                pass





prueba = emailChecker()
prueba.requestDataFromApi()
prueba.validateEmail()
print(prueba.listEmailsPhishing)