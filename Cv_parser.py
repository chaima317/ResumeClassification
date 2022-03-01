import re
import requests
import json
import unidecode
import time
import urllib.parse
from deep_translator import GoogleTranslator

from geopy.geocoders import Nominatim
import pycountry_convert as pc
from math import ceil
import string
import os
import cv2
from pandas.io.json import json_normalize
from pdf2image import convert_from_path

from gapipy import Client
class CvParser:

    def __init__(self, dir_path, file_name, text, dict_etablissements_address):
        self.dir_path = dir_path
        self.text = text
        self.file_name = file_name
        self.dict_etablissements_address = dict_etablissements_address
        self.informations = dict()
        self.extract_type_poste()
        self.extract_disponibilites()
        #changement du parametre
        self.extract_nationality()
        self.extract_phone_number()
        self.extract_mail()
        self.extract_birth_date()
        self.extract_driving_licence()
        self.extract_name()
        self.extract_gender()
        self.informations['address'] = extract_address_from_text(self.text)
        self.extract_siteRes()
        self.extract_age()
        self.extraire_formation()
        #self.extraire_competence()
        self.extract_skills_from_document()
        self.extraire_langue()
        self.extraire_centreInteret()
        self.extract_photo()
        self.extraire_experience()


    def extract_type_poste(self):
        regexp_type_poste = re.compile("RECH[A-Z]RCHE ?[A-Z]* ?[A-Z]* ?[A-Z]* ?[A-Z]* ?(?:STAGE|CDI|CDD|INTERIM|CTT|CONTRAT A DUREE INDETERMINEE|CONTRAT A DUREE DETERMINEE|CONTRAT DE TRAVAIL TEMPORAIRE|CONTRAT D APPRENTISSAGE|ALTERNANCE|CUI|CAE) ?[\S]* ?[\S]* ?[\S]* ?[\S]*")
        type_poste = re.findall(regexp_type_poste, self.text.upper())
        self.informations['type_poste'] = re.sub("RECH[A-Z]RCHE ?[A-Z]* ?[A-Z]* ?[A-Z]* ?[A-Z]* ?((?:STAGE|CDI|CDD|INTERIM|CTT|CONTRAT A DUREE INDETERMINEE|CONTRAT A DUREE DETERMINEE|CONTRAT DE TRAVAIL TEMPORAIRE|CONTRAT D APPRENTISSAGE|ALTERNANCE|CUI|CAE)) ?[\S]* ?[\S]* ?[\S]* ?[\S]*",'\g<1>', type_poste[0]).strip() if type_poste != [] else 'NULL'        
        self.informations['poste_recherche'] = (" ".join([poste.strip().replace('\'',' ') for poste in re.sub("RECH[A-Z]RCHE ?[A-Z]* ?[A-Z]* ?[A-Z]* ?[A-Z]* ?(?:STAGE|CDI|CDD|INTERIM|CTT|CONTRAT A DUREE INDETERMINEE|CONTRAT A DUREE DETERMINEE|CONTRAT DE TRAVAIL TEMPORAIRE|CONTRAT D APPRENTISSAGE|ALTERNANCE|CUI|CAE)( ?[\S]* ?[\S]* ?[\S]* ?[\S]*)",'\g<1>', type_poste[0]).strip().replace('\'',' ').split() if poste not in ['A','DE','D','DU', 'FIND', 'FIN','PARTIR','FIN', 'ETUDE','EN','AU','POSTE','MOIS','/', '-', '(',')','0','1','2','3','4','5','6','7','8','9','JANVIER','FEVRIER','MARS','AVRIL','MAI','JUIN','JUILLET','AOUT','SEPTEMBRE','OCTOBRE','NOVEMBRE','DECEMBRE','2021','2020']]) if type_poste != [] else 'NULL') or 'NULL'
        print("type de poste", self.informations['type_poste'])
        print("poste recherche",self.informations['poste_recherche'] )
    def extract_disponibilites(self):

        regexp_disponibilite = re.compile("(?:A PARTIR|DISPONIBLE) ?[\S]* ?[\S]* ?[\S]* ?(?:JANVIER|FEVRIER|MARS|AVRIL|MAI|JUIN|JUILLET|AOUT|SEPTEMBRE|OCTOBRE|NOVEMBRE|DECEMBRE) ?20[0-9][0-9]")
        disponibilite = re.findall(regexp_disponibilite, self.text.upper())
        self.informations['disponibilite'] = re.sub("(?:A PARTIR|DISPONIBLE) ?[\S]* ?[\S]* ?[\S]* ?((?:JANVIER|FEVRIER|MARS|AVRIL|MAI|JUIN|JUILLET|AOUT|SEPTEMBRE|OCTOBRE|NOVEMBRE|DECEMBRE) ?20[0-9][0-9])",'\g<1>', disponibilite[0]).strip() if disponibilite != [] else 'NULL'
       

    def extract_phone_number(self):
        regexp_phone = re.compile('\(?(?:(?:\+|00)6[6543210]|(?:\+|00)7|(?:\+|00) ?3[9643210]|(?:\+|00)9[976]\d|(?:\+|00)8[987530]\d|(?:\+|00)6[987]\d|(?:\+|00)5[90]\d|(?:\+|00)42\d|(?:\+|00)3[875]\d|(?:\+|00)2[98654321]\d|(?:\+|00)9[8543210]|(?:\+|00)8[6421]|(?:\+|00)5[87654321]|(?:\+|00)4[987654310]|(?:\+|00)2[70]|(?:\+|00)1|0)\)?\s?[1-9](?:[\s\.\-]?\(?\d{2,5}\)?){3,5}')
        tel = re.findall(regexp_phone, self.text)
        if tel:
            #On prend en priorité les numéros français
            numbers = [num for num in tel if re.match('(?:\+33|06|07)[0-9 \.()\-]+', num)]
            tel = numbers or tel

            tel = tel[0]
            tel = tel.replace(' ', '')
            tel = tel.replace('-', '')
            tel = tel.replace('.', '')
            tel = tel.replace('(', '')
            tel = tel.replace(')', '')
            tel = tel.replace('+330', '0')
            tel = tel.replace('+33', '0')
            tel = tel.replace('+', '00')
            tel = tel.strip()

        self.informations['phone'] = tel or 'NULL'

    def extract_mail(self):
        regexp_mail = re.compile("[A-Za-z]+[A-Za-z0-9--\._]+@[A-Za-z0-9\.\- ]+\.(?:com|fr|net|org|edu|gov|mil|int|info|biz|name|pro|coop|aero|museum|arpa|asia|bike|bzh|cat|ceo|post|[a-z]{2,2})")
        mail = re.findall(regexp_mail, self.text.lower())
        mail2 = [m.split()[0] for m in mail if re.match('[A-Za-z]+[A-Za-z0-9--\._]+@[A-Za-z0-9\.\-]+\.(com|fr|net|org|edu|gov|mil|int|info|biz|name|pro|coop|aero|museum|arpa|asia|bike|bzh|cat|ceo|post)', m.split()[0])]
        mail = mail2 or mail
        self.informations['mail'] = mail[0].strip().replace(' ', '') if mail != [] else 'NULL'

    def extract_name(self):
        first_name = ''
        last_name = ''

        # Si le nom du fichier respectent la norme fixée
        if re.match('2020-12-03(?:-|_)CV(?:-|_)[A-Z]+((?:-|_)[A-Z]+)*(?:-|_)[A-Z][A-Za-zéïàèîôû]+((?:-|_)[A-Z][A-Za-zéïàèîôû]+)*.pdf', self.file_name):
            first_name = re.sub( '2020-12-03(?:-|_)CV(?:-|_)[A-Z]+((?:-|_)[A-Z]+)*(?:-|_)([A-Z][A-Za-zéïàèîôû]+((?:-|_)[A-Z][A-Za-zéïàèîôû]+)*).pdf','\g<2>', self.file_name)
            last_name = re.sub('2020-12-03(?:-|_)CV(?:-|_)([A-Z]+((?:-|_)[A-Z]+)*)(?:-|_)[A-Z][A-Za-zéïàèîôû]+((?:-|_)[A-Z][A-Za-zéïàèîôû]+)*.pdf','\g<1>', self.file_name)
            first_name, last_name = corr_name(first_name, last_name)
        # Sinon on va essayer de le trouver en utilisant le nom du pdf, l'adresse mail et le texte
        else:
            if re.match('[A-Za-z]+[A-Za-z0-9--\._]+@[A-Za-z0-9\.\- ]+\.[A-Za-z]{2,4}', self.informations['mail']):
                first_part_mail = re.sub('([A-Za-z]+[A-Za-z0-9--\._]+)@[A-Za-z0-9\.\- ]+\.[A-Za-z]{2,4}', '\g<1>', self.informations['mail'])
                list_word = [word for word in self.text.upper().split() if (first_part_mail.upper().find(word) >= 0 or self.dir_path.upper().find(word) >= 0) and len(word) > 2]
                # Pour chaque mot, on appelle l'API des prénoms afin de savoir si c'est un nom ou un prénom
                api_url = "https://api.genderize.io?"
                for word in list(set(list_word)):
                    api_url += 'name[]=' + word + '&'
                api_url = api_url[:-1]
                response = requests.get(api_url)

                #On vérifie si c'est un nom ou un prenom
                if response.json() != []:
                    for name in response.json():
                        if name.get('count') > 5 and name.get('count') < 1000:
                            last_name += ' ' + name.get('name')
                        elif name.get('count') > 1000:
                            first_name += ' ' + name.get('name')
  
                first_name = first_name.strip()
                last_name = last_name.strip()
                first_name, last_name = corr_name(first_name, last_name)

        self.informations['first_name'] = first_name or 'NULL'
        self.informations['last_name'] = last_name or 'NULL'

    def extract_driving_licence(self):
        # Regexp permis de conduire
        regexp_permis = re.compile('PERMIS ?(?:DE CONDUIRE|TYPE)? ?:? ?(?:AM|BSR|A|A1|A2|B|B1|B2|BE|BVA|C|C1|CE|C1E|D|D1|D2|DE|DE1)')
        listPermis = re.findall(regexp_permis, self.text.upper())
        # On garde seulement le nom du permis
        self.informations['driving_licences'] = [re.sub('PERMIS ?(?:DE CONDUIRE|TYPE)? ?:? ?((?:AM|BSR|A|A1|A2|B|B1|B2|BE|BVA|C|C1|CE|C1E|D|D1|D2|DE|DE1))','\g<1>', permis).strip() for permis in listPermis if re.match('PERMIS ?(?:DE CONDUIRE|TYPE)? ?:? ?(?:AM|BSR|A|A1|A2|B|B1|B2|BE|BVA|C|C1|CE|C1E|D|D1|D2|DE|DE1)', permis)] or 'NULL'
 
    def extract_age(self):
        regexp_age = re.compile('[0-9]{2,3} ANS')
        age = re.findall(regexp_age, self.text.upper())
        self.informations['age'] = 'NULL' if age == [] else re.sub('([0-9]{2,3}) ANS', '\g<1>', age[0])

    def extract_birth_date(self):
        regexp_birth_date = re.compile('DATE ?(?:DE| )? ?NAISSANCE ?:? ?[0-9]{2}(?:-|/|\.)[0-9]{2}(?:-|/|\.)[0-9]{4}')
        birth_date = re.findall(regexp_birth_date, self.text.upper())
        self.informations['birth_date'] = 'NULL' if birth_date == [] else re.sub('DATE ?(?:DE| )? ?NAISSANCE ?:? ?([0-9]{2}(?:-|/|\.)[0-9]{2}(?:-|/|\.)[0-9]{4})', '\g<1>', birth_date[0]).strip()


  ## ==> dans cette partie j'ai mis toutes les nationalitées possibles
    def extract_nationality(self):


        regexp_nationality = re.compile('Afghan| Albanian |   Algerian  |   American  |  Andorran  |   Angolan |  Antiguans | Argentinean  |   Armenian  |   Australian  |   Austrian  |   Azerbaijani  |   Bahamian  | Bahraini  |   Bangladeshi  |   Barbadian  |   Barbudans  |   Batswana  |   Belarusian  |   Belgian  | Belizean  |   Beninese  |   Bhutanese  |   Bolivian  |   Bosnian  |   Brazilian  |   British  | Bruneian  |   Bulgarian  |   Burkinabe  |   Burmese  |   Burundian  |   Cambodian  |   Cameroonian  | Canadian  |   Cape Verdean  |   Central African  |   Chadian  |   Chilean  |   Chinese  | Colombian  |   Comoran  |   Congolese  |   Costa Rican  |   Croatian  |   Cuban  |   Cypriot  | Czech  |   Danish  |   Djibouti  |   Dominican  |   Dutch  |   Dutchman  |   Dutchwoman  | East Timorese  |   Ecuadorean  |   Egyptian  |   Emirian  |   Equatorial Guinean  |   Eritrean  | Estonian  |   Ethiopian  |   Fijian  |   Filipino  |   Finnish  |   French  |   Gabonese  |   Gambian  | Georgian  |   German  |   Ghanaian  |   Greek  |   Grenadian  |   Guatemalan  |   Guinea-Bissauan  | Guinean  |   Guyanese  |   Haitian  |   Herzegovinian  |   Honduran  |   Hungarian  |   I-Kiribati  | Icelander  |   Indian  |   Indonesian  |   Iranian  |   Iraqi  |   Irish  |   Israeli  |   Italian  | Ivorian  |   Jamaican  |   Japanese  |   Jordanian  |   Kazakhstani  |   Kenyan  | Kittian |  Nevisian  |   Kuwaiti  |   Kyrgyz  |   Laotian  |   Latvian  |   Lebanese  |   Liberian  | Libyan  |   Liechtensteiner  |   Lithuanian  |   Luxembourger  |   Macedonian  |   Malagasy  | Malawian  |   Malaysian  |   Maldivan  |   Malian  |   Maltese  |   Marshallese  |   Mauritanian  | Mauritian  |   Mexican  |   Micronesian  |   Moldovan  |   Monacan  |   Mongolian  |   Moroccan  | Mosotho  |   Motswana  |   Mozambican  |   Namibian  |   Nauruan  |   Nepalese  |   Netherlander  | New Zealander  |   Ni-Vanuatu  |   Nicaraguan  |   Nigerian  |   Nigerien  |   North Korean  | Northern Irish  |   Norwegian  |   Omani  |   Pakistani  |   Palauan  |   Panamanian  | Papua New Guinean  |   Paraguayan  |   Peruvian  |   Polish  |   Portuguese  |   Qatari  | Romanian  |   Russian  |   Rwandan  |   Saint Lucian  |   Salvadoran  |   Samoan  |   San Marinese  | Sao Tomean  |   Saudi  |   Scottish  |   Senegalese  |   Serbian  |   Seychellois  | Sierra Leonean  |   Singaporean  |   Slovakian  |   Slovenian  |   Solomon Islander  |   Somali  | South African  |   South Korean  |   Spanish  |   Sri Lankan  |   Sudanese  |   Surinamer  | Swazi  |   Swedish  |   Swiss  |   Syrian  |   Taiwanese  |   Tajik  |   Tanzanian  |   Thai  | Togolese  |   Tongan  |   Trinidadian |  Tobagonian  |   Tunisian  |   Turkish  |   Tuvaluan  | Ugandan  |   Ukrainian  |   Uruguayan  |   Uzbekistani  |   Venezuelan  |   Vietnamese  |   Welsh  | Yemenite  |   Zambian  |   Zimbabwean ')
        nationality = re.findall(regexp_nationality, unidecode.unidecode(self.text.upper()))
        self.informations['nationality'] = 'NULL' if nationality == [] else re.sub('Afghan| Albanian |   Algerian  |   American  |  Andorran  |   Angolan |  Antiguans | Argentinean  |   Armenian  |   Australian  |   Austrian  |   Azerbaijani  |   Bahamian  | Bahraini  |   Bangladeshi  |   Barbadian  |   Barbudans  |   Batswana  |   Belarusian  |   Belgian  | Belizean  |   Beninese  |   Bhutanese  |   Bolivian  |   Bosnian  |   Brazilian  |   British  | Bruneian  |   Bulgarian  |   Burkinabe  |   Burmese  |   Burundian  |   Cambodian  |   Cameroonian  | Canadian  |   Cape Verdean  |   Central African  |   Chadian  |   Chilean  |   Chinese  | Colombian  |   Comoran  |   Congolese  |   Costa Rican  |   Croatian  |   Cuban  |   Cypriot  | Czech  |   Danish  |   Djibouti  |   Dominican  |   Dutch  |   Dutchman  |   Dutchwoman  | East Timorese  |   Ecuadorean  |   Egyptian  |   Emirian  |   Equatorial Guinean  |   Eritrean  | Estonian  |   Ethiopian  |   Fijian  |   Filipino  |   Finnish  |   French  |   Gabonese  |   Gambian  | Georgian  |   German  |   Ghanaian  |   Greek  |   Grenadian  |   Guatemalan  |   Guinea-Bissauan  | Guinean  |   Guyanese  |   Haitian  |   Herzegovinian  |   Honduran  |   Hungarian  |   I-Kiribati  | Icelander  |   Indian  |   Indonesian  |   Iranian  |   Iraqi  |   Irish  |   Israeli  |   Italian  | Ivorian  |   Jamaican  |   Japanese  |   Jordanian  |   Kazakhstani  |   Kenyan  | Kittian |  Nevisian  |   Kuwaiti  |   Kyrgyz  |   Laotian  |   Latvian  |   Lebanese  |   Liberian  | Libyan  |   Liechtensteiner  |   Lithuanian  |   Luxembourger  |   Macedonian  |   Malagasy  | Malawian  |   Malaysian  |   Maldivan  |   Malian  |   Maltese  |   Marshallese  |   Mauritanian  | Mauritian  |   Mexican  |   Micronesian  |   Moldovan  |   Monacan  |   Mongolian  |   Moroccan  | Mosotho  |   Motswana  |   Mozambican  |   Namibian  |   Nauruan  |   Nepalese  |   Netherlander  | New Zealander  |   Ni-Vanuatu  |   Nicaraguan  |   Nigerian  |   Nigerien  |   North Korean  | Northern Irish  |   Norwegian  |   Omani  |   Pakistani  |   Palauan  |   Panamanian  | Papua New Guinean  |   Paraguayan  |   Peruvian  |   Polish  |   Portuguese  |   Qatari  | Romanian  |   Russian  |   Rwandan  |   Saint Lucian  |   Salvadoran  |   Samoan  |   San Marinese  | Sao Tomean  |   Saudi  |   Scottish  |   Senegalese  |   Serbian  |   Seychellois  | Sierra Leonean  |   Singaporean  |   Slovakian  |   Slovenian  |   Solomon Islander  |   Somali  | South African  |   South Korean  |   Spanish  |   Sri Lankan  |   Sudanese  |   Surinamer  | Swazi  |   Swedish  |   Swiss  |   Syrian  |   Taiwanese  |   Tajik  |   Tanzanian  |   Thai  | Togolese  |   Tongan  |   Trinidadian |  Tobagonian  |   Tunisian  |   Turkish  |   Tuvaluan  | Ugandan  |   Ukrainian  |   Uruguayan  |   Uzbekistani  |   Venezuelan  |   Vietnamese  |   Welsh  | Yemenite  |   Zambian  |   Zimbabwean ', '\g<1>', nationality[0]).strip()







    def extract_siteRes(self):

         regexp_site_res = re.compile('(?:http://|https://|HTTP://|HTTPS://)[a-zA-Z0-9\.\-=/\?]+')
         site_res = re.findall(regexp_site_res, self.text)
         self.informations['sites_socialNetwork'] = [site.strip() for site in site_res] or 'NULL'



    def extraire_formation(self):
        tabFormation = []
        tabF = []

        # pour formation
        # on utilise 2 méthode pour extraire les formation soit on coupe les bloc par date (on arrete le bloc quand une 3e data apparait)
        # soit on coupe les bloc par les mots de niveau comme master, licence, etc et on arrete le bloc quand un autre de ces mot apparait
        # et sinon les 2 méthodes arrete le bloc si une longueur est dépasse ou si les mots experience apparaissent
        # on compare quelle méthode trouve le plus de formation
        regex = r"(20[0-2][0-9]|19[0-9][0-9]).{0,5}(20[0-2][0-9]|19[0-9][0-9]).{0,200}?(?=(master|licence|Baccalaureat|dut|lycee|universite|ecole))(.{0,400}?(?=(20[0-2][0-9]|19[0-9][0-9]|Experience|EXPERIENCE|experience|experience))|(.{0,200}))"
        matches = re.findall(regex, self.text, re.MULTILINE | re.IGNORECASE)
        compteur1 = len(matches)

        regex2 = r"(Master|master|MASTER|Licence|LICENCE|licence|Baccalaureat)(.{0,400}?(?=(Master|master|MASTER|Licence|LICENCE|licence|Experience|EXPERIENCES|experience|experience|COMPETENCES|Competence|competence|Baccalaureat|EXPERIENCES|EXPERIENCE))|.{0,200})"
        matches = re.findall(regex2, self.text, re.MULTILINE | re.IGNORECASE)
        compteur2 = len(matches)
        # on utilise le regexp le plus performant a chaque fois
        regex = regex2 if compteur1 < compteur2 else regex

        matches = re.finditer(regex, self.text, re.MULTILINE | re.IGNORECASE)

        # on analyse chaque formation trouvé
        for matchNum, match in enumerate(matches, start=1):
            formation = match.group()
            # expression reguliere pour extraire le niveau de la formation
            regexFormation = r"(master ?[1-2])|(licence|L1|L2|L3)|(baccalaureat|baccalaureat)|(DUT)"
            matchesFormation = re.finditer(regexFormation, formation, re.IGNORECASE)
            niveau = 'NULL'
            for matchNumFormation, matchFormation in enumerate(matchesFormation, start=1):
                niveau = matchFormation.group().strip()

            # expression reguliere pour extraire le nom de l'ecole
            ecole = "NULL"
            regexEcole = r"(Universite|lycee|ecole|college)[ ][a-z]*?[ ][a-z0-9]*([ ][a-z0-9]*)?"
            matchesEcole = re.finditer(regexEcole, formation, re.IGNORECASE)
            for matchNumEcole, matchEcole in enumerate(matchesEcole, start=1):
                ecole = matchEcole.group().strip()
                # expression reguliere pour extraire la date de debut et de fin de la formation
            dateDebut = "NULL"
            dateFin = "NULL"
            regexDate = r"((janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)[ ])?(20[0-2][0-9]|19[0-9][0-9])"
            matchesDate = re.finditer(regexDate, formation, re.MULTILINE | re.IGNORECASE)
            compteurDate = 0
            for matchNumDate, matchDate in enumerate(matchesDate, start=1):
                if matchNumDate == 1:
                    dateDebut = matchDate.group().strip()
                elif matchNumDate == 2:
                    dateFin = matchDate.group().strip()
                    # expression reguliere pour extraire la specialite de la formation
            specialite = "NULL"
            regexSpecialite = r"(informatique)"
            matchesSpecialite = re.finditer(regexSpecialite, formation, re.IGNORECASE)
            for matchNumEcole, matchSpecialite in enumerate(matchesSpecialite, start=1):
                specialite = matchSpecialite.group().strip()
                
            niveau = niveau.upper().replace('MASTER1','MASTER 1').replace('MASTER2','MASTER 2').replace('LICENCE1','LICENCE 1').replace('LICENCE2','LICENCE 2').replace('LICENCE3','LICENCE 3').strip()
            if niveau != 'NULL' and not (specialite == 'NULL' and ecole == 'NULL'):
                tabFormation.append([niveau.upper(), specialite.upper(), ecole.upper(), dateDebut, dateFin, 'NULL'])
        
        for niveau, specialite, ecole, dateDebut, dateFin, tel_ecole in tabFormation:
            if ecole != 'NULL':
                #Si l'école à déjà été traitée
                if ecole.upper() in self.dict_etablissements_address:
                    adr_ecole = self.dict_etablissements_address[ecole.upper()][0]
                    tel_ecole = self.dict_etablissements_address[ecole.upper()][1]
                else:
                    # API établissement supérieur
                    if 'UNIVERSITE' in ecole.upper().split():
                        api_url = "https://data.enseignementsup-recherche.gouv.fr/api/records/1.0/search/?dataset=fr-esr-principaux-etablissements-enseignement-superieur&q=" + ecole.replace('  ', ' ').replace(' ', '+') + "&limit=1"
                        response = requests.get(api_url)
                        if response.json().get('records') != []:
                            ecole = unidecode.unidecode(str(response.json().get('records', 'NULL')[0].get('fields', 'NULL').get('uo_lib','NULL')).upper().replace('\'', ' ').replace('"', ' '))
                            adr_ecole = extract_address(str(response.json().get('records', '')[0].get('fields', '').get('adresse_uai', '')) + ' ' + str( response.json().get('records', '')[0].get('fields', '').get('localite_acheminement_uai','')))
                            tel_ecole = str(response.json().get('records', 'NULL')[0].get('fields', 'NULL').get('numero_telephone_uai','NULL'))
                        else:
                            adr_ecole = {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}
                            tel_ecole = 'NULL'
                    # API établissement scolaire
                    else:
                        tel_ecole = 'NULL'
                        api_url = 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre&q=' + ecole.replace('  ', ' ').replace(' ', '+') + '&limit=1'
                        response = requests.get(api_url)
                        if response.json().get('records') != []:
                            ecole = unidecode.unidecode(str(response.json().get('records', 'NULL')[0].get('fields', 'NULL').get('appellation_officielle', 'NULL')).upper().replace('\'', ' ').replace('"', ' '))
                            adr_ecole = extract_address(str(response.json().get('records', '')[0].get('fields', '').get('adresse_uai', '')) + ' ' + str(response.json().get('records', '')[0].get('fields', '').get('localite_acheminement_uai','')))
                        else:
                            adr_ecole = {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}
                    
                    #On ajoute dans le dictionnaire la clé école avec sa valeur adresse/tel ecole, pour les prochaines fois
                    self.dict_etablissements_address[ecole] = [adr_ecole, tel_ecole]
                tabF.append([niveau, specialite, ecole, dateDebut, dateFin, adr_ecole, tel_ecole])


        tabFormation = tabF

        self.informations['trainings'] = tabFormation or 'NULL'

    def extract_gender(self):
        # On remplace tous les signes de ponctuation par un espace
        replace_punctuation = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        first_name = self.informations['first_name'].translate(replace_punctuation)

        # On split le prénom en sous-prénom
        names = first_name.split()

        # URL de l'API
        api_url = "https://api.genderize.io?"

        # On ajoute chaque sous-prénom à l'URL
        for name in names:
            api_url += 'name=' + name + '&'
        # On supprime le '&' en trop
        api_url = api_url[:-1]

        # On lance la requête
        response = requests.get(api_url)
        # print(response.json())

        # Si aucun cas n'est satisfait, on renvoie NULL pour le genre
        self.informations['gender'] = 'NULL'

        # Cas où le prénom est composé
        if len(names) > 1:
            cpt_female = 0
            cpt_male = 0
            # Pour chaque sous-prénom, on compte si c'est une fille ou un garçon
            for dic in response.json():
                if dic.get('gender') == 'female':
                    cpt_female += 1
                elif dic.get('gender') == 'male':
                    cpt_male += 1
            # On prend le max entre les deux
            if cpt_female > cpt_male:
                self.informations['gender'] = 'F'
            elif cpt_female < cpt_male:
                self.informations['gender'] = 'M'
        # Cas où le prénom n'est pas composé
        else:
            if response.json().get('gender') == 'female':
                self.informations['gender'] = 'F'
            elif response.json().get('gender') == 'male':
                self.informations['gender'] = 'M'

    #def extraire_competence(self):
        # clean le texte du cv
        #regex = ("skills|SKILLS?Communication|reseautage|Esprit d equipe|Travail autonome|Capacite à travailler sous pression|marketing|redaction|developpement de contenu|Gestion du temps|Photoshop|Joomia|Indesign|Graphisme|Illustration|Photographie|Images animees|Videographie|Mise en page|Ruby|Microsoft ASP.NET MVC.Web API|C#|eco-responsables|processus de recyclage|Conceptualisation des espaces 3D|Gestion de marque|Analyse des concurrents|Marketing sur les reseaux sociaux|Optimisation du moteur de recherche|Marketing de contenu|Recherche de marche|Redacteur publicitaire|notions juridiques et financières|Rigueur|diplomatie|Travailleur social agree|Association|action sociale|Sens de responsabilites|Travail en equipe|Flexible|Facilite d integration|Sens de responsabilite|Autodidaxie|Creativite et force de proposition|Ambitieux|Organise|Applique|Desireux dapprendre|Dynamique|Communication|adaptation facile|nouvelles technologies|Benevole|Organise|autonome|assidu|curieux|Travail en equipe|Perseverant|Adaptable|Communicant|Curiosite|Serieux|Motive|rigoureux|organise|autonome|Bonne capacite danalyse|traitements de problematiques|Bonnes qualites redactionnel|bonne approche des clients|Sens negociation|Capacite dadaptation|Competences relationnelles|Esprit dequipe|Travail en equipe|Respect des delais|etablir un cahier des charges|Capacite à sorganiser|Determine|curieuse|rigoureuse|aventures|Relationnel|Adaptabilite|Apprentissage|Rigueur|Autonomie|Travail en groupe|Travail sous pression|Autonome|Organise|Rigoureux|Eclipse|NetBeans|AndroidStudio|Code:Blocks|Dev\-C\+\+|VisualStudio|STVisualdevelop|IDE|SASSoftware|SASViya|Jupyter|Linux|Ubuntu|NASM|Anaconda|Spyder|Talend|Tableau|BusinessObjects|SAS|Jira|Trello|jupyter-notebook|pycharm|Oracle|SasStudio|Mangodb|PowerBI|Talend|Tableau|Excel|Jupyter|Anaconda|Jupyter|spyder|KNIME|PhpMyAdmin|Colab|Dynamic|Dynamique|collaborative work|Collaboratif|Analyse critique|Ponctualite|Travail en groupe|Gestion de temps|Esprit d’analyse|Meticulosite|communication|Agile|Waterfal|Python|SQL|PL/SQL|SAS|Java|C|SQL|MATLAB|Python|Sql|Java|OcamlMatlab|UML|Haskell|SQL3|SAS|JavaScript|PHP|J2E|Pascal|HTML|CSS|XML|R|Java/JEE|OCaml|Mysql|Html|VBA|DATA warehouse|DateWarehouse|PHP5|Symfony|Angular9|SpringBoot|JEE|HTML5|CSS3|JS|JavaScript|pandas|numpy|matplotlib|seaborn|PLSQL|Ocaml|Scala|SQL|PLSQL|NoSQL|Prolog|SAS|Oracle|MongoDB|MySQL|Talend|Tableau|BusinessObjects|TensorFlow|Keras|Scikit-learn|Scikit-Fuzzy|MicrosoftOfficeExcel|Prolog|Oracle|MongoDB|MySQL|DataBase|Talend|DataIntegration|DataQuality|SAS|Tableau|BusinessObjects|HADOOP|HDFS|MapReduce|HBASE|SPARK|RSTUDIO|WEKA|IBMSPSSMODELER|REDIS|MongoDB|JupyterNotebook|Eclipse|SAS|VisualStudioCode|Rstudio|AndroidStudio|Git|Oracle|SASViya|SAS9|MangoDB|MATLAB|Oracle|BusinessObjects|MethodeAgile|SCRUM|Trello|GitHub|oracle|PLSQL|SQLserver|SSIS|Trello|Word|Excel|PowerPoint|make|git|Oracle|SasStudio|PowerBI|Excel|Jupyter|ApacheKakfa|Elasticsearch|Logstash|Kibana|FileBeat|Trello|MarvenApp|Git|UML|Docker|SpringBoot|SpringData|SpringSecurity|HTML|Thymeleaf|CSS|VB|UML|GRASPpattern|Merise|Proto.io|Axure|Internet des objets|IOT|Business intelligence|Representation graphique de donnees statistiques|Domotique|meetup tafterworks|Statistiques")
        #matches = re.finditer(regex, self.text, re.MULTILINE | re.IGNORECASE)       
        #listeCompetences = [unidecode.unidecode(match.group().upper().strip()) for matchNum, match in enumerate(matches, start=1)]
        #self.informations['skills'] = list(set(listeCompetences)) or 'NULL'
     



    #extraction of skills using apis 


    def extract_skills_from_document(self):
           skills_from_doc_endpoint = "https://emsiservices.com/skills/versions/latest/extract"
           text = input(self.text)

           payload = "{ \"text\": \"... " + text + " ...\", \"confidenceThreshold\": " + confidence_interval + " }"
          
            headers = {
                'authorization': "Bearer " + access_token,
                'content-type': "application/json"
            }

            response = requests.request("POST", skills_from_doc_endpoint, data=payload.encode('utf-8'), headers=headers)

            skills_found_in_document_df = pd.DataFrame(json_normalize(response.json()['data'])); # Where response is a JSON object drilled down to the level of 'data' key
                                            
            return skills_found_in_document_df
  
          


    def extraire_langue(self):
        listLangue = []
        langue = "NULL"
        niveau = "NULL"
        regex = r"(francais|anglais|Allemand|Kabyle|Arabe|Chinois|mandarin|hindi|bengali|panjabi|Espagnol|Deutsch|Turc|Berbère|Wolof|Tamoul|italien|portuguais|russe|japonais|danois|polonais|javanais|telougou|malais|coreen|marathi|turc|vietnamien|tamoul|italien|persan|thai|gujarati|polonais|pachtou|kannada|malayalam|soundanais|oriya|birman|ukrainien|bhojpouri|filipino|yorouba|maithili|ouzbek|sindhi|amharique|peul|roumain|oromo|igbo|azeri|awadhi|visayan|neerlandais|kurde|malgache|saraiki|chittagonien|khmer|turkmène|assamais|madourais|somali|marwari|magahi|haryanvi|hongrois|chhattisgarhi|grec|chewa|deccan|akan|kazakh|sylheti|zoulou|tcheque)[ ](.*?[ ].*?[ ].*?[ ])"

        matches = re.finditer(regex, self.text, re.MULTILINE | re.IGNORECASE)

        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                if (groupNum == 1):
                    langue = match.group(groupNum).upper().strip()
                elif (groupNum == 2):
                    regexNiveau = r"(A1|B1|B2|C1|C2|langue maternelle|bilingue|debutant|avance|HSK 3)"
                    matchesNiveau = re.finditer(regexNiveau, match.group(groupNum), re.IGNORECASE)
                    for matchNumNiveau, matchNiveau in enumerate(matchesNiveau, start=1):
                        niveau = matchNiveau.group().upper().strip()
            listLangue.append([langue, niveau])

        self.informations['languages'] = listLangue or 'NULL'

    def extraire_centreInteret(self):
        regex = r"(Cyclisme|Patisserie|Lecture|Musique|Bricolages|Associations|Conferences|Mangas|Science|Jeux videos|Technologie|Physique|Philosophie|Travail Associatif|Planification|Entraînement physique|Transport et mobilite|technologies Web emergentes|Tennis de table|Bricolage|Voyage|Natation|handball|Engagement benevole|Aviron|Boxe|Benevolat|Photographie|Basketball|Football|cinema|escalade|Photoshop|Tennis|SeriesTV|Films|Art martiaux|musique|documentaire|Pâtisserie|volley-ball|benevolat|Football|litterature|Cyclisme|Cuisiner|Hand-ball|Jeux cognitifs)"
        matches = re.finditer(regex, self.text, re.MULTILINE | re.IGNORECASE)
        listeCentreInteret = [match.group().upper().strip() for matchNum, match in enumerate(matches, start=1)]
        self.informations['areas_of_interest'] = list(set(listeCentreInteret)) or 'NULL'

    def extraire_experience(self):

        #API entreprise https://entreprise.data.gouv.fr/api/sirene/v1/full_text/escapade+francaise
        tabExperiences = []
        tabE = []

        # pour experiences

        regex = r"(janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)[ ](20[0-2][0-9]|19[0-9][0-9]).{0,20}(20[0-2][0-9]|19[0-9][0-9])(?!.*?(université|universite|lycee|lycée|dut|ecole|classe)).*?(?=(janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre))"
        matches = re.finditer(regex, self.text, re.MULTILINE | re.IGNORECASE)

        matches = re.finditer(regex, self.text, re.MULTILINE | re.IGNORECASE)

        # on analyse chaque experiences trouve

        for matchNum, match in enumerate(matches, start=1):
            s = experience = match.group()

            # expression reguliere pour extraire le poste occupe
            regexPoste = r"(technicien developpeur|ingenieur developpeur|Developpeuse web|Developpeur web|Preparateur de plateaux|Analyste Junior|Ingenieure des applications|ingenieure R&D|Vacataire|electricien|ouvrier|Magasinier|developpement WEB|Employe polyvalent|Assistant caisse|Hote de caisse|Receptionniste|Analyste strategique|Chargee de veille|Expert veille internet|Vendeuse|Consultant|Product Owner|Consultant reporting BI|Data scientist|Serveur|CONSEILLER COMMERCIAL|Analyste|SOFTWARE DEVELOPER|Employee polyvalente|Caissiere|Business Analyst|Developpeur Full Stack|Analyst|DATA ENGINEER|Baby-sitter|Equipier polyvalent|Developpeur Android|INGENIEUR CLOUD|DATA ENGINEER JUNIOR|Ingenieur)"            
            matchesFormation = re.finditer(regexPoste, experience,re.IGNORECASE)
            poste = 'NULL'
            for matchNumFormation, matchFormation in enumerate(matchesFormation, start=1):
                poste =  matchFormation.group().strip()
                if poste != 'NULL':
                    s = s.replace(poste, '')
            # expression reguliere pour extraire le nom de l'entreprise
            entreprise = "NULL"
            regexEntreprise = r"(ORANGE|HUAWEI|ADNTECH|SIMENS|100KAKTUS|Ministere de l education nationale|Escapade Francaise|Escapade Francaise|Ministere de l Eau|SERVAIR- PAC|SERVAIR|Banque Postale|Societe nationale d'assurance|AlKhorayef Petroleum Company|Laboratories GREMAN|Robert Bosch Automotive Steering|Pharmaceuetical Institute|Haut Commissariat au Plan|Direction Generale des Impots|UNIVERSITE BEIHANG|NEW PATH|MEUBLES TECH|RICOTRANS|ELECTRONICS|METRAGAZ|Mercedes-Benz|Quick|McDonald s|ASAPLACE|Groupe PSA|MONOPRIX|Hotel Mont Louis|keenturtle|ministere de sante publique|l universite Laval|Clear Impulse|Ministere de l Interieur|Digimind|Auchan|l Universite Paris 13|Groupe Banque Populaire|Shokly|Royal Air Maroc|Office National Des Aeroports|SYSTRAN SAS Paris|Office National des Chemins de Fer|Credit Agricole|Henceforth|MAMDA-MCMA|OCP|Juillet 2020|En cours|6mois|BEREXIA|Juillet 2018|Agence urbaine Kenitra|GRILL 169|Monkey Locky|Generali Assurance|FPT SOFTWARE|Extens Consulting|Normal FRANCE|LIDL|SQLI|DXC TECHNOLOGY|ORANGE BUSINESS SERVICES|SICEM|2SI|Extens Consulting|Declic Eveil|Universite de Mersin|Burger King|AXELIFE|AIS TECH|SSI|AlgoConsulting|INOV-Group)"            
            matchesEntreprise = re.finditer(regexEntreprise, experience,re.IGNORECASE)
            for matchNumE, matchEntreprise in enumerate(matchesEntreprise, start=1):
                entreprise = matchEntreprise.group().strip()
                if poste != 'NULL':
                    s = s.replace(entreprise, '')  
            
           # expression reguliere pour extraire la date de debut et de fin de la formation
            dateDebut = "NULL"
            dateFin = "NULL"
                
            regexDate = r"((janvier|fevrier|mars|avril|mai|juin|juillet|aout|Août|septembre|octobre|novembre|decembre)[ ])?(20[0-2][0-9]|19[0-9][0-9])|((janvier|fevrier|mars|avril|mai|juin|juillet|aout|Août|septembre|octobre|novembre|decembre)[ ])(20[0-2][0-9]|19[0-9][0-9])?"
            matchesDate = re.finditer(regexDate, experience, re.MULTILINE | re.IGNORECASE)
            compteurDate=0
            for matchNumDate, matchDate in enumerate(matchesDate, start=1):
                if matchNumDate==1:
                    dateDebut = matchDate.group().strip()
                    s = s.replace(dateDebut, '')
                elif matchNumDate==2:
                    dateFin = matchDate.group().strip()
                    s = s.replace(dateFin, '')
              
            # expression reguliere pour extraire le type de contrat
            typeContrat = "NULL"
            regexContrat = r"(stage|CDD|CDI)"            
            matchesSpecialite = re.finditer(regexContrat, experience,re.IGNORECASE)
            for matchNumEcole, matchSpecialite in enumerate(matchesSpecialite, start=1):
                typeContrat =  matchSpecialite.group().strip()
                if poste != 'NULL':
                    s = s.replace(typeContrat, '')
            description = s.replace('\'', ' ').replace('"', ' ').replace(',','').replace(';','').replace('  ', ' ').strip()[:100] or 'NULL'  

            if not (poste == 'NULL' and typeContrat == 'NULL' and entreprise == 'NULL'):    
                #Recupération de l'adresse de l'entreprise 
                api_url = 'https://entreprise.data.gouv.fr/api/sirene/v1/full_text/' + entreprise.replace('  ', ' ').replace(' ', '+')
                response = requests.get(api_url)
                if response.json().get('etablissement'):
                    adr_entreprise = extract_address(str(response.json().get('etablissement', '')[0].get('geo_adresse', '')))
                else:
                    adr_entreprise = {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}
                
                tabE.append([poste.upper(),typeContrat.upper(),entreprise.upper(),dateDebut,dateFin, description, adr_entreprise])        
        
        tabExperiences = tabE 
        
        self.informations['experiences'] = tabExperiences or 'NULL'

    def extract_photo(self):

        """
        Fonction permettant d'extraire automatiquement la photo d'un fichier PDF
        La fonction va permettre de détecter le visage de la personne (s'il y a une photo sur le CV)
        @params:
            storage_file - Required : Le fichier de stockage des PDF
            pdf_file     - Required : Le fichier PDF
        @return:
            lien_photo           : Le lien vers la photo ou 'NULL' s'il n'y a pas de photo sur le CV
        """
        try:
            # Fichier de sauvegarde des photos de CV
            photo_file = './Photos_CV/'
            # On met le pdf en image
            images = convert_from_path(self.dir_path + self.file_name, dpi=200)
            # On crée le nom de la photo équivalent au nom du pdf (sans l'extention .pdf) puis on ajoute .jpg
            img_name = '.'.join(self.file_name.split('.')[:-1]) + '.jpg'

            # On sauvegarde l'image du CV pour pouvoir extraire la photo
            images[0].save(photo_file + img_name, 'JPEG')
            # On lit l'image du PDF
            image = cv2.imread(photo_file + img_name)
            # On detecte le(s) visage(s) en ne gardant que ceux inférieux à 300px * 300px
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(image, minSize=(100, 100), maxSize=(300, 300))
            # print(faces)
            # print("[INFO] {0} visage(s) trouvé(s)!".format(len(faces)))
            # On sauvegarde le visage dans un fichier photo_pdf_file_name.jpg
            for (x, y, w, h) in faces:
                # Si le rectangle est trop petit on ne prend pas l'image
                if x > 40 and y > 40 and w > 40 and h > 40:
                    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    img_trouve = image[y - 50:y + h, x:x + w]
                    cv2.imwrite(photo_file + 'photo_' + img_name, img_trouve)
            # On supprime la photo du fichier PDF
            os.remove(photo_file + img_name)
            # On retourne le lien de la photo s'il existe une photo, sinon NULL
            self.informations['pic'] = photo_file + 'photo_' + img_name if len(faces) > 0 else 'NULL'
        except Exception:
            self.informations['pic'] = 'NULL'





def corr_name(first_name, last_name):
    """
    Fonction permettant de normaliser le prénom et le nom
    """
    first_name = unidecode.unidecode(first_name)
    last_name = unidecode.unidecode(last_name)

    first_name = first_name.replace('_',' ')
    last_name = last_name.replace('_',' ')

    first_name = first_name.replace('-',' ')
    last_name = last_name.replace('-',' ')

    listFirstName = first_name.split()
    listLastName = last_name.split()

    first_name = ''
    last_name = ''

    for p in listFirstName:
        pre = p.capitalize()
        first_name = first_name + ' ' + pre
    for p in listLastName:
        pre = p.upper()
        last_name = last_name + ' ' + pre
    first_name = first_name.strip()
    first_name = first_name.replace(' ','-')
    last_name = last_name.strip()
    last_name = last_name.replace(' ','-')

    return first_name,last_name

def parse_fr_address(adr):
    """
    Cette fonction permet de vérifier si une adresse existe grâce à une API.
    Si elle existe, elle découpe les segments de l'adresse dans plusieurs variables
    """


    #Avoir toutes les informations sur l'adresse
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    response = requests.get(api_url + urllib.parse.quote(adr.upper()) + '&limit=1')
    #Si la requête n'abouti pas, on l'a relance
    if response.status_code != 200:
        return {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}

    #print(response.json())

    house_number = 'NULL'
    street = 'NULL'
    type_of_street = 'NULL'
    post_code = 'NULL'
    city = 'NULL'
    country = 'NULL'
    continent = 'NULL'


    if response.json().get('features') != [] and adr != '':

        post_code = response.json().get('features','NULL')[0].get('properties','NULL').get('postcode','NULL')
        city = response.json().get('features','NULL')[0].get('properties','NULL').get('city','NULL')
        house_number = response.json().get('features','NULL')[0].get('properties','NULL').get('housenumber','NULL')
        street = response.json().get('features','NULL')[0].get('properties','NULL').get('street','NULL')

        if street != 'NULL' :
            if street.upper().split(' ', 1)[0] in ['AVENUE','RUE','BOULEVARD','QUAI','IMPASSE','PONT','PLACE','SQUARE','ALLEE','ALLEES','VOIE','MONTEE','ESPLANADE','ROUTE','VOIRIE','CITE','CHEMIN','PARVIS']:
                type_of_street = street.split(' ', 1)[0]
                street = street.split(' ', 1)[1]
        street = unidecode.unidecode(street)
        city = unidecode.unidecode(city)

        #Récupérer le pays avec la latitude et la longitude de la ville
        Latitude = str(response.json().get('features','NULL')[0].get('geometry','NULL').get('coordinates','NULL')[0])
        Longitude = str(response.json().get('features','NULL')[0].get('geometry','NULL').get('coordinates','NULL')[1])
        geolocator = Nominatim(user_agent="geoapiExercises")
        if Latitude != 'NULL' and Longitude != 'NULL':
            location = geolocator.reverse(Latitude+","+Longitude)
            url = 'https://geocode.xyz/' + Longitude + ',' + Latitude + '?json=1'
            response = requests.get(url)
            #Si la requête n'a pas abouti on l'a relance
            if response.status_code != 200:
                time.sleep(1)
                response = requests.get(url)
            #print(json.loads(response.text.encode('ascii', 'ignore').decode('utf-8')))
            response = json.loads(unidecode.unidecode(response.text))
            #print(response)
            country = response.get('country', 'NULL')
            try:
                #Récupérer le continent avec le pays
                country_code = pc.country_name_to_country_alpha2(country, cn_name_format="upper")
                country_continent_code = pc.country_alpha2_to_continent_code(country_code)
                continent = pc.convert_continent_code_to_continent_name(country_continent_code)
                country = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(country))
                continent = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(continent))
            except Exception:
                try:
                    #Récupérer le continent avec le pays
                    country_continent_code = pc.country_alpha2_to_continent_code(response.get('prov'))
                    continent = pc.convert_continent_code_to_continent_name(country_continent_code)
                    country = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(country))
                    continent = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(continent))
                except Exception:
                    pass

    dict_adress = dict()
    dict_adress['house_number'] = house_number.upper()
    dict_adress['type_of_street'] = type_of_street.upper()
    dict_adress['street'] = street.upper()
    dict_adress['post_code'] = post_code.upper()
    dict_adress['city'] = city.upper()
    dict_adress['country'] = country.upper()
    dict_adress['continent'] = continent.upper()
    dict_adress['number_null_val'] = count_null_value_dict(dict_adress)

    return dict_adress

def parse_strange_address(adr):

    #Url de l'API (adresse internationale)
    api_url = 'https://nominatim.openstreetmap.org/search/'

    #Requete vers l'API
    response = requests.get(api_url + urllib.parse.quote(adr.upper()) +'?format=json&addressdetails=1&limit=1')
    #On retente d'exécuter la requête
    if response.status_code != 200:
        time.sleep(1)
        response = requests.get(api_url + urllib.parse.quote(adr.upper()) +'?format=json&addressdetails=1&limit=1')
    if response.status_code == 200:
        #Formatage de la réponse
        response = json.loads(unidecode.unidecode(response.text))
        #Variable de retour
        house_number = 'NULL'
        street = 'NULL'
        type_of_street = 'NULL'
        post_code = 'NULL'
        city = 'NULL'
        country = 'NULL'
        continent = 'NULL'
        if response != []:
            post_code = response[0].get('address','NULL').get('postcode','NULL')
            city = response[0].get('address','NULL').get('city','NULL')
            if city == 'NULL' :
                city = response[0].get('address','NULL').get('town','NULL')
            house_number = response[0].get('address','NULL').get('house_number','NULL')
            street = response[0].get('address','NULL').get('road','NULL')
            if street != 'NULL' :
                if street.upper().split(' ', 1)[0] in ['AVENUE','RUE','BOULEVARD','QUAI','IMPASSE','PONT','PLACE','SQUARE','ALLEE','ALLEES','VOIE','MONTEE','ESPLANADE','ROUTE','VOIRIE','CITE','CHEMIN','PARVIS']:
                    type_of_street = street.split(' ', 1)[0]
                    street = street.split(' ', 1)[1]
            street = unidecode.unidecode(street)
            city = unidecode.unidecode(city)
            country = response[0].get('address','NULL').get('country','NULL')

            #Récupérer le pays avec la latitude et la longitude de la ville
            Latitude = response[0].get('lat','NULL')
            Longitude = response[0].get('lon','NULL')
            geolocator = Nominatim(user_agent="geoapiExercises")
            if Latitude != 'NULL' and Longitude != 'NULL':
                location = geolocator.reverse(Latitude+","+Longitude)
                url = 'https://geocode.xyz/' + Longitude + ',' + Latitude + '?json=1'
                response = requests.get(url)
                #Si la requête n'a pas abouti on l'a relance
                if response.status_code != 200:
                    time.sleep(1)
                    response = requests.get(url)
                #print(json.loads(response.text.encode('ascii', 'ignore').decode('utf-8')))
                response = json.loads(unidecode.unidecode(response.text))
                #print(response)
                if country == 'NULL':
                    country = response.get('country')
                try:
                    #Récupérer le continent avec le pays
                    country_code = pc.country_name_to_country_alpha2(country, cn_name_format="upper")
                    country_continent_code = pc.country_alpha2_to_continent_code(country_code)
                    continent = pc.convert_continent_code_to_continent_name(country_continent_code)
                    country = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(country))
                    continent = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(continent))
                except Exception:
                    try:
                        #Récupérer le continent avec le pays
                        country_continent_code = pc.country_alpha2_to_continent_code(response.get('prov'))
                        continent = pc.convert_continent_code_to_continent_name(country_continent_code)
                        country = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(country))
                        continent = unidecode.unidecode(GoogleTranslator(source='auto', target='fr').translate(continent))
                    except Exception:
                        pass

    dict_adress = dict()
    dict_adress['house_number'] = house_number.upper()
    dict_adress['type_of_street'] = type_of_street.upper()
    dict_adress['street'] = street.upper()
    dict_adress['post_code'] = post_code.upper()
    dict_adress['city'] = city.upper()
    dict_adress['country'] = country.upper()
    dict_adress['continent'] = continent.upper()
    dict_adress['number_null_val'] = count_null_value_dict(dict_adress)
    return dict_adress

def count_null_value_dict(dico):
    cpt = 0
    for val in dico.values():
        cpt += (val in ('NULL',None))
    return cpt

def extract_address(adr):
    """
    Fonction permettant d'optimiser une adresse soit avec l'API des adresses françaises, soit avec celle internationale
    On garde l'adresse qui a le moins de valeur NULL
    """
    #On appelle la fonction qui utilise l'API française
    addr1 = parse_fr_address(adr)
    if addr1['number_null_val'] <= 3:
        #On appelle la fonction qui utilise l'API international
        addr2 = parse_strange_address(adr)
        #Si on a moins de valeur null avec la seconde méthode
        if addr1['number_null_val'] > addr2['number_null_val']:
            addr1 = addr2

    return normalize_address(addr1)

def extract_address_with_totaltext(text):
    """der
    Fonction permettant d'extraire une adresse en explorant tout le texte et en cherchant toute les éventuelles adresses
    """
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    #On passe tout le texte dans l'API des adresses s'il detecte des adresses
    list_ville = []
    for i in range(0, ceil(len(text)/200)):
        txt = text[i*200:(i+1)*200]
        response = requests.get(api_url + urllib.parse.quote(txt) + '&limit=1')
        if response.json().get('features','NULL') != []:
            #Si la ville détecter est présente dans le texte
            if response.json().get('features','NULL')[0].get('properties','NULL').get('city','NULL').upper() in text.upper().split():
                #On l'ajoute à la liste des villes possiblement constitutive d'une adresse
                list_ville.append(response.json().get('features','NULL')[0].get('properties','NULL').get('city','NULL').upper())

    #On recupere toutes les positions des villes trouvées
    list_pos = []
    for ville in set(list_ville):
        cpt = 0
        for word in text.upper().split():
            if word == ville:
                list_pos.append(cpt)
            cpt = cpt + 1
    #Pour chaque position, on va récupérer les mots avant et le mot après
    #En effet dans une adresse la ville est très souvent dans la dernière ou avant dernière position
    list_ok = []
    for pos in list_pos:
        list_av_ap = text.upper().split()[pos-6:pos+1] if pos > 6 else text.upper().split()[0:pos+1]
        #Pour chaque groupe de mots ainsi obtenu, on verifie s'il match avec des composantes fréquemment présentes dans une adresse telles que le code postal ou le type de voie
        #S"il match c'est que c'est très certainement une adresse valide
        list_av_ap =  ' '.join(list_av_ap)
        if re.match('.*(?:AVENUE|RUE|BOULEVARD|QUAI|IMPASSE|PONT|PLACE|SQUARE|ALLEE|ALLEES|VOIE|MONTEE|ESPLANADE|ROUTE|VOIRIE|CITE|CHEMIN|PARVIS).*', list_av_ap) or re.match('.*(?:[0-9]{5}).*',list_av_ap):
            list_ok.append(list_av_ap)

    #Si un des elements respecte les deux pattern on le place devant (car il y a de grande chance que ce soit une adresse valide du candidat)
    for val in list_ok:
        if re.match('.*(?:AVENUE|RUE|BOULEVARD|QUAI|IMPASSE|PONT|PLACE|SQUARE|ALLEE|ALLEES|VOIE|MONTEE|ESPLANADE|ROUTE|VOIRIE|CITE|CHEMIN|PARVIS).*', list_av_ap) and re.match('.*(?:[0-9]{5}).*',list_av_ap):
            list_ok[0] = val

    #Pour cette adresse, on fait une reqûete vers l'API afin d'avoir les informations complémentaires
    return extract_address(list_ok[0]) if list_ok != [] else {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}

def extract_address_with_type_voie(text):
    """
    Fonction permettant d'extraire une adresse simplement avec le type de voie. En effet, c'est un élément important constitutif d'une adress
    """
    adr_res = dict()
    #Pour des soucis d'optimisation, on verifie d'abord qu'un des types de voie est présent
    regexp_type_voie = re.compile('.*(?:AVENUE|RUE|BOULEVARD|QUAI|IMPASSE|PONT|PLACE|SQUARE|ALLEE|ALLEES|VOIE|MONTEE|ESPLANADE|ROUTE|VOIRIE|CITE|CHEMIN|PARVIS).*')
    type_voie = re.findall(regexp_type_voie, text)
    if type_voie != []:
        cpt = 0
        list_pos = []
        #On recupère les positions de tous les types de voie que l'on trouve dans le texte
        for word in text.upper().split():
            if re.match('.*(?:AVENUE|RUE|BOULEVARD|QUAI|IMPASSE|PONT|PLACE|SQUARE|ALLEE|ALLEES|VOIE|MONTEE|ESPLANADE|ROUTE|VOIRIE|CITE|CHEMIN|PARVIS).*', word):
                list_pos.append(cpt)
            cpt = cpt + 1
        #Pour chaque position on va prendre un groupe de mot avant et un groupe de mot après (possiblement le reste de l'adresse)
        list_av_ap = [text.upper().split()[pos-2:pos+4] if pos > 2 else text.upper().split()[0:pos+4] for pos in list_pos]
        #Pour chacun des groupes de mots constitués, on vérifie et complète avec l'API afin de s'assurer que c'es réellement une adresse
        #Et on garde l'adresse la plus optimum (avec le moins d'attribut NULL)
        min_nul = 8
        for adresse in list_av_ap:
            adresse =  ' '.join(adresse)
            adr = extract_address(adresse)
            if adr.get('number_null_val') < min_nul:
                adr_res = adr
                min_nul = adr.get('number_null_val')

    #On renvoie l'adresse sous forme d'un disctionnaire
    #Ici le or est equivalent à adr_res if adr_res != {} else {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}
    #Mais c'est plus optimiser (on enleve une condition)
    return adr_res or {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}


def extract_address_with_regexp(text):
    """
    Fonction permettant d'extraire une adresse avec l'expression régulière des adresses
    """
    text = text.upper()
    #Expression reguliere d'une adresse
    regexp_adresse = re.compile('[0-9]+(?:BIS|TER)?,? ?(?:AVENUE|RUE|BOULEVARD|QUAI|IMPASSE|PONT|PLACE|SQUARE|ALLEE|ALLEES|VOIE|MONTEE|ESPLANADE|ROUTE|VOIRIE|CITE|CHEMIN|PARVIS) [A-Z ]+,? ?(?:[0-9]{5}| )? [A-Z\-]+')
    #On cherche toutes les adresses dans le texte
    adresses = re.findall(regexp_adresse, text.upper())
    min_nul = 8
    adr_res = dict()
    #Pour chaque adresse trouvée, on vérifie avec l'API si elle existe et on la complète le cas échéant
    for adr in adresses:
        adr = extract_address(adr)
        #Si l'adresse en cours a moins d'attribut NULL que les précédentes, on enregistre cette adresse
        if adr.get('number_null_val') < min_nul:
            adr_res = adr
            min_nul = adr.get('number_null_val')

    #On renvoie l'adresse sous forme de dictionnaire
    return adr_res or {'house_number':'NULL', 'type_of_street' : 'NULL', 'street':'NULL', 'post_code':'NULL','city':'NULL','country':'NULL','continent':'NULL','number_null_val':7}

def extract_address_from_text(text):
    """
    Fonction permettant d'extraire l'adresse d'un CV
    Les adresses sont souvent entrées de manière hétérogène, defois on a seulement la ville avec le CP, defois nous n'avons pas le CP,...
    On va donc utilisé les 3 méthodes d'extractions (avec expression régulière, avec type de voie et explorant tout le texte)
    Et nous allons prendre la manière qui renvoie les meilleurs résultats
    Comme la première méthode est moins énergivore (regexp) on l'appelle en premier et on regarde si on n'a pas le résulat optimum
    Sinon on essaye les autres.
    """
    #Appelle de la méthode avec expression regulière
    adr1 = extract_address_with_regexp(text)
    #Si on a la solution optimum (aucun attribut de l'adresse est 'NULL') on renvoie cette adresse
    if adr1.get('number_null_val') <= 4:
        return normalize_address(adr1)
    else:
        #Sinon on essaye la méthode (type voie)
        adr2 = extract_address_with_type_voie(text)
        #On regarde si on a une solution optimum
        if adr2.get('number_null_val') <= 4:
            return normalize_address(adr2)
        else:
            #Sinon on fait la 3
            adr3 = extract_address_with_totaltext(text)
            if adr3.get('number_null_val') <= 4:
                return normalize_address(adr3)
    #On prend l'adresse qui a le moins d'attribut NULL
    if adr1.get('number_null_val') <= adr2.get('number_null_val') and adr1.get('number_null_val') <= adr3.get('number_null_val'):
        return normalize_address(adr1)
    elif adr2.get('number_null_val') <= adr1.get('number_null_val') and adr2.get('number_null_val') <= adr3.get('number_null_val'):
        return normalize_address(adr2)
    else:
        return normalize_address(adr3)


def normalize_address(adr):
    adr['house_number'] = adr['house_number'].replace('B','BIS').replace('T','TER') 
    adr['street'] = adr['street'].replace('\'', ' ')
    adr['street'] = adr['street'].replace('"', ' ')
    adr['city'] = adr['city'].replace('\'cla', ' ')
    adr['city'] = adr['city'].replace('"', ' ')    
    adr['country'] = adr['country'].replace('\'', ' ')
    adr['country'] = adr['country'].replace('"', ' ')    
    adr['continent'] = adr['continent'].replace('\'', ' ')
    adr['continent'] = adr['continent'].replace('"', ' ')

    return adr