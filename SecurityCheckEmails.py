import requests

class techChecker:

    def __init__(self):
        self.emailsList = []
        pass

    #Consultar data de datosabiertos
    def queryData(self):
        responseData = requests.get("https://www.datos.gov.co/resource/jtnk-dmga.json")
        for ind in range(len(responseData.json())):
            self.emailsList.append(responseData.json()[ind]['email_address'])

    def validateReputation(self):
        for email in self.emailsList:
            responseValidation = requests.get(f"https://mailscrap.com/api/verifier-lookup/{email}")

    def prepareAndSaveData(self):
        pass

prueba = techChecker()
prueba.queryData()
print(prueba.emailsList)

