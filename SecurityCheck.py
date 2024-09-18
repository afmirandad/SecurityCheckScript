#Recursos que requiero para funcionar
from configMongo import config
from pymongo.mongo_client import MongoClient
import requests, time

#Parametros de config MongoAtlas
clientConnection = MongoClient(config['URI'])
databaseAccess = clientConnection[config['DATABASE']]
collectionAccess = databaseAccess[config['COLLECTION']]

class IpDataResearch:

    def __init__(self,domain):
        self.domain = domain
        self.ipListByDomain = []
        self.emailsListByDomain = []
        self.regionByIp = {}

    #Metodo para obtener las IP's de un dominio dado
    def getIpFromDomain(self):
        responseIP = requests.get(f"https://networkcalc.com/api/dns/lookup/{self.domain}")
        responseJson = responseIP.json()
        if responseJson["records"] != None:
            for ip in range(len(responseJson["records"]["A"])):
                self.ipListByDomain.append(responseJson["records"]["A"][ip]["address"])

    # Metodo para obtener las región de una IP dada
    def getRegionFromIp(self):
        for ip in self.ipListByDomain:
            responseRegion = requests.get(f"https://ipinfo.io/{ip}?token=f18cd1e491bd68")
            time.sleep(10)
            self.regionByIp[str(ip)] = responseRegion.json()['city']

    #Metodo para obtener correos desde el dominio
    def getEmailsFromDomain(self):
        responseEmail = requests.get(f"https://api.hunter.io/v2/domain-search?domain={self.domain}&api_key=2cc9012e339a13ba2743a17cc7c60bf185684f51")
        time.sleep(10)
        responseEmailJson = responseEmail.json()
        if responseEmailJson['data']['emails'] != None:
            for email in range(len(responseEmailJson['data']['emails'])):
                emailFound = responseEmailJson['data']['emails'][email]["value"]
                self.emailsListByDomain.append(emailFound)

    #Metodo para guardar el JSON en mongo Atlas
    def saveData(self):
        dataFormatTemplate = {
                            "domain":self.domain,
                            "ips":self.regionByIp,
                            "emails":self.emailsListByDomain
                        }
        responseSave = collectionAccess.insert_one(dataFormatTemplate)
        print(responseSave.inserted_id)



prueba = IpDataResearch("paratebueno-cundinamarca.gov.co")
prueba.getIpFromDomain()
prueba.getRegionFromIp()
prueba.getEmailsFromDomain()
prueba.saveData()
