from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Greeting
import pandas as pd
import datetime


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    print('HI')
    df = pd.read_csv(
        '/Users/abhinav/Documents/abhinav_vinci/free/python-getting-started/staticfiles/temp.csv')
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
    df_ml = df["ML"].values[:20]
    df_index = df.index.values[:20]
    print('head df: ', df_ml)
    print('index df: ', df_index)

    return render(request, "index.html", {'courts': [20, 4, 23], 'club_name': 'club_name', 'df_ml': list(df_ml), 'df_index': list(df_index)
                                          })


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
