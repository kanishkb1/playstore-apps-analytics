import pandas as pd
import numpy as np

def run(dataframe):
    #Treating Version Numbers
    dataframe['Android_Ver'].replace(to_replace=[r"([1-8]).*", 'Varies with device'], value=[r"\1", "4"], inplace=True, regex=True)

    #calculate the mean of the rating and by means of category average ratings
    nan_category = dataframe.loc[dataframe['Rating'].isna()].Category.value_counts()
    for index, value in nan_category.items():
        average = dataframe.loc[dataframe['Category'] == index, 'Rating'].mean()
        dataframe.loc[dataframe['Category'] == index, 'Rating'] = dataframe.loc[dataframe['Category'] == index, 'Rating'].fillna(average)

    #Content_Rating contains many Unrated values which need to be dropped as null values
    dataframe.drop(dataframe[dataframe['Content_Rating']=='Unrated'].index,inplace= True)
    dataframe.dropna(inplace=True)

    #converting data-types of several colums into integer
    dataframe["Rating"] = pd.to_numeric(dataframe["Rating"])
    dataframe["Reviews"] = pd.to_numeric(dataframe["Reviews"])
    dataframe[["Android_Ver"]] = dataframe[["Android_Ver"]].astype(int)

    #Remove the extra characters from the Installs and Price columns and convert them to the numeric form
    dataframe['Installs'] = dataframe['Installs'].str.replace(',','',regex=False)
    dataframe['Installs'] = pd.to_numeric(dataframe['Installs'])

    dataframe['Price'] = dataframe['Price'].str.replace('$','',regex=False)
    dataframe['Price'] = pd.to_numeric(dataframe['Price'])
    dataframe["Rating"] =  dataframe['Rating'].mul(2).round().div(2)

    return dataframe

