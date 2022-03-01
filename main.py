from deep_translator import GoogleTranslator
from frontend.server import app
from starlette.staticfiles import StaticFiles
from Cv_parser import CvParser
from buildQuery import BuildQuery

from os import listdir
from os.path import isfile, join

import unidecode
import re
from progress.bar import ShadyBar
import fitz



def loadURL(repertoire):
    """
    Fonction permettant d'extraire une liste de fichier d'un repertoire
    @params:
        repertoire  - Required : Repertoire depuis lequel on veut extraire les fichiers
    """
    return [f for f in listdir(repertoire) if isfile(join(repertoire, f))]

def extract_text_pdf(storage_file, pdf_files):
    """
    Fonction permettant de gerer lextraction dinformation des PDF
    @params:
        storage_file    - Required : Le fichier de stockage des PDF
        pdf_files       - Required : La liste des fichiers PDF

    """
    #Dictionnaire {'Etablissement':[adresse, tel]}
    #Il va permettre doptimiser le programme en stockant les adresses et numero de telephone des differents etablissements (scolaires ou entreprises) afin d'éviter l'appel repete
    # à l'API qui est très couteux en temps 
    dict_etablissements_address = dict()

    #Fichier d'ecriture des requetes SQL
    sqlQueryfile = './G1_InsertDon_CV.sql'
    mongoDBQueryFile = './G1_InsertDonMongoDB_CV.json'

    #Ouverture des fichier 
    out_SQLfile = open(sqlQueryfile, 'a')
    out_MongoDBfile = open(mongoDBQueryFile, 'a')

    with ShadyBar('Extraction en cours...', max=len(pdf_files),  suffix = '%(percent)d%% [ %(index)d/%(max)d - %(elapsed)ds ]') as bar:
        for index, pdf_file in enumerate(pdf_files):

            #Ouverture du CV
            doc = fitz.open(storage_file + pdf_file)
            #Pour chaque page du CV, on recupère tout le texte
            text = ""
            for page in doc:
                text += str(page.getText())
            tx = " ".join(text.split('\n'))
            #On traduit le texte en francais par ex: United Kingdom -> Royaume-Unis)
            tx = GoogleTranslator(source='auto', target='fr').translate(tx)
            tx = re.sub(r'(?<=\b[a-zA-ZÉ]) (?=[a-zA-Z]\b)', '', tx)
            tx = re.sub(r'(?<=\b[0-9]) (?=[0-9]\b)', '', tx)
            tx = unidecode.unidecode(tx.replace('  ',' ').replace('\'',' '))
            #Extraction des informations des CV
            dict_informations = CvParser(storage_file,pdf_file,tx, dict_etablissements_address)
            print(dict_informations.informations)

            #Variable pour savoir si un CV est accepté, refusé ou dans le statut inconnu           
            if storage_file == './CV_ACCEPTE/':
                accepted = 'ACCEPTE' 
            elif storage_file == './CV_REFUSE/' :
                accepted = 'REFUSE'
            else:
                accepted = 'INCONNU'
            #Création de la requete SQL
            insert_query = BuildQuery(pdf_file, dict_informations.informations, accepted)

            #Mise à jour du dictionnaire etablissements/adresses
            dict_etablissements_address = dict_informations.dict_etablissements_address
            
            #Ecriture des requêtes d'insertions dans les fichiers
            out_SQLfile.write(insert_query.sqlQuery)
            out_MongoDBfile.write(insert_query.mongoDBQuery)
            if not (storage_file == './CV_INCONNU/' and index == len(pdf_files) - 1):
                out_MongoDBfile.write(',')

            #Incrementer barre de progression
            bar.next()
    #Fermeture des fichier
    out_SQLfile.close()
    out_MongoDBfile.close()

def main():
    out_MongoDBfile = open('./G1_InsertDonMongoDB_CV.json', 'a')
    out_MongoDBfile.write('[')
    out_MongoDBfile.close()

    #Fichier de stockage des PDF que l'on veut traiter
    for storage_file in(['./CV_INCONNU/','./CV_ACCEPTE/', './CV_REFUSE/', './CV_INCONNU/']):

      for storage_file in ['./CV_TEST/']:
        #Chargement des PDF
        list_pdf_files = loadURL(storage_file)
        #Extraction de l'informations des PDF et création des requetes SQL et MongoDB dans les fichiers
        if list_pdf_files: 
            print('Traitement des CV de', storage_file, 'en cours...')
            extract_text_pdf(storage_file, list_pdf_files)
            print('Extraction des PDF de', storage_file, 'terminée.')
        else:
            print('Le dossier', storage_file, 'est vide.')

    out_MongoDBfile = open('./G1_InsertDonMongoDB_CV.json', 'a')
    out_MongoDBfile.write(']')
    out_MongoDBfile.close()

    print('Les fichiers d\'insertions SQL et MongoDB ont été créés.')

if __name__ == '__main__':
    """import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()"""
    main()
    """profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
    stats.print_stats('extract_address_with_type_voie')"""

