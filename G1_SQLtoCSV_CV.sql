SET SERVEROUTPUT ON;

SET echo off
SET termout off
SET feedback off
SET pages 0
SET LINES 0
SET pagesize 0
SET heading OFF
SET pause off
SET colsep ';'
set term off
set trimspool on

spool './CSV_Table/candidats.txt' 
SELECT 'IDCAN;IDADR;NOMCAN;PRENOMCAN;SEXE;AGE;DATENAISSANCE;MAILCAN;NATIONALITE;TELCAN' FROM DUAL;
SELECT 	CASE WHEN IDADR IS NOT NULL 
		THEN 'CAN_' || IDCAN || ';ADR_' || IDADR || ';' || NOMCAN || ';' || PRENOMCAN || ';' || SEXE || ';' || AGE || ';' || DATENAISSANCE || ';' || MAILCAN || ';' || NATIONALITE || ';' || TELCAN 
		ELSE 'CAN_' || IDCAN || ';' || IDADR || ';' || NOMCAN || ';' || PRENOMCAN || ';' || SEXE || ';' || AGE || ';' || DATENAISSANCE || ';' || MAILCAN || ';' || NATIONALITE || ';' || TELCAN
		END
FROM CANDIDATS;
spool off

spool './CSV_Table/cv.txt' 
SELECT 'IDCV;IDCAN;NOMCV;DESCRIPTIFCV;POSTERECHERCHER;TYPEPOSTE;DISPONIBILITE;ADMIS;DATETRANSMISSION;PHOTO' FROM DUAL;
SELECT 	CASE WHEN IDCAN IS NOT NULL 
		THEN 'CV_' || IDCV || ';CAN_' || IDCAN || ';' || NOMCV || ';' || DESCRIPTIFCV || ';' || POSTERECHERCHER || ';' || TYPEPOSTE || ';' || DISPONIBILITE || ';' || ADMIS || ';' || DATETRANSMISSION || ';' || PHOTO 
		ELSE 'CV_' || IDCV || ';' || IDCAN || ';' || NOMCV || ';' || DESCRIPTIFCV || ';' || POSTERECHERCHER || ';' || TYPEPOSTE || ';' || DISPONIBILITE || ';' || ADMIS || ';' || DATETRANSMISSION || ';' || PHOTO 
		END
FROM CV;
spool off


spool './CSV_Table/adresses.txt' 
SELECT 'IDADR;NUMADR;LOCALITEADR;NOMRUEADR;CPADR;VILLEADR;PAYSADR;CONTINENTADR' FROM DUAL;
SELECT 'ADR_' || IDADR || ';' || NUMADR || ';' || LOCALITEADR || ';' || NOMRUEADR || ';' || CPADR || ';' || VILLEADR || ';' || PAYSADR || ';' || CONTINENTADR FROM ADRESSES;
spool off

spool './CSV_Table/competences.txt' 
SELECT 'NOMCPT;NOMCATEGORIE' FROM DUAL;
SELECT NOMCPT || ';' || NOMCATEGORIE FROM COMPETENCES;
spool off

spool './CSV_Table/categorie_cpt.txt' 
SELECT 'NOMCATEGORIE' FROM DUAL;
SELECT NOMCATEGORIE FROM CATEGORIE_CPT;
spool off

spool './CSV_Table/permis.txt' 
SELECT 'NOMPERM' FROM DUAL;
SELECT NOMPERM FROM PERMIS;
spool off

spool './CSV_Table/centres_interets.txt' 
SELECT 'NOMCTRINT' FROM DUAL;
SELECT NOMCTRINT FROM CENTREINTERET;
spool off

spool './CSV_Table/sites_reseaux.txt' 
SELECT 'IDSITERES;IDCAN;LIEN' FROM DUAL;
SELECT 'SITRES_' || IDSITERES || ';CAN_' || IDCAN || ';' || LIEN FROM SITES_RESEAUX;
spool off

spool './CSV_Table/langues.txt' 
SELECT 'NOMLANGUE' FROM DUAL;
SELECT NOMLANGUE FROM LANGUES;
spool off

spool './CSV_Table/entreprises.txt' 
SELECT 'IDENT;IDADR;NOMENT;MAILENT;TELENT' FROM DUAL;
SELECT 	CASE WHEN IDADR IS NOT NULL 
		THEN 'ENT_' || IDENT || ';ADR_' || IDADR || ';' || NOMENT || ';' || MAILENT || ';' || TELENT
		ELSE 'ENT_' || IDENT || ';' || IDADR || ';' || NOMENT || ';' || MAILENT || ';' || TELENT
		END
FROM ENTREPRISES;
spool off

spool './CSV_Table/etablissements_scolaires.txt' 
SELECT 'IDETASCO;IDADR;NOMETASCO;TELETASCO' FROM DUAL;
SELECT 	CASE WHEN IDADR IS NOT NULL 
		THEN 'ETASCO_' || IDETASCO || ';ADR_' || IDADR || ';' || NOMETASCO || ';' || TELETASCO 
		ELSE 'ETASCO_' || IDETASCO || ';' || IDADR || ';' || NOMETASCO || ';' || TELETASCO 
		END
FROM ETABLISSEMENTSCOLAIRES;
spool off

spool './CSV_Table/formations.txt' 
SELECT 'IDFORM;IDETASCO;NIVEAU;SPECIALITE' FROM DUAL;
SELECT 	CASE WHEN IDETASCO IS NOT NULL 
		THEN 'FORM_' || IDFORM || ';ETASCO_' || IDETASCO || ';' || NIVEAU || ';' || SPECIALITE
		ELSE 'FORM_' || IDFORM || ';' || IDETASCO || ';' || NIVEAU || ';' || SPECIALITE
		END
FROM FORMATIONS;
spool off

spool './CSV_Table/obtention_permis.txt' 
SELECT 'NOMPERM;IDCAN;DATEOBTENTION' FROM DUAL;
SELECT NOMPERM || ';CAN_' || IDCAN || ';' || DATEOBTENTION FROM OBTENTIONPERMIS;
spool off

spool './CSV_Table/relation_CtrInt_Can.txt' 
SELECT 'NOMCTRINT;IDCAN' FROM DUAL;
SELECT NOMCTRINT || ';CAN_' || IDCAN FROM RELATION_CENTINT_CAN;
spool off

spool './CSV_Table/relation_Langue_Can.txt' 
SELECT 'NOMLANGUE;IDCAN;NIVEAU' FROM DUAL;
SELECT NOMLANGUE || ';CAN_' || IDCAN || ';' || NIVEAU FROM RELATION_LANG_CAN;
spool off

spool './CSV_Table/relation_Competence_Can.txt' 
SELECT 'NOMCPT;IDCAN' FROM DUAL;
SELECT NOMCPT || ';CAN_' || IDCAN FROM RELATION_COMP_CAN;
spool off

spool './CSV_Table/experiences.txt' 
SELECT 'IDENT;IDCAN;POSTE;TYPECONTRAT;DESCRIPTIFEXP;DATEDEBUTEXP;DATEFINEXP' FROM DUAL;
SELECT 'ENT_' || IDENT || ';CAN_' || IDCAN || ';' || POSTE || ';' || TYPECONTRAT || ';' || DESCRIPTIFEXP || ';' || DATEDEBUTEXP || ';' || DATEFINEXP FROM EXPERIENCES;
spool off

spool './CSV_Table/suit_formations.txt' 
SELECT 'IDFORM;IDCAN;DATEDEBUTFORM;DATEFINFORM' FROM DUAL;
SELECT 'FORM_' || IDFORM || ';CAN_' || IDCAN || ';' || DATEDEBUTFORM || ';' || DATEFINFORM FROM SUIT_FORMATIONS;
spool off


SET echo off
SET termout on
SET feedback on
SET head ON
SET pages 1000
SET LINES 1000
SET pagesize 1000
SET pause off
SET colsep ' '