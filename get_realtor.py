#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import time
import json
import requests
import bs4
import belgium_zipcode

class Realtor:
    """ """

    def __init__(self, ipi, name, company_name, street, house_number, postal_code, locality, syndic, mediator):
        """ """
        self.ipi = ipi if ipi is not None else ""
        self.name = name if name is not None else ""
        self.company_name = company_name if company_name is not None else ""
        self.street = street if street is not None else ""
        self.house_number = house_number if house_number is not None else ""
        self.postal_code = postal_code if postal_code is not None else ""
        self.locality = locality if locality is not None else ""
        if "Titulaire" in str(syndic):
            self.syndic = "Titulaire" 
        elif "Stagiaire" in str(syndic):
            self.syndic = "Stagiaire"
        else:        
            self.syndic = "/"
        if "Titulaire" in str(mediator):
            self.mediator = "Titulaire"
        elif "Stagiaire" in str(mediator):
            self.mediator = "Stagiaire" 
        else:
            self.mediator = "/"

    def __str__(self):
        """ """
        preform_str = "[IPI num {}]\n  Complet name\t: {}\n  Company\t: {}\n  Address\t:\n\t\t{} {}\n\t\t{} {}\n  Function\t:\n\t\tsyndic -> {}\n\t\tmediator -> {}\n"
        realtor_str = preform_str.format(self.ipi, self.name, self.company_name, self.street, self.house_number, self.postal_code, self.locality, self.syndic, self.mediator)
        return realtor_str

    def json_encoder(my_realtor):
        """ """
        return json.dumps({
            "ipi": my_realtor.ipi,
            "name": my_realtor.name,
            "company_name": my_realtor.company_name,
            "street": my_realtor.street,
            "house_number": my_realtor.house_number,
            "postal_code": my_realtor.postal_code,
            "locality": my_realtor.locality,
            "syndic": my_realtor.syndic,
            "mediator": my_realtor.mediator 
        }, indent=4, ensure_ascii=False)

    def json_decoder(json_data):
        """ """
        data = json.loads(json_data)
        my_realtor = Realtor(data['ipi'],
                            data['name'],
                            data['company_name'],
                            data['street'],
                            data['house_number'],
                            data['postal_code'],
                            data['locality'],
                            data['syndic'],
                            data['mediator'])
        return my_realtor

    def save(my_realtor, path=None):
        """ """
        data = Realtor.json_encoder(my_realtor)
        file = my_realtor.ipi
        path = path if path is not None else "./data"
        filename = "{}/{}.json".format(path, file)
        with open(filename, 'w') as fd:
            fd.write(data)
        return

def scrapper(preformat_url, zipcode_list, outputdir=None, debug=False):
    max_zipcode = len(zipcode_list)
    for zip_code in zipcode_list:
        if debug is not False:               
            print("current postal code = {}".format(zip_code))
        url = preformat_url.format(zip_code)
        while True:
            try: r = requests.get(url)
            except: sys.exit(1)
            html = r.text
            soup = bs4.BeautifulSoup(html, "lxml")
            raw = soup.find("div", class_="search-results-list").find("div", class_="item-list").find("ol").find_all("li")
            for item in raw:
                subsoup = item.find("div", class_="entity-broker-address-association").find("div", class_="brokeraddress__name")
                ipi = subsoup.find("span", class_="name").a["href"].split("?")[0].split("-")[-1]
                try: name = subsoup.find("span", class_="name").a.string
                except: name = None                
                try: company_name = subsoup.find("span", class_="company-name").a.string
                except: company_name = None
                subsoup = item.find("div", class_="entity-broker-address-association").find("div", class_="broker-address__address")
                try: street = subsoup.find("span", class_="street").string
                except: street = None                
                try: house_number = subsoup.find("span", class_="house-number").string
                except: house_number = None                
                sub_soup = subsoup.find("div", class_="locality-block")
                try: postal_code = subsoup.find("span", class_="postal-code").string
                except: postal_code = None                
                try: locality = subsoup.find("span", class_="locality").string
                except: None                
                subsoup = item.find("div", class_="entity-broker-address-association").find("div", class_="brokeraddress__status")
                try: syndic = subsoup.find("span", class_="syndic").string
                except: syndic = None
                try: mediator = subsoup.find("span", class_="mediator").string
                except: mediator = None
                my_realtor = Realtor(ipi, name, company_name, street, house_number, postal_code, locality, syndic, mediator)
                if debug is not False:               
                    print(my_realtor)
                Realtor.save(my_realtor, outputdir)
            try:
                url = soup.find("div", {"class": "pager"}).find("li", {"class": "pager-next"}).a['href'] # next-page
            except:
                break

if __name__ == "__main__":
    preformat_url = "https://www.ipi.be/lagent-immobilier/recherchez-vous-un-agent-immobilier-agree-ipi-vous-les-trouverez-tous-ici?location={}"
    scrapper(preformat_url=preformat_url, zipcode_list=belgium_zipcode.zipcode_list, outputdir="./data", debug=True)
    sys.exit(0)

