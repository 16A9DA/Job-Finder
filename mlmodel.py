from datasets import load_dataset
import pandas as pd
import re
import unicodedata
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics.pairwise import cosine_similarity
import json


def clean_text(text):
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[@,$,&,/]", " ", text)
    text = re.sub(r"[<.*?>]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text


def load_and_clean_dataset():
    df = pd.DataFrame(
        load_dataset(
            "hanshan1988/recruitment-dataset-job-descriptions-english-sample-pt5",
            split="train",
        )
    )

    # dropping col as we do not need them
    df = df.drop(
        columns=[
            "Exp Years",
            "English Level",
            "Published",
            "Long Description_lang",
            "id",
        ]
    )

    # cleaning long descrption
    df["Long Description"] = df["Long Description"].apply(clean_text)

    # change index value to salary
    df.rename(columns={"__index_level_0__": "Salary"}, inplace=True)

    return df


def plot_skill_frequency(df):
    # Count frequency of each skill
    skill_counts = df["Primary Keyword"].value_counts()
    skills = skill_counts.index
    counts = skill_counts.values

    plt.figure(figsize=(12, 6))
    # bars must be assigned to capture them
    bars = plt.bar(skills, counts)

    plt.xticks(rotation=90)  # rotate so they dont overlap
    plt.xlabel("Skills")
    plt.ylabel("Frequency")
    plt.title("Frequency of Skills in Dataset")
    plt.show()


def prepare_train_test(df):
    X_train, X_test, Y_train, Y_test = train_test_split(
        df["Primary Keyword"], df["Position"], test_size=0.2, random_state=30
    )

    # vectorize
    tfid = TfidfVectorizer()
    # learn and apply both on training
    X_train_tfid = tfid.fit_transform(X_train)
    # apply what you trained on test data
    X_test_tfid = tfid.transform(X_test)

    return X_train, X_test, Y_train, Y_test, tfid, X_train_tfid, X_test_tfid


def train_model(X_train_tfid, Y_train):
    # as we have several different uniqure outputs, MLP would be better
    tfd_MLP = MLPClassifier()  # model
    tfd_MLP.fit(X_train_tfid, Y_train)  # learn
    return tfd_MLP


# this is additional function to help import return values of tfid and other values to use in main.py
def load_ml_model():
    # Load data
    df = load_and_clean_dataset()
    X_train, X_test, Y_train, Y_test = train_test_split(
        df["Primary Keyword"], df["Position"], test_size=0.2, random_state=30
    )

    # Vectorizer
    tfid = TfidfVectorizer()
    X_train_tfid = tfid.fit_transform(X_train)

    # Model
    tfd_MLP = MLPClassifier()
    tfd_MLP.fit(X_train_tfid, Y_train)

    return tfid, tfd_MLP, X_train_tfid, X_train, df


def predict_data(user_skills: list, tfid, tfd_MLP, X_train_tfid, X_train, df):
    company = {"Positions": [], "Companies": [], "Descriptions": [], "Salaries": []}
    for skill in user_skills:
        vec = tfid.transform(
            [skill]
        )  # trasform expects list, we give it each skills as list
        pred = tfd_MLP.predict(vec)[
            0
        ]  # output is np array we use [0] to give it as string

        similarity = cosine_similarity(
            vec, X_train_tfid
        )  # cosine checks similarity for other info we need, output 0(not)/1(similar)
        index = np.argmax(
            similarity
        )  # finds the training sample index with the highest similarity

        # append all info in company, using index find the other info on training set and append
        company["Positions"].append(pred)
        company["Companies"].append(df.iloc[X_train.index[index]]["Company Name"])
        company["Descriptions"].append(
            df.iloc[X_train.index[index]]["Long Description"]
        )
        company["Salaries"].append(
            int(df.iloc[X_train.index[index]]["Salary"])
        )  # covert to int as
        # "Object of type int64 is not JSON serializable" on fastapi

    return company


# example predict
def example_prediction(X_test_tfid, tfd_MLP):
    predicton = tfd_MLP.predict(X_test_tfid[0])  # predict
    print(predicton[0])


if __name__ == "__main__":
    df = load_and_clean_dataset()  # load data set
    plot_skill_frequency(df)  # plot key words
    X_train, X_test, Y_train, Y_test, tfid, X_train_tfid, X_test_tfid = (
        prepare_train_test(df)
    )  # train and test
    tfd_MLP = train_model(X_train_tfid, Y_train)  # MLP
    example_prediction(X_test_tfid, tfd_MLP)
