import locale
import re
from datetime import datetime
import unidecode

class BuildQuery:

    def __init__(self, pdf_name, informations, accepted):
        self.pdf_name = pdf_name
        self.informations = informations
        self.accepted = accepted

        self.sqlQuery = 'EXEC INSERT_('
        self.mongoDBQuery = '{'

        self.add_cv()
        self.add_address()
        self.add_candidate()
        self.add_driving_licences()
        self.add_degree()
        self.add_sites_socialNetwork()
        self.add_areas_of_interest()
        self.add_skills()
        self.add_languages()
        self.add_trainings()
        self.add_experiences()

        self.sqlQuery += ');\n'  
        self.mongoDBQuery += '}'  


    def add_cv(self):
        self.sqlQuery += '\'' + unidecode.unidecode(self.pdf_name) + '\','
        self.sqlQuery += 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('poste_recherche') + '\',' if self.informations.get('poste_recherche') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('type_poste') + '\',' if self.informations.get('type_poste') != 'NULL' else 'NULL,'
        dispo = convert_date(self.informations.get('disponibilite'))
        self.sqlQuery += 'NULL,' if dispo == 'NULL' else '\'' + dispo + '\','
        self.sqlQuery += '\'' + self.accepted + '\','
        self.sqlQuery += 'SYSDATE,'
        self.sqlQuery += '\'' + unidecode.unidecode(self.informations.get('pic')) + '\',' if self.informations.get('pic') != 'NULL' else 'NULL,'

        self.mongoDBQuery += '"cv" : {'
        self.mongoDBQuery += '"pdf_name" : "' + self.pdf_name + '",'
        self.mongoDBQuery += '"description" : null,'
        self.mongoDBQuery += '"poste_recherche" : "' + self.informations.get('poste_recherche') + '",' if self.informations.get('poste_recherche') != 'NULL' else '"poste_recherche" : null,'
        self.mongoDBQuery += '"type_poste" : "' + self.informations.get('type_poste') + '",' if self.informations.get('type_poste') != 'NULL' else '"type_poste" : null,'
        #Dispo à faire
        self.mongoDBQuery += '"accepted" : "' + self.accepted + '",'
        #Date de transmission à faire
        self.mongoDBQuery += '"pic" : "' + self.informations.get('pic') + '" },' if self.informations.get('pic') != 'NULL' else '"pic" : null },'


    def add_address(self):
        self.sqlQuery += '\'' + self.informations.get('address').get('house_number') + '\',' if self.informations.get('address').get('house_number') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('address').get('type_of_street') + '\',' if self.informations.get('address').get('type_of_street') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('address').get('street') + '\',' if self.informations.get('address').get('street') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('address').get('post_code') + '\',' if self.informations.get('address').get('post_code') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('address').get('city') + '\',' if self.informations.get('address').get('city') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('address').get('country') + '\',' if self.informations.get('address').get('country') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('address').get('continent') + '\',' if self.informations.get('address').get('continent') != 'NULL' else 'NULL,'
    
        self.mongoDBQuery += '"address" : {'
        self.mongoDBQuery += '"house_number" : "' + self.informations.get('address').get('house_number') + '",' if self.informations.get('address').get('house_number') != 'NULL' else '"house_number" : null,'
        self.mongoDBQuery += '"type_of_street" : "' + self.informations.get('address').get('type_of_street') + '",' if self.informations.get('address').get('type_of_street') != 'NULL' else '"type_of_street" : null,'
        self.mongoDBQuery += '"street" : "' + self.informations.get('address').get('street') + '",' if self.informations.get('address').get('street') != 'NULL' else '"street" : null,'
        self.mongoDBQuery += '"post_code" : "' + self.informations.get('address').get('post_code') + '",' if self.informations.get('address').get('post_code') != 'NULL' else '"post_code" : null,'
        self.mongoDBQuery += '"city" : "' + self.informations.get('address').get('city') + '",' if self.informations.get('address').get('city') != 'NULL' else '"city" : null,'
        self.mongoDBQuery += '"country" : "' + self.informations.get('address').get('country') + '",' if self.informations.get('address').get('country') != 'NULL' else '"country" : null,'
        self.mongoDBQuery += '"continent" : "' + self.informations.get('address').get('continent') + '" },' if self.informations.get('address').get('continent') != 'NULL' else '"continent" : null },'

    def add_candidate(self):
        self.sqlQuery += '\'' + self.informations.get('last_name') + '\',' if self.informations.get('last_name') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('first_name') + '\',' if self.informations.get('first_name') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('gender') + '\',' if self.informations.get('gender') != 'NULL' else 'NULL,'
        self.sqlQuery += self.informations.get('age') + ','
        self.sqlQuery += '\'' + self.informations.get('birth_date') + '\',' if self.informations.get('birth_date') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('mail') + '\',' if self.informations.get('mail') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('nationality') + '\',' if self.informations.get('nationality') != 'NULL' else 'NULL,'
        self.sqlQuery += '\'' + self.informations.get('phone') + '\',' if self.informations.get('phone') != 'NULL' else 'NULL,'

        self.mongoDBQuery += '"identity" : {'
        self.mongoDBQuery += '"last_name" : "' + self.informations.get('last_name') + '",' if self.informations.get('last_name') != 'NULL' else '"last_name" : null,'
        self.mongoDBQuery += '"first_name" : "' + self.informations.get('first_name') + '",' if self.informations.get('first_name') != 'NULL' else '"first_name" : null,'
        self.mongoDBQuery += '"gender" : "' + self.informations.get('gender') + '",' if self.informations.get('gender') != 'NULL' else '"gender" : null,'
        self.mongoDBQuery += '"age" : ' + self.informations.get('age') + ',' if self.informations.get('age') != 'NULL' else '"age" : null,'
        self.mongoDBQuery += '"birth_date" : "' + self.informations.get('birth_date') + '",' if self.informations.get('birth_date') != 'NULL' else '"birth_date" : null,'
        self.mongoDBQuery += '"mail" : "' + self.informations.get('mail') + '",' if self.informations.get('mail') != 'NULL' else '"mail" : null,'
        self.mongoDBQuery += '"nationality" : "' + self.informations.get('nationality') + '",' if self.informations.get('nationality') != 'NULL' else '"nationality" : null,'
        self.mongoDBQuery += '"phone" : "' + self.informations.get('phone') + '"},' if self.informations.get('phone') != 'NULL' else '"phone" : null },'


    def add_driving_licences(self):
        if self.informations.get('driving_licences') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"driving_licences" : ['
            for driving_licence in self.informations.get('driving_licences'):
                self.sqlQuery += driving_licence + ','
                self.mongoDBQuery += '{"driving_licence" : "' + driving_licence + '"},'
            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]
            self.sqlQuery += ']\','
            self.mongoDBQuery += '],'
        else:
            self.sqlQuery += 'NULL,'
            self.mongoDBQuery += '"driving_licences" : null,'

    def add_degree(self):
        self.sqlQuery += 'NULL,'
        self.mongoDBQuery += '"degrees" : null,'

    def add_sites_socialNetwork(self):
        if self.informations.get('sites_socialNetwork') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"sites_socialNetwork" : ['
            for site_socialNetwork in self.informations.get('sites_socialNetwork'):
                self.sqlQuery += site_socialNetwork + ','
                self.mongoDBQuery += '{"site_socialNetwork" : "' + site_socialNetwork + '"},'
            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]
            self.sqlQuery += ']\','
            self.mongoDBQuery += '],'
        else:
            self.sqlQuery += 'NULL,'
            self.mongoDBQuery += '"sites_socialNetwork" : null,'
    
    def add_areas_of_interest(self):
        if self.informations.get('areas_of_interest') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"areas_of_interest" : ['
            for areas_of_interest in self.informations.get('areas_of_interest'):
                self.sqlQuery += areas_of_interest + ','
                self.mongoDBQuery += '{"area_of_interest" : "' + areas_of_interest + '"},'
            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]
            self.sqlQuery += ']\','
            self.mongoDBQuery += '],'
        else:
            self.sqlQuery += 'NULL,'
            self.mongoDBQuery += '"areas_of_interest" : null,'
     
    def add_skills(self):
        if self.informations.get('skills') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"skills" : ['

            for skill in self.informations.get('skills'):
                cat = find_cat_cpt(skill)
                self.sqlQuery += '(' + skill + ';' + cat + '),'
                self.mongoDBQuery += '{ "skill" : "' + skill + '", "category" : '
                self.mongoDBQuery += 'null },' if cat == 'NULL' else '"' + cat + '"},'

            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]

            self.sqlQuery += ']\','
            self.mongoDBQuery += '],'

        else:
            self.sqlQuery += 'NULL,'
            self.mongoDBQuery += '"skills" : null,'

    def add_languages(self):
        if self.informations.get('languages') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"languages" : ['
            for langue, niveau in self.informations.get('languages'):
                self.sqlQuery += '(' + langue + ';' + niveau + '),'
                self.mongoDBQuery += '{ "language" : "' + langue + '", "level" : '
                self.mongoDBQuery += 'null },' if niveau == 'NULL' else '"' + niveau + '"},'

            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]

            self.sqlQuery += ']\','
            self.mongoDBQuery += '],'

        else:
            self.sqlQuery += 'NULL,'
            self.mongoDBQuery += '"languages" : null,'


    def add_trainings(self):
        if self.informations.get('trainings') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"trainings" : ['

            for niveau, specialite, etablissementScolaire, dateDeb, dateFin, adresseEtaSco, tel_ecole in self.informations.get('trainings'):
                startDate = convert_date(dateDeb)
                endDate = convert_date(dateFin)

                self.sqlQuery += '(' + niveau + ';' + specialite + ';' + etablissementScolaire + ';' + startDate + ';' + endDate + ';'
                self.sqlQuery += adresseEtaSco.get('house_number','NULL') + ';' + adresseEtaSco.get('type_of_street','NULL') + ';' + adresseEtaSco.get('street','NULL') + ';'
                self.sqlQuery += adresseEtaSco.get('post_code','NULL') + ';' + adresseEtaSco.get('city','NULL') + ';' + adresseEtaSco.get('country','NULL') + ';' + adresseEtaSco.get('continent','NULL') + ';' 
                self.sqlQuery += tel_ecole 
                self.sqlQuery += '),' 

                self.mongoDBQuery += '{"level" : "' + niveau + '",' if niveau != 'NULL' else '{"level" : null,'
                self.mongoDBQuery += '"speciality" : "' + specialite + '",' if specialite != 'NULL' else '"speciality" : null,'
                self.mongoDBQuery += '"school_establishment" : "' + etablissementScolaire + '",' if etablissementScolaire != 'NULL' else '"school_establishment" : null,'
                self.mongoDBQuery += '"start_date" : "' + startDate + '",' if startDate != 'NULL' else '"start_date" : null,'
                self.mongoDBQuery += '"end_date" : "' + endDate + '",' if endDate != 'NULL' else '"end_date" : null,'
                self.mongoDBQuery += '"school_establishment_address" : {'
                self.mongoDBQuery += '"house_number" : "' + adresseEtaSco.get('house_number') + '",' if adresseEtaSco.get('house_number') != 'NULL' else '"house_number" : null,'
                self.mongoDBQuery += '"type_of_street" : "' + adresseEtaSco.get('type_of_street') + '",' if adresseEtaSco.get('type_of_street') != 'NULL' else '"type_of_street" : null,'
                self.mongoDBQuery += '"street" : "' + adresseEtaSco.get('street') + '",' if adresseEtaSco.get('street') != 'NULL' else '"street" : null,'
                self.mongoDBQuery += '"post_code" : "' + adresseEtaSco.get('post_code') + '",' if adresseEtaSco.get('post_code') != 'NULL' else '"post_code" : null,'
                self.mongoDBQuery += '"city" : "' + adresseEtaSco.get('city') + '",' if adresseEtaSco.get('city') != 'NULL' else '"city" : null,'
                self.mongoDBQuery += '"country" : "' + adresseEtaSco.get('country') + '",' if adresseEtaSco.get('country') != 'NULL' else '"country" : null,'
                self.mongoDBQuery += '"continent" : "' + adresseEtaSco.get('continent') + '"}' if adresseEtaSco.get('continent') != 'NULL' else '"continent" : null}'
                self.mongoDBQuery += '},' 


            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]

            self.sqlQuery += ']\','
            self.mongoDBQuery += '],'

        else:
            self.sqlQuery += 'NULL,'
            self.mongoDBQuery += '"trainings" : null,'

    def add_experiences(self):
        if self.informations.get('experiences') != 'NULL':
            self.sqlQuery += '\'['
            self.mongoDBQuery += '"experiences" : ['

            for poste, typeContrat, entreprise, dateDeb, dateFin, descriptionExp, adrExp in self.informations.get('experiences'):
                startDate = convert_date(dateDeb)
                endDate = convert_date(dateFin)

                self.sqlQuery += '(' + poste + ';' + typeContrat + ';' + entreprise + ';' + startDate + ';' + endDate + ';' + descriptionExp + ';'
                self.sqlQuery += adrExp.get('house_number','NULL') + ';' + adrExp.get('type_of_street','NULL') + ';' + adrExp.get('street','NULL') + ';'
                self.sqlQuery += adrExp.get('post_code','NULL') + ';' + adrExp.get('city','NULL') + ';' + adrExp.get('country','NULL') + ';' + adrExp.get('continent','NULL') 
                self.sqlQuery += '),' 

                self.mongoDBQuery += '{"poste" : "' + poste + '",' if poste != 'NULL' else '{"poste" : null,'
                self.mongoDBQuery += '"typeContrat" : "' + typeContrat + '",' if typeContrat != 'NULL' else '"typeContrat" : null,'
                self.mongoDBQuery += '"entreprise" : "' + entreprise + '",' if entreprise != 'NULL' else '"entreprise" : null,'
                self.mongoDBQuery += '"start_date" : "' + startDate + '",' if startDate != 'NULL' else '"start_date" : null,'
                self.mongoDBQuery += '"end_date" : "' + endDate + '",' if endDate != 'NULL' else '"end_date" : null,'
                self.mongoDBQuery += '"descriptifExp" : "' + descriptionExp + '",' if descriptionExp != 'NULL' else '"descriptifExp" : null,'
                self.mongoDBQuery += '"entreprise_address" : {'
                self.mongoDBQuery += '"house_number" : "' + adrExp.get('house_number') + '",' if adrExp.get('house_number') != 'NULL' else '"house_number" : null,'
                self.mongoDBQuery += '"type_of_street" : "' + adrExp.get('type_of_street') + '",' if adrExp.get('type_of_street') != 'NULL' else '"type_of_street" : null,'
                self.mongoDBQuery += '"street" : "' + adrExp.get('street') + '",' if adrExp.get('street') != 'NULL' else '"street" : null,'
                self.mongoDBQuery += '"post_code" : "' + adrExp.get('post_code') + '",' if adrExp.get('post_code') != 'NULL' else '"post_code" : null,'
                self.mongoDBQuery += '"city" : "' + adrExp.get('city') + '",' if adrExp.get('city') != 'NULL' else '"city" : null,'
                self.mongoDBQuery += '"country" : "' + adrExp.get('country') + '",' if adrExp.get('country') != 'NULL' else '"country" : null,'
                self.mongoDBQuery += '"continent" : "' + adrExp.get('continent') + '"}' if adrExp.get('continent') != 'NULL' else '"continent" : null}'
                self.mongoDBQuery += '},' 

            self.sqlQuery = self.sqlQuery[:-1]
            self.mongoDBQuery = self.mongoDBQuery[:-1]

            self.sqlQuery += ']\''
            self.mongoDBQuery += ']'

        else:
            self.sqlQuery += 'NULL'
            self.mongoDBQuery += '"experiences" : null'


def find_cat_cpt(cpt):
    cat_bdd = ['APPRENTISSAGE','SASSOFTWARE','SASVIYA','BUSINESS OBJECTS','BUSINESSOBJECTS','SQL','ORACLE','JAVA/JEE','SQL3','MYSQL','DATA WAREHOUSE','PLSQL','PL/SQL','NOSQL','MONGODB','DATABASE','DATA INTEGRATION','DATAQUALITY','SQLSERVER','SPRINGBOOT','SPRINGDATA','SPRINGSECURITY','BUSINESS INTELLIGENCE','TABLEAU','REPRESENTATION GRAPHIQUE DE DONNEES STATISTIQUES','MEETUP TAFTERWORKS'] 
    cat_comp = ['INTERNET DES OBJETS',' IOT']
    cat_web = ['DEVELOPPEMENT DE CONTENU','PHPMYADMIN','JAVASCRIPT','PHP','J2E','HTML','CSS','XML','PHP5','SYMFONY','JS','CSS3','JAVASCRIPT'] 
    cat_lang = ['C','SAS','PYTHON','JAVA','R','C++','C#','MATLAB','OCAML','UML','HASKELL','SCALA'] 
    cat_crea = ['PHOTOSHOP','PHOTOGRAPHIE','VIDEOGRAPHIE','CREATIVITE'] 
    cat_se = ['LINUX','MACOS','WINDOWS','UBUNTU','DEBIAN']
    cat_outil = ['NETBEANS','ANDROIDSTUDIO','CODE:BLOCKS','VISUALSTUDIO','STVISUALDEVELOP','JUPYTER','ANACONDA','SPYDER','TALEND','JIRA','TRELLO','JUPYTER-NOTEBOOK','SASSTUDIO','EXCEL','KNIME','COLAB','MICROSOFTOFFICEEXCEL','PANDAS','NUMPY','SCIKIT-LEARN','SCIKIT-FUZZY','HADOOP','SPARK','RSTUDIO','JUPYTERNOTEBOOK','ECLIPSE','STUDIOCODE','GIT','SASVIYA','METHODEAGILE','GITHUB','POWERPOINT','APACHEKAKFA','DOMOTIQUE','WORD','EXCEL','MICROSOFT ASP.NET MVC.WEB API']
    cat_softSkill = ['BENEVOLE','ANALYSE DES CONCURRENTS','COMMUNICATION','RESEAUTAGE','ESPRIT D EQUIPE','TRAVAIL AUTONOME','CAPACITE A TRAVAILLER SOUS PRESSION','GESTION DU TEMPS','RECHERCHE DE MARCHE','FACILITE DINTEGRATION','DIPLOMATIE','TRAVAILLEUR SOCIAL AGREE','AUTODIDAXIE','ORGANISE','APPLIQUE','DYNAMIQUE','AGILE','ASSOCIATION','ACTION SOCIALE','SENS DE RESPONSABILITÉS','TRAVAIL EN EQUIPE','FLEXIBLE','COMMUNICATION','ADAPTATION FACILE','CAPACITE DADAPTATION','CURIEUX','TRAVAIL EN EQUIPE','ADAPTABLE','COMMUNICANT','SERIEUX','MOTIVE','RIGOUREUX','BONNE APPROCHE DES CLIENTS','SENS  NEGOCIATION','COMPETENCES RELATIONNELLES','ESPRIT DEQUIPE','TRAVAIL EN EQUIPE',' RESPECT DES DELAIS','ETABLIR UN CAHIER DES CHARGES','CAPACITE À SORGANISER','DETERMINE','CURIEUSE','RIGOUREUSE','AVENTURES','RELATIONNEL','ADAPTABILITE','RIGUEUR','AUTONOMIE','TRAVAIL EN GROUPE','TRAVAIL SOUS PRESSION','ECLIPSE','DYNAMIC','DYNAMIQUE','COLLABORATIVE WORK','COLLABORATIF','PONCTUALITE','TRAVAIL EN GROUPE','GESTION DE TEMPS','ESPRIT D’ANALYSE'] 
    if cpt.upper() in cat_bdd:
        return 'BASE DE DONNEES'
    elif cpt.upper() in cat_lang:
        return 'LANGAGE DE PROGRAMMATION'
    elif cpt.upper() in cat_comp:
        return 'ELECTRONIQUE'
    elif cpt.upper() in cat_crea:
        return 'CREATIVITE'
    elif cpt.upper() in cat_web:
        return 'WEB'
    elif cpt.upper() in cat_se:
        return 'SYSTEME EXPLOITATION' 
    elif cpt.upper() in cat_outil:
        return 'OUTILS'
    elif cpt.upper() in cat_softSkill:
        return 'SOFTSKILLS'  
    else:
        return 'NULL'

def convert_date(date):
    """
    Fonction permettant de convertir les dates dans le format souhaité
    @params:
        date -Require : La date
    @return 
        date : La date dans le bon format
    """
    #On se met en français
    dateNorm = date.lower()
    if re.match('(janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre) ([0-9]{4})',dateNorm):
        if re.match('decembre [0-9]+',dateNorm):
            an = re.sub('decembre ([0-9]+)', '\g<1>',dateNorm)
            dateNorm = 'décembre ' + an
        elif re.match('fevrier [0-9]+',dateNorm):
            an = re.sub('fevrier ([0-9]+)', '\g<1>',dateNorm)
            dateNorm = 'février ' + an
        elif re.match('aout [0-9]+',dateNorm):
            an = re.sub('aout ([0-9]+)', '\g<1>',dateNorm)
            dateNorm = 'août ' + an
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        #On récupère convertie la date en format numrique en supprimant les apostrophes en début et fin de date
        dateConvert = datetime.strptime(dateNorm ,'%B %Y')
        #On crée la date
        date = str(dateConvert.day) + '/' + str(dateConvert.month) + '/' + str(dateConvert.year)
    elif re.match('([0-9]{4})',dateNorm):
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        #On récupère convertie la date en format numrique en supprimant les apostrophes en début et fin de date
        dateConvert = datetime.strptime(dateNorm ,'%Y')
        #On crée la date
        date = str(dateConvert.day) + '/' + str(dateConvert.month) + '/' + str(dateConvert.year)
    else:
        date = 'NULL'

    date = date.strip().upper() 
    return date