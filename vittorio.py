import pandas as pd
import re
import sys
import math
import time
from enum import Enum

class ItemValues(Enum):
    MAX_THRESHOLD_WORD_LENGTH = 3

def getInitialDataFrame(data_set):
    # if data_set = csv file, pd.method_name = read_csv
    return pd.read_csv(data_set, index_col='index');

def getUserWordList():
    clean_word_list = [];
    user_word_list = input('Which word would you like to have stats on? Comma-separated list, ex: "Trump, Biden" (leave empty to have full stats) \n')

    if len(user_word_list) == 0:
        return False

    for word in user_word_list.split(','):
        clean_word_list.append(cleanUpWord(word))

    return clean_word_list

def getDefaultWordList(data_frame):
    '''
    :return: a dict of form : {
          'government': [123, 5564, 122, 4],
          'juventus': [2, 569, 9784, 12]
    };
    '''
    word_list = {};

    for index, title in data_frame['title'].items():
        if title and not pd.isna(title):
            title_by_words = re.sub("(?:\W|\d)", " ", title).split()

        for word in title_by_words:
            if not isWordValid(word):
                continue

            word = word.lower()
            if word in word_list:
                if index not in word_list[word]:
                    word_list[word].append(index)
            else:
                word_list[word] = [index]

    print('Processing ' + str(len(word_list)) + ' words...')
    return word_list

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
    word_regex = '(?:^|\W)' + word + '(?:$|\W)'

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

def getNumberOfLikesByIndexes(indexes, data_frame):
    return data_frame.iloc[indexes]['engagement_reaction_count'].sum()

def getNumberOfCommentsByIndexes(indexes, data_frame):
    return data_frame.iloc[indexes]['engagement_comment_count'].sum()

def getNumberOfSharesByIndexes(indexes, data_frame):
    return data_frame.iloc[indexes]['engagement_share_count'].sum()

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
    rows_list = []
    start_time = time.time()

    if word_list == False:
        word_list = getDefaultWordList(initial_data_frame)

        for word,indexes in word_list.items():
            likes = getNumberOfLikesByIndexes(indexes, initial_data_frame)
            comments = getNumberOfCommentsByIndexes(indexes, initial_data_frame)
            shares = getNumberOfSharesByIndexes(indexes, initial_data_frame)

            rows_list.append(getDictOfResults(word, likes, comments, shares))
    else:
        for word in word_list:
            new_data_frame = getMatchsTitleWord(initial_data_frame, word)

            likes = getNumberOfLikes(new_data_frame)
            comments = getNumberOfComments(new_data_frame)
            shares = getNumberOfShares(new_data_frame)

            rows_list.append(getDictOfResults(word, likes, comments, shares))

    final_dataframe = pd.DataFrame(rows_list).sort_values('likes', ascending=False)

    if len(final_dataframe.index) > 100:
        print('Only 10 first results : ')
        print(final_dataframe[:10].plot.barh('word'))
    else:
        print(final_dataframe.plot.barh('word'))

    print("--- {} words proceeded in {} seconds ---".format(len(word_list), (time.time() - start_time)))
run()

