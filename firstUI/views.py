from django.shortcuts import render
from django.conf import settings
import requests
import os
import pandas as pd
import json
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.
@cache_page(CACHE_TTL)
def indexPage(request):

    dataItalia = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')
    dataRegioni = pd.read_csv(
        'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv')

    df2 = dataRegioni.tail(21)
    df2 = df2.sort_values(by='totale_positivi', ascending=False)
    maxVal = df2.head(1)['totale_positivi'].sum()
    listaDatiMappa = []
    datiPerMappa = df2[['denominazione_regione', 'totale_positivi']]
    for index, row in datiPerMappa.iterrows():
        dato = {}
        dato['Regione'] = row['denominazione_regione'].replace('-',' ')
        dato['value'] = row['totale_positivi']
        # print(dato)
        listaDatiMappa.append(dato)
    nomiRegioni = list(df2['denominazione_regione'].values)
    countsVal = list(df2['totale_positivi'].values)

    response = requests.get('https://api.covid19api.com/summary').json()
    # italyGeoJSON = requests.get('https://gist.githubusercontent.com/datajournalism-it/f1abb68e718b54f6a0fe/raw/23636ff76534439b52b87a67e766b11fa7373aa9/regioni-con-trento-bolzano.geojson').json()
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'italy.json'), 'r') as f:
        json_data = json.load(f)
        f.close()

    italyGeoJSON = json.dumps(json_data)


    totals = response['Global']
    totaliItalia = dataItalia.tail(1)['totale_positivi'].sum()

    countries = response['Countries']
    data = pd.json_normalize(countries)
    barplotData = data[['Country', 'TotalConfirmed']].sort_values('TotalConfirmed', ascending=False)

    countryNames = barplotData['Country'].to_list()
    for (index, name) in enumerate(countryNames):
        if ", " in name:
            new_name = name.split(", ")

            countryNames[index]=new_name
        elif "(" in name:
            new_name = name.split(" (")
            new_name[1]="("+new_name[1]
            countryNames[index] = new_name
            # print(new_name)

    barPlotVals =  barplotData['TotalConfirmed'].to_list()


    context = {
        'overallCount': totals['TotalConfirmed'],
        'countryNames': countryNames,
        'countsVal': barPlotVals
    }

    context = {
        'overallCount': totaliItalia,
        'countryNames': nomiRegioni,
        'countsVal': countsVal,
        'italyGeoJSON': italyGeoJSON,
        'listaDatiMappa':listaDatiMappa,
        'maxVal' : maxVal
    }

    return render(request, 'index.html', context=context)


def drillDownACountry(request):
    print (request.POST.dict())
    context = {}
    return render(request, 'index2.html', context)
