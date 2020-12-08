import pandas as pd
import sys

def getInitialDataFrame(data_set):
    # if data_set = csv file, pd.method_name = read_csv
    return pd.read_csv(data_set, index_col='index');

def getUserWordList():
    # TODO: constuire une liste de mots
    return [input('Which word would you like to have stats on? \n')]

def getDefaultWordList(data_frame):
    # TODO
    pass

def cleanUpWord(word):
    # TODO
    pass

def getMatchsTitleWord(data_frame, word):
    '''
    Retourne un nouveau dataframe contenant uniquement
    les lignes dont le titre contient 'word'

    :return: DataFrame
    '''
    # les mots dont les caractères précédents et suivans ne sont pas des lettres
    word_regex = '(^|\W)' + word[0] + '\W'

    return data_frame[data_frame['title'].str.contains(
        word_regex, case=False, regex=True, na=False)]

def getMatchsContentWord(data_frame, word):
    pass

def getNumberOfLikes(data_frame):
    return data_frame['engagement_reaction_count'].sum()

def getNumberOfComments(data_frame):
    return data_frame['engagement_comment_count'].sum()

def getNumberOfShares(data_frame):
    return data_frame['engagement_share_count'].sum()

def getDictOfResults(word, likes, comments, shares):
    dict_of_result = {
            'word': word,
            'likes': likes,
            'comments': comments,
            'shares': shares
    }

    return dict_of_result


initial_data_frame = getInitialDataFrame('./articles_data.csv')
word_list = getUserWordList()

if len(word_list) == 0:
    word_list = getDefaultWordList(initial_data_frame)

filtered_data_frame = getMatchsTitleWord(
        initial_data_frame,
        word_list)

likes = getNumberOfLikes(filtered_data_frame)
comments = getNumberOfComments(filtered_data_frame)
shares = getNumberOfShares(filtered_data_frame)

rows_list = []

for word in word_list:
    rows_list.append(getDictOfResults(word, likes, comments, shares))

final_dataframe = pd.DataFrame(rows_list)

print(final_dataframe)

for word in word_list:
    pass



