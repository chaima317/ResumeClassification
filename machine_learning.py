import numpy as np
import pandas as pd
from matplotlib import pyplot
from sklearn.impute import KNNImputer
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder



class MachineLearningCV:
    labelencoder = LabelEncoder()
    def __init__(self):
        self.df = self.dataFrame()

        self.X_train, self.Y_train = self.training()
        self.X,self.Y=self.extraction_Importante_features()
        self.model = self.model()

        #self.Y_pred = self.predict()
        #self.extraction_Importante_features()
    def dataFrame(self):
        df = pd.read_csv('tab_MachineLearning.txt', sep=';', encoding = "ISO-8859-1", header=0,  error_bad_lines=False, lineterminator="@")
        df['PAYSADR'] = df['PAYSADR'].fillna('')
        df['CONTINENTADR'] = df['CONTINENTADR'].fillna('')
        df['NATIONALITE'] = df['NATIONALITE'].fillna('')
        df.loc[:,['PAYSADR']] = self.labelencoder.fit_transform(df.loc[:,'PAYSADR'].values)
        df.loc[:,['CONTINENTADR']] = self.labelencoder.fit_transform(df.loc[:,'CONTINENTADR'].values)
        df.loc[:,['NATIONALITE']] = self.labelencoder.fit_transform(df.loc[:,'NATIONALITE'].values)
        df.iloc[:,0] = df.iloc[:,0].str.replace('\n', '')
        df.iloc[:,0] = df.iloc[:,0].str.replace('\r', '')
        df['PHOTO'] = df['PHOTO'].fillna(0)
        df['PHOTO'] = df['PHOTO'].apply(lambda x: 1 if x != 0 else 0) 
        df['SEXE'].replace(['M', 'F'], [0, 1], inplace=True)
        df['ADMIS'].replace(['ACCEPTE ', 'REFUSE ','nan'], [0, 1,2], inplace=True)
        df=df.iloc[0:49, :]
        df.replace(to_replace='2020-12-03-CV_ESSEBBABI_Nour.pdf', value='Nour', regex=True)

        print(df)

        return df

    def extraction_Importante_features(self):
        arr=[]
        for feat in ['PAYSADR', 'CONTINENTADR', 'NATIONALITE', 'PAYSADR', 'PHOTO', 'SEXE','ADMIS',]:
            self.df[feat] = self.labelencoder.fit_transform(self.df[feat])
        model = DecisionTreeClassifier()
        # fit the model
        model.fit(self.X_train, self.Y_train)
        # get importance
        importance = model.feature_importances_
        # summarize feature importance
        for i, v in enumerate(importance):
            print('Feature: %0d, Score: %.5f' % (i, v))
            if v>0:
                arr.append(i)
        # plot feature importance
        pyplot.bar([x for x in range(len(importance))], importance)
        pyplot.show()

        print("dataset with the more importante features")
        values=[]
        for i in arr:
             print(self.X_train.columns.values[i])
             values.append(self.X_train.columns.values[i])

        """ 
        df_test = self.df[self.df['ADMIS'] == 'INCONNU']
        
        df_test = df_test.fillna(-1)
        X_test = self.df.drop(labels=['ADMIS', 'IDCAN'], axis=1)
        X_test = X_test.fillna(-1)
         """
        X=self.X_train[values].astype(np.float16).fillna(-1)
        Y=self.Y_train


        print(X.dtypes)
        print(X)

        return X,Y


    def training(self):
        #imputer = KNNImputer(n_neighbors=2, weights="uniform")
        #self.df= imputer.fit_
        # transform(self.df)
        #self.df = self.df.dropna(how='any', axis=0)
        df_train = self.df[(self.df['ADMIS'] == 'REFUSE') | (self.df['ADMIS'] == 'ACCEPTE')]
        df_train = df_train.dropna(subset=['ADMIS'])
        df_train['ADMIS'].replace(['REFUSE', 'ACCEPTE'], [0, 1], inplace=True)
        df_train = df_train.fillna(-1)
        X_train = df_train.drop(labels=['NOMCV','ADMIS', 'IDCAN'], axis=1)
        Y_train = df_train['ADMIS']

        return X_train, Y_train

    """


def testing(self):
    df_test = self.df[self.df['ADMIS'] == 'INCONNU']
    df_test = df_test.fillna(-1)
    X_test = self.df.drop(labels=['ADMIS', 'IDCAN'], axis=1)
    X_test = X_test.fillna(-1)
    return X_test
    """

    def model(self):

        clf = GaussianNB()
        return clf.fit(self.X, self.Y)



    def score(self):
        #chaima ==>75% trainnig ,25%test
        #Test sur les données d'entrainemclearent avec 50% d'apprentissage/50% de test

        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, test_size=0.25, random_state=1)

        clf = GaussianNB()
        clf.fit(X_train, Y_train)
        Y_pred = self.model.predict(X_test)
        print('\n--------------- MESURE DE LA QUALITE DE L\'ALGORITHME DE PREDICTION ---------------')
        print('Recall Score    : ',recall_score(Y_test,Y_pred))
        print('F-Measure Score : ',f1_score(Y_test,Y_pred))
        print('Accuracy Score  : ', accuracy_score(Y_test,Y_pred))

        conf_matrix = confusion_matrix(Y_test,Y_pred, labels=[0,1])
        print(conf_matrix)
        print('Sur' , np.sum(conf_matrix), 'CV de validation (Matrice de confusion):')
        print('\t-', conf_matrix[1][0], 'CV REFUSE ont été mal classé;')
        print('\t-', conf_matrix[0][1], 'CV ACCEPTE ont été mal classé.')
        print('\t- On a donc', conf_matrix[0][0], '/', (conf_matrix[0][0] + conf_matrix[1][0]), 'CV REFUSE bien classé et',conf_matrix[1][1], '/', (conf_matrix[1][1] + conf_matrix[0][1]),'CV ACCEPTE bien classé')
        print('\t- Soit un taux de réussite de', (conf_matrix[0][0] + conf_matrix[1][1]) * 100 / np.sum(conf_matrix), '%.')
        print('----------------------------------------------------------------------------------')

if __name__ == '__main__':
    machineLearning = MachineLearningCV()
    """
    accepted_list = ['ACCEPTE' if accept else 'REFUSE' for accept in machineLearning.Y_pred]
    df_INCONNU = machineLearning.test
    df_INCONNU['ADMIS'] = accepted_list
    df_INCONNU.reset_index(drop = True, inplace = True)
    
    for i in range(len(df_INCONNU)): 
        print('Le CV "'+ str(df_INCONNU.loc[i,'NOMCV']) + '" est conseillé comme étant ' + str(df_INCONNU .loc[i,'ADMIS']) + ' par l\'algorithme.')
    """
    machineLearning.score()
