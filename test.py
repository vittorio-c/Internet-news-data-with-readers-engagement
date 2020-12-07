import pandas as pd

dataframe = pd.read_csv('./articles_data.csv', sep=',')

print(dataframe.groupby('source_name')['engagement_reaction_count'].count())

