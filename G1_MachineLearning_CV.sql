SET SERVEROUTPUT ON;


-- Procédure permettant de créer une GROSSE table avec toutes les autres tables afin qu'elle puisse être traitée avec du Machine Learning en Python
CREATE OR REPLACE PROCEDURE CREATE_TABLE_MACHINE_LEARNING AS 
	
	-- Curseur sur les tables
	 CURSOR cur_competence IS SELECT * FROM COMPETENCES;
	 CURSOR cur_ctr_interet IS SELECT * FROM CENTREINTERET;
	 CURSOR cur_permis IS SELECT * FROM PERMIS;
	 CURSOR cur_langue IS SELECT * FROM LANGUES;

	-- Variables de gestion
	 test_existence_col NUMBER(2);
	 test_existence_table NUMBER(2);
	 nom_col VARCHAR2(150);
	 
	 BEGIN 
		 SELECT COUNT(*) INTO test_existence_table FROM ALL_TABLES WHERE TABLE_Name = 'TABLE_MACHINE_LEARNING';
		 IF test_existence_table > 0 THEN
			 EXECUTE IMMEDIATE 'DROP TABLE TABLE_MACHINE_LEARNING';
		 END IF;

		 EXECUTE IMMEDIATE 'CREATE TABLE TABLE_MACHINE_LEARNING AS (SELECT NOMCV, IDCAN, ADMIS, PHOTO, SEXE, AGE, NATIONALITE, PAYSADR, CONTINENTADR FROM (CV JOIN CANDIDATS USING(IDCAN)) LEFT JOIN ADRESSES USING(IDADR))';
		 
		-- Ajout de colonnes pour chaque compétence
		-- La valeur de la colonne sera 0 si le candidat n'a pas la compétence, 1 sinon
		 FOR ligne in cur_competence LOOP 
			-- On enleve les caractères de ponctuations et les espaces pour le nom de la colonne 
		     nom_col := REGEXP_REPLACE(ligne.NOMCPT,'[[:punct:]]','_');
			 nom_col := REGEXP_REPLACE(nom_col,' ','_');
			 IF LENGTH(ligne.NOMCPT) > 20 THEN
				 nom_col := SUBSTR(nom_col, 0, 20);
			 END IF;
			-- On vérifie que la colonne n'existe pas déjà pour l'ajouter à la table
			 SELECT COUNT(*) INTO test_existence_col FROM ALL_TAB_COLUMNS WHERE TABLE_Name = 'TABLE_MACHINE_LEARNING' AND COLUMN_name = nom_col;
			 IF test_existence_col = 0 THEN
				 EXECUTE IMMEDIATE 'ALTER TABLE TABLE_MACHINE_LEARNING ADD ' || nom_col || ' CHAR DEFAULT 0';
			 END IF;
			-- On la met à jour avec 1 si le candidat à la compétence
			 EXECUTE IMMEDIATE 'UPDATE TABLE_MACHINE_LEARNING SET ' || nom_col || ' = 1' || ' WHERE IDCAN IN (SELECT IDCAN FROM RELATION_COMP_CAN WHERE NOMCPT = ' || CHR(39) || ligne.NOMCPT || CHR(39) || ')';
		 END LOOP;
		 
		-- Ajout de colonnes pour les centres d'interet
		FOR ligne in cur_ctr_interet LOOP 
		     nom_col := REGEXP_REPLACE(ligne.NOMCTRINT,'[[:punct:]]','_');
			 nom_col := REGEXP_REPLACE(nom_col,' ','_');
			 IF LENGTH(ligne.NOMCTRINT) > 20 THEN
				 nom_col := SUBSTR(nom_col, 0, 20);
			 END IF;
			-- On vérifie que la colonne n'existe pas déjà pour l'ajouter à la table
			 SELECT COUNT(*) INTO test_existence_col FROM ALL_TAB_COLUMNS WHERE TABLE_Name = 'TABLE_MACHINE_LEARNING' AND COLUMN_name = nom_col;
			 IF test_existence_col = 0 THEN
				 EXECUTE IMMEDIATE 'ALTER TABLE TABLE_MACHINE_LEARNING ADD ' || nom_col || ' CHAR DEFAULT 0';
			 END IF;
			 EXECUTE IMMEDIATE 'UPDATE TABLE_MACHINE_LEARNING SET ' || nom_col || ' = 1' || ' WHERE IDCAN IN (SELECT IDCAN FROM RELATION_CENTINT_CAN WHERE NOMCTRINT = ' || CHR(39) || ligne.NOMCTRINT || CHR(39) || ')';
		 END LOOP;
		 
		-- Ajout de colonnes pour les permis
		FOR ligne in cur_permis LOOP 
		     nom_col := REGEXP_REPLACE(ligne.NOMPERM,'[[:punct:]]','_');
			 nom_col := REGEXP_REPLACE(nom_col,' ','_');
			 IF LENGTH(ligne.NOMPERM) > 20 THEN
				 nom_col := SUBSTR(nom_col, 0, 20);
			 END IF;
			-- On vérifie que la colonne n'existe pas déjà pour l'ajouter à la table
			 SELECT COUNT(*) INTO test_existence_col FROM ALL_TAB_COLUMNS WHERE TABLE_Name = 'TABLE_MACHINE_LEARNING' AND COLUMN_name = nom_col;
			 IF test_existence_col = 0 THEN
				 EXECUTE IMMEDIATE 'ALTER TABLE TABLE_MACHINE_LEARNING ADD ' || nom_col || ' CHAR DEFAULT 0';
			 END IF;
			 EXECUTE IMMEDIATE 'UPDATE TABLE_MACHINE_LEARNING SET ' || nom_col || ' = 1' || ' WHERE IDCAN IN (SELECT IDCAN FROM OBTENTIONPERMIS WHERE NOMPERM = ' || CHR(39) || ligne.NOMPERM || CHR(39) || ')';
		 END LOOP;
		 
		-- Ajout de colonnes pour les langues
		FOR ligne in cur_langue LOOP 
		     nom_col := REGEXP_REPLACE(ligne.NOMLANGUE,'[[:punct:]]','_');
			 nom_col := REGEXP_REPLACE(nom_col,' ','_');
			 IF LENGTH(ligne.NOMLANGUE) > 20 THEN
				 nom_col := SUBSTR(nom_col, 0, 20);
			 END IF;
			-- On vérifie que la colonne n'existe pas déjà pour l'ajouter à la table
			 SELECT COUNT(*) INTO test_existence_col FROM ALL_TAB_COLUMNS WHERE TABLE_Name = 'TABLE_MACHINE_LEARNING' AND COLUMN_name = nom_col;
			 IF test_existence_col = 0 THEN
				 EXECUTE IMMEDIATE 'ALTER TABLE TABLE_MACHINE_LEARNING ADD ' || nom_col || ' CHAR DEFAULT 0';
			 END IF;			 
			 EXECUTE IMMEDIATE 'UPDATE TABLE_MACHINE_LEARNING SET ' || nom_col || ' = 1' || ' WHERE IDCAN IN (SELECT IDCAN FROM RELATION_LANG_CAN WHERE NOMLANGUE = ' || CHR(39) || ligne.NOMLANGUE || CHR(39) || ')';
		 END LOOP;
		 
	 END;
	/
	
CREATE OR REPLACE PROCEDURE ECRIRE_FICHIER AS
	 CURSOR cur_table IS SELECT COLUMN_name FROM ALL_TAB_COLUMNS WHERE TABLE_Name = 'TABLE_MACHINE_LEARNING' ORDER BY COLUMN_name;
	 CURSOR cur_machine_learning IS SELECT * FROM TABLE_MACHINE_LEARNING ;

	 query VARCHAR2(20000) := '';
	 c VARCHAR2(20000) := '';
	 enreg VARCHAR2(25000);

     TYPE cursor_type IS REF CURSOR;
     moncurseur cursor_type;
	 
	 BEGIN
		-- Ecriture des colonnes dans le fichier
		 FOR col in cur_table LOOP
			 query := query || '"' || col.COLUMN_name || '";';
		 END LOOP;
		 query := SUBSTR(query, 1, LENGTH(query) - 1);
		 query := query || '@';
		 DBMS_OUTPUT.PUT_LINE(query);
		 
		 FOR ligne in cur_machine_learning LOOP
			 query := '';
		 	 FOR col in cur_table LOOP
				 Open moncurseur For 'SELECT ' || col.COLUMN_name || ' FROM TABLE_MACHINE_LEARNING WHERE IDCAN = ' || ligne.IDCAN ;
				 LOOP
					 FETCH moncurseur INTO enreg;
					 EXIT WHEN moncurseur%NOTFOUND;
					 IF col.COLUMN_name IN ('NOMCV', 'IDCAN', 'ADMIS', 'PHOTO', 'SEXE', 'NATIONALITE', 'PAYSADR', 'CONTINENTADR') THEN
						 query := query || '"' || enreg || '";';
					 ELSE
						 query := query || enreg || ';';
					 END IF;
				 END LOOP;
				 CLOSE moncurseur;
			 END LOOP;
			 query := SUBSTR(query, 1, LENGTH(query) - 1);
			 query := query || '@';

			 DBMS_OUTPUT.PUT_LINE(query);
		 END LOOP;
	 END;
	/
	
EXEC CREATE_TABLE_MACHINE_LEARNING

-- Pour le machine learning
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

spool 'tab_MachineLearning.txt' 	
EXEC ECRIRE_FICHIER;
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
