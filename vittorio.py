import pandas as pd
import re
import sys
from enum import Enum
import math
import time

class ItemValues(Enum):
    MAX_THRESHOLD_WORD_LENGTH = 3

def getInitialDataFrame(data_set):
    # if data_set = csv file, pd.method_name = read_csv
    return pd.read_csv(data_set, index_col='index');

def getUserWordList():
    clean_word_list = [];
    user_word_list = input('Which ord would you like to have stats on? \n')

    if len(user_word_list) == 0:
        return False

    for word in user_word_list.split(','):
        clean_word_list.append(cleanUpWord(word))

    return clean_word_list

def getDefaultWordList(data_frame):
    word_list = [];

    for title in data_frame['title']:
        if title and not pd.isna(title):
            word_list_temp = re.sub("(?:\W|\d)", " ", title).split()

        for word in word_list_temp:
            if word.lower() not in word_list and isWordValid(word):
                word_list.append(word.lower())

    return word_list[:500]

def isWordValid(word):
    if len(word) <= ItemValues.MAX_THRESHOLD_WORD_LENGTH.value:
        return False

    if word == word.upper():
        return False

    return True

def cleanUpWord(word):
    return word.strip()

def getMatchsTitleWord(data_frame, word):
    '''
    Retourne un nouveau dataframe contenant uniquement
    les lignes dont le titre contient 'word'

    :return: DataFrame
    '''
    # les mots dont les caractères précédents et suivans ne sont pas des lettres
    word_regex = '(?:^|\W)' + word + '\W'

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

def run():
    initial_data_frame = getInitialDataFrame('./articles_data.csv')
    word_list = getUserWordList()

    if word_list == False:
        word_list = getDefaultWordList(initial_data_frame)

    rows_list = []

    for word in word_list:
        start_time = time.time()
        print(word)
        filtered_data_frame = getMatchsTitleWord(
                initial_data_frame,
                word)

        likes = getNumberOfLikes(filtered_data_frame)
        comments = getNumberOfComments(filtered_data_frame)
        shares = getNumberOfShares(filtered_data_frame)

        rows_list.append(getDictOfResults(word, likes, comments, shares))

        print("--- %s seconds ---" % (time.time() - start_time))

        # print(rows_list)
        # sys.exit()

    final_dataframe = pd.DataFrame(rows_list).sort_values('likes', ascending=False)

    print(final_dataframe)

run()
