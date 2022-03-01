
Notes importantes : 

Avant toute chose, assuez-vous que les dossiers suivants soient correctement remplis

- CV_ACCEPTE 	: Dossier qui permet de stocker les CV au format PDF qui ont été acceptés;
	- Mettre dans ce dossier les CV acceptés
- CV_REFUSE 	: Dossier qui permet de stocker les CV au format PDF qui n'ont pas été acceptés;
	- Mettre dans ce dossier les CV non acceptés
- CV_INCONNU 	: Dossier qui permet de stocker les CV au format PDF que nous voulons prétraiter avec du Machine Learning pour faire un premier classement;
	- Mettre dans ce dossier les CV dont on souhaite que l'algorithme de Machine Learning, nous conseille sur la classe
- Photo_CV	: Dossier qui stocke les photos extraites automatiquement par le script avec un detection des visage.
	- Ne rien mettre dans ce dossier, le scipt s'en charge

Attention : Vérifier qu'un CV donné ne se trouve pas dans plusieurs dossiers. Cela n'aura aucune incidence sur le fonctionnement du projet mais peut créer du sur-apprentissage pour le Machine Learning.

Pour exécuter ce Projet.

Suivez les étapes ci-dessous : 

Etape 1) Python 

- Ouvrez un terminal :
	- Lancez : Invite de commandes (ou CMD) sur WINDOWS (ou Terminal sur Mac et Linux)
	- Placez vous dans le dossier de ce projet (cd ..'lien avant le dossier'../Projet_CV_V2)
	- Exécuter la commande : pip install -r requirements.txt (Python 2) ou pip3 install -r requirements.txt (Python 3). 
		- requirements.txt contient toutes les bibliothèques qui sont nécessaire au projet et la commande permet de toutes les installer ;
		- (optionnelle) S’il manque des fichiers ou que l’exécution s’est mal passée, exécutez une par une les instructions suivantes (Rmq : certaines bibliothèques peuvent manquées): 
 			- pip install numpy
    			- pip install unidecode
    			- pip install pandas
    			- pip uninstall pymupdf
    			- pip install strsimpy
     			- pip install opencv-python
    			- pip install pdf2image
    			- pip install deep_translator
           		- pip install geopy
        		- pip install pycountry_convert
        		- pip install frontend
        		- pip install fitz
        		- pip install progress


- Exécutez le code python du fichier main.py avec la commande : python main.py (ou python3 selon votre version)
	- En cas d'erreur, vérifier qu'il ne vous manque pas une bibliothèque, qui n'est pas mentionnée au-dessus

- Des barres de chargement indiquent l'avancée du processus
	- Attendre la fin d'exécution de script python (quelques minutes)

L'exécution de ce scipt python a permit d'extraire les informations des PDF et de créer les requêtes d'insertions SQL et un fichier JSON pour MongoDB par rapport à ces PDF.


Etape 2) Oracle (SQL) / MongoDB

- SQL :
	- Exécuter le fichier G1_CreatDon_CV.sql (@G1_CreatDon_CV.sql sur SQL*PLUS ou copier/coller sur d'autres environnements)
	- Exécuter le fichier G1_InsertDon_CV.sql (@G1_InsertDon_CV.sql sur SQL*PLUS ou copier/coller sur d'autres environnements)
	- Exécuter le fichier G1_ManipDon_CV.sql (@G1_ManipDon_CV.sql sur SQL*PLUS ou copier/coller sur d'autres environnements)
- MongoDB :
	- Importer le fichier JSON G1_InsertDonMongoDB_CV.json 
		- dans MongoDB directement;
		- (ou avec la commande : "mongoimport --db=cvs --collection=cv --file=G1_InsertDonMongoDB_CV.json .json").

Etape 3) Machine Learning (Optionnelle)

Cette phase permet d'apprendre sur les CV des dossiers CV_ACCPETE et CV_REFUSE dont la classe (ACCEPTE ou REFUSE) est déjà connue avec du Machine Learning afin de prédire la classe des CV encore non classé du dossier CV_INCONNU.
Ce traitement est un pré-traitement. L'algorithme conseille simplement l'utilisateur en fonction de ce qu'il a déjà rencontré.

- Exécuter le fichier SQL : G1_MachineLearning_CV.sql (@G1_MachineLearning_CV.sql sur SQL*PLUS ou copier/coller sur d'autres environnements)
- Exécuter le fichier Python : machine_learning.py (python machine_learning.py ou python3 machine_learning.py)
- Un affichage affiche les classes prédites pour chaque CV de CV_INCONNU et score l'algorithme de prédiction

Etape 4) Data Integration Talend

Cette partie permet d'intégrer les données de gestionnaires de bases de données hétérogènes et de les fusionner en une seule base via Talend

- Importer les Jobs Talend fournis dans l'archive ProjetZip.zip dans Talend.

Etape 5) Visualisation Tableau

Cette partie permet de visualiser, avec Tableau, les données qui ont été précédemment fusionnées avec Talend

- Importer dans Tableau VilleBDA.twbx et ProjetBDA.twbx afin de visualiser les données dans tableau.


