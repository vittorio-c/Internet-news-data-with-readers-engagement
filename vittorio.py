import pandas as pd
import re
import sys
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from classes.Chart import Chart
import time

class ItemValues(Enum):
    MAX_THRESHOLD_WORD_LENGTH = 3
    UNMEANINGFULL_WORDS = ['after', 'with', 'from', 'says', 'year', 'will', 'over']

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

def getDefaultWordList(df):
    '''
    :return: a dict of form : {
          'government': [123, 5564, 122, 4],
          'juventus': [2, 569, 9784, 12]
    };
    '''
    word_list = {};

    df = reduceInitialDataframe(df)

    for index, title in df['title'].items():
        if title:
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

def reduceInitialDataframe(df):
    # keep only rows that has at least 1 like and that has no NaN values
    return df[df.engagement_reaction_count != 0].dropna()

def isWordValid(word):
    if len(word) <= ItemValues.MAX_THRESHOLD_WORD_LENGTH.value:
        return False

    if word == word.upper():
        return False

    if word in ItemValues.UNMEANINGFULL_WORDS.value:
        return False

    return True

def cleanUpWord(word):
    return word.strip()

def getMatchsTitleWord(data_frame, word):
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

def drawHorizontalThreeBarsChart(keys, vals, labels, height=0.8):
    plt.figure(figsize=(20,15))

    # trick to display bars in descending order
    Y = list(reversed(keys))
    for idx,val in enumerate(vals):
        vals[idx] = list(reversed(val))


    n = len(vals) # n = 3
    _Y = np.arange(len(Y)) # _Y = array([0, 1, 2, ...])

    # ajout des bard de graph
    for i in range(n):
        # _Y - 0.8/2. = array([-0.4,  0.6,  1.6])
        plt.barh(_Y - height/2. + i / float(n)*height, vals[i],
                height=height/float(n), align="edge", label=labels[i])

    # placement des ticks sur l'axe Y
    plt.yticks(_Y, Y)
    # placement de la légende
    plt.legend()

def getAppParameters(user_args):
    try:
        quantity_to_show = user_args[0]
        position_to_show = user_args[1]
        steps_to_apply = user_args[2]
    except IndexError:
        quantity_to_show = 30
        position_to_show = 'first'
        steps_to_apply = 1

    return {'quantity_to_show': int(quantity_to_show),
            'position_to_show': position_to_show,
            'steps_to_apply': int(steps_to_apply)}

def getSliceToShow(parameters):
    switcher = {
            'first': [None, parameters['quantity_to_show'], parameters['steps_to_apply']],
            'last' : [-parameters['quantity_to_show'], None, parameters['steps_to_apply']]
    }
    start, stop, step = switcher.get(parameters['position_to_show'], [None, 30, 1])

    return slice(start, stop, step)



def run():
    initial_data_frame = getInitialDataFrame('./articles_data.csv')
    user_args = sys.argv[1:]
    parameters = getAppParameters(user_args)
    dict_result = {}

    start_time = time.time()
    if len(user_args) == 0:
        word_list = getUserWordList()

        for word in word_list:
            new_data_frame = getMatchsTitleWord(initial_data_frame, word)

            likes = getNumberOfLikes(new_data_frame)
            comments = getNumberOfComments(new_data_frame)
            shares = getNumberOfShares(new_data_frame)

            dict_result[word] = [likes, comments, shares]
    else:
        word_list = getDefaultWordList(initial_data_frame)

        for word,indexes in word_list.items():
            likes = getNumberOfLikesByIndexes(indexes, initial_data_frame)
            comments = getNumberOfCommentsByIndexes(indexes, initial_data_frame)
            shares = getNumberOfSharesByIndexes(indexes, initial_data_frame)

            dict_result[word] = [likes, comments, shares]

    results = dict(sorted(dict_result.items(), key=lambda v: v[1][0], reverse=True))

    category_names = ['Likes', 'Comments', 'Shares']
    words = []
    likes = []
    comments = []
    shares = []
    labels = ['Likes', 'Comments', 'Shares']
    slices = getSliceToShow(parameters)

    for key,value in list(results.items())[slices]:
        words.append(key)
        likes.append(value[0])
        comments.append(value[1])
        shares.append(value[2])

    Chart.drawHorizontalThreeBarsChart(words, [likes, comments, shares], labels)
    print("{} words proceeded in {} seconds".format(str(len(word_list)), (time.time() - start_time)))

run()
