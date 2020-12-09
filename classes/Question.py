class Question :
    title = 'Empty'
    data = [] # Dataframe
    processResult = None
    processGraphic = None
    temp_variable = {}

    def __init__(self, title, data, callbackResult, callbackGraphic) :
        self.title = title
        self.data = data

        self.processResult = callbackResult
        self.processGraphic = callbackGraphic
    
    def showResult(self) :
        """ Montre le resultat """
        self.processResult(self.data, self)
        print("\n")
    
    def showGraphic(self) :
        """ Montre le graphique"""
        self.processGraphic(self.data, self)



# DANS LE FICHIER JUPITER

data = ['pouet'] # read_csv() ...

# Question 1
""" def resolve(data):
    print('Voila le resultat')


my_question = Question('Quels sont les mots clés produisant le plus d\'engagement ?', data, resolve)

my_question.showResult() """
        