import pandas as pd
import re
import sys
import math
import time
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

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
    # dict_of_result = {
            # 'word': word,
            # 'likes': likes,
            # 'comments': comments,
            # 'shares': shares
            # }

    result[word] = [likes, comments, shares]
    return result

# Create bar chart with matplotlib
def createBarChart(title, datas, labels, explode, autopct = '%1.2f%%') :
    fig, ax = plt.subplots()

    ax.bar()

    ax.pie(datas, explode=explode, labels=labels, autopct=autopct,
            shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title(title)

    plt.show()


def survey(X, vals, width=0.8):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    # labels = list(results.keys())
    # print(labels)
    # data = np.array(list(results.values()))
    # print(data)
    # data_cum = data.cumsum(axis=1)
    # category_colors = plt.get_cmap('RdYlGn')(
        # np.linspace(0.15, 0.85, data.shape[1]))

    # likes = results.values()[0]
    # comments = results.values()[1]
    # shares = results.values()[2]

    n = len(vals)
    _X = np.arange(len(X))
    for i in range(n):
        plt.barh(_X - width/2. + i/float(n)*width, vals[i],
                height=width/float(n), align="edge")
    plt.yticks(_X, X)

    # ax = plt.subplots(111)
    # ax.bar(labels[], likes, width=0.2, color='b', align='center')
    # ax.bar(, comments, width=0.2, color='g', align='center')
    # ax.bar(, shares, width=0.2, color='r', align='center')
    # ax.invert_yaxis()
    # ax.xaxis.set_visible(False)
    # ax.set_xlim(0, np.sum(data, axis=1).max())

    # for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        # widths = data[:, i]
        # print("aoubzda")
        # print(widths)
        # starts = data_cum[:, i] - widths
        # ax.barh(labels, widths, left=starts, height=0.5,
                # label=colname, color=color)
    # ax.barh(labels, data, height=0.5)
        # xcenters = starts + widths / 2

        # r, g, b, _ = color
        # text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        # for y, (x, c) in enumerate(zip(xcenters, widths)):
            # ax.text(x, y, str(int(c)), ha='center', va='center',
                    # color=text_color)
    # ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              # loc='lower left', fontsize='small')

    # return fig, ax

def run():
    initial_data_frame = getInitialDataFrame('./articles_data.csv')
    word_list = getUserWordList()
    dict_result = {}
    start_time = time.time()

    if word_list == False:
        word_list = getDefaultWordList(initial_data_frame)

        for word,indexes in word_list.items():
            likes = getNumberOfLikesByIndexes(indexes, initial_data_frame)
            comments = getNumberOfCommentsByIndexes(indexes, initial_data_frame)
            shares = getNumberOfSharesByIndexes(indexes, initial_data_frame)

            dict_result[word] = [likes, comments, shares]
    else:
        for word in word_list:
            new_data_frame = getMatchsTitleWord(initial_data_frame, word)

            likes = getNumberOfLikes(new_data_frame)
            comments = getNumberOfComments(new_data_frame)
            shares = getNumberOfShares(new_data_frame)

            dict_result[word] = [likes, comments, shares]

    # final_dataframe = pd.DataFrame(dict_result).sort_values('likes', ascending=False)

    # print(dict_result)
    # print(final_dataframe)

    # if len(final_dataframe.index) > 100:
        # print('Only 10 first results : ')
        # print(final_dataframe[:10].plot.barh('word'))
    # else:
        # print(final_dataframe.plot.barh('word'))
    # print(dict_result)
    # sys.exit()

    print()
    # print(list(dict_result.items())[:10])
    for result in dict_result.items():
        print(result)
    print(type(dict_result))
    sys.exit()

    category_names = ['Likes', 'Comments', 'Shares']
    # results = dict(sorted(dict_result.items(), key=lambda k, v: v[0], reverse=False))

    # print(list(results)[:10])

    # print(results)
    # print(type(results))
    # sys.exit()

    # print(rows_list_sorted)
    # sys.exit()

    # names = []
    # values = []
    # for row in rows_list_sorted[-30:]:
        # names.append(row['word'])
        # values.append(row['likes'])


    # names = ['group_a', 'group_b', 'group_c']
    # values = [1, 10, 100]

    # plt.figure(figsize=(9, 3))
    # plt.figure()

    # plt.figure(num=1, figsize=(6,12))
    # plt.subplot()
    # plt.bar(names, values, color="b", height=0.25)
    # # plt.subplot(132)
    # # plt.scatter(names, values)
    # # plt.subplot(133)
    # # plt.plot(names, values)
    # plt.suptitle('TEST TEST')
    # plt.show()

    words = []
    likes = []
    comments = []
    shares = []

    for key,value in list(results.items())[:10]:
        words.append(key)
        likes.append(value[0])
        comments.append(value[1])
        shares.append(value[2])

    # words = list(results.keys()) # words
    # likes = list(results.values()) # likes
    # likes = list(results.values()[0]) # likes
    # comments = list(results.values()[1]) # comments
    # shares = list(results.values()[2]) # shares

    # print(words)
    # print(likes)
    # print(comments)
    # print(shares)
    # print(words)
    # sys.exit()


    survey(words, [likes, comments, shares])
    plt.show()

    # print("--- {} words proceeded in {} seconds ---".format(len(word_list), (time.time() - start_time)))

run()



def show30first():
    pass

def show30last():
    pass

# fig, ax = plt.subplots()  # Create a figure containing a single axes.
# print(ax.plot([1, 2, 3, 4], [1, 4, 2, 3])) # Plot some data on the axes.
# print(type(ax))
# plt.title('hetllo')

# plt.show()


# evenly sampled time at 200ms intervals
# t = np.arange(0., 5., 0.2)

# print(type(t))
# sys.exit()

# red dashes, blue squares and green triangles
# plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
# plt.show()

