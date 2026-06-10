import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

df=pd.read_csv("parsed_data.csv")

global date_range
date_range=False

global start_date
start_date = None
global end_date
end_date = None


# KPI 1: Total Outages
def total_outages(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df.shape[0]

print("Total Outages:", total_outages(df))

# KPI 2: Average MTTR
def average_mttr(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df['MTTR in \nMints'].mean()

print("Average MTTR:", average_mttr(df))

df['Customers'] = df['Customers'].apply(ast.literal_eval)


# KPI 3: Customers Impacted
def customers_impacted(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    customers=set()
    for i, row in df.iterrows():
        impacted=row['Customers']

        for customer in impacted:
            customers.add(customer)
    return len(customers)

print("Customers Impacted:", customers_impacted(df))

# KPI 4: Total Downtime
def total_downtime(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df['MTTR in \nMints'].sum()

print("Total Downtime:", total_downtime(df))