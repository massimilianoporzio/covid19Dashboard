from django.shortcuts import render
import requests
import pandas as pd

# Create your views here.
def indexPage(request):
    response = requests.get('https://api.covid19api.com/summary').json()
    totals = response['Global']
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
    return render(request, 'index.html', context=context)