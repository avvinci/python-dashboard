from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Greeting
import pandas as pd
import datetime
import os
from gettingstarted.settings import BASE_DIR
file_path = os.path.join(BASE_DIR, 'gettingstarted/temp.csv')

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    print('HI', file_path)
    df = pd.read_csv(file_path)
    df.columns = ["ML"]
    df = df[df.ML < 10]
    print('mean', df['ML'].mean())
    print('sum', df['ML'].sum())
    df["ML"].value_counts().sort_index()
    df["ML"].value_counts().sort_index().cumsum()
    dff = pd.DataFrame({"index": df["ML"].value_counts().sort_index().index, "cum_val":   df["ML"].value_counts(
    ).sort_index().cumsum(), "val":  df["ML"].value_counts().sort_index()})
    dff['perc'] = dff['cum_val'].apply(lambda x: x / dff.iloc[-1:]['cum_val'])
   
    dd = []
    for i in range(0, df.shape[0]):
        k = (datetime.date.today() - datetime.timedelta(days=i))
        dd.append(k)
    df['Data'] = dd[::-1]
    df = df.set_index('Data')
    df['cm_sum'] = df['ML'].cumsum()
    print('head df: ', df.head())
    df_ml = df["ML"].values[-10:]
    df_index = df.index.values[-10:]
    print('head df: ', df_ml)
    print('index df: ', df_index)

    df_ml_30 = df["ML"].values[-30:]
    df_index_30 = df.index.values[-30:]
    print('head df: ', df_ml_30)
    print('index df: ', df_index_30)

    df_ml_full = df["ML"].values
    df_index_full = df.index.values

    dff = df.reset_index()
    dff['Date'] = pd.to_datetime(dff['Data'])
    dff.set_index('Date', inplace=True)

    g = dff.groupby(pd.Grouper(freq="M"))
    gg = g.sum()
    month_full = gg["ML"].values
    month_full_index = gg.index.values
    print('head df: ', month_full)
    print('index df: ', month_full_index)

    return render(request, "index.html",
                  {'courts': [20, 4, 23], 'club_name': 'club_name',
                   'df_ml': list(df_ml), 'df_index': list(df_index),
                   'month_full': list(month_full), 'month_full_index': list(month_full_index),
                   'df_ml_full': list(df_ml_full), 'df_index_full': list(df_index_full),
                   'df_ml_30': list(df_ml_30), 'df_index_30': list(df_index_30),
                   })


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
