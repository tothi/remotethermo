#!/usr/bin/env python3
#
# Ariston Remote Thermo API alpha
#

import requests

class RemoteThermo:
    URI = "https://www.ariston-net.remotethermo.com"
    def __init__(self, email, password):
        self.s = requests.Session()
        self.login(email, password)

    def __del__(self):
        self.logout()
        del self.s
        
    def login(self, email, password):
        r = self.s.post(self.URI+"/Account/Login",
                        data={"Email": email, "Password": password})
        assert r.url.startswith(self.URI+"/PlantDashboard/Index/")
        self.plant_id = r.url.split("/")[5]

    def logout(self):
        r = self.s.get(self.URI+"/Account/Logout")
        assert r.url == self.URI+"/Account/Login"
        
    def getPlantData(self):
        r = self.s.get(self.URI+"/PlantDashboard/GetPlantData/"+self.plant_id)
        self.plant_data = r.json()
        return self.plant_data

if __name__ == "__main__":
    EMAIL = "test@test.com"
    PASSWORD = "password_for_test@test.com"

    print("[*] logging in...")
    gw = RemoteThermo(EMAIL, PASSWORD)
    print("[+] plant id is %s" % gw.plant_id)

    print("[*] getting PlantData:")
    gw.getPlantData()
    #print(gw.plant_data)
    print("[+] outside temperature is %s" % gw.plant_data['outsideTemp'])
    print("[+] room temperature is %s" % gw.plant_data['zone']['roomTemp'])
    
    del gw
    print("[+] logged out.")
