from django.shortcuts import render, redirect
from django.http import FileResponse
from .forms import SelectionForm
import datafunctions
import json


# Create your views here.

def base(request):
    return render(request, 'home/base.html')

def docs(request):
    return render(request, 'home/docs.html')

def view_pp(request):
    filename = 'SP-2-DataMining-AI-ProjectPlan.pdf'
    return FileResponse(open(filename, 'rb'), content_type='application/pdf')

def view_srs(request):
    filename = 'SP-2-DataMiningAI-SRS.pdf'
    return FileResponse(open(filename, 'rb'), content_type='application/pdf')

def data(request):
    form = SelectionForm(request.POST or None)
    formtitle = 'Select variables'
    characteristic = ''
    crime = ''
    graphtitle = ''
    xvals = []
    yvals = []
    xvalsjson = None
    yvalsjson = None

    # when 'Create graph' button is clicked
    if request.method == 'POST':

        # get characteristic (string)
        characteristictuple = request.POST.get('personal_characteristics')
        characteristicvalue = int(characteristictuple) - 1
        characteristics = ["all", "age", "race", "sex", "sexual orientation", "gender identity", "household income", "urban, suburban, or rural", "reported to police", "did not report to police"]
        characteristic = characteristics[characteristicvalue]

        # get crime (string)
        crimetuple = request.POST.get('crime_type')
        crimevalue = int(crimetuple) - 1
        crimes = ["all violent victimizations", "all property victimizations", "thefts and attempted thefts", "breakins and attempted breakins", "motor vehicle thefts", "attacks and threats", "unwanted sex"]
        crime = crimes[crimevalue]

        # get rate or number (string)
        rntuple = request.POST.get('rate_or_number')
        rnvalue = int(rntuple) - 1
        rnlist = ["rate", "number"]
        rate_or_number = rnlist[rnvalue]

        # generate graph title (string)
        graphtitle = "Viewing {} of {} by {}:".format(rate_or_number, crime, characteristic)

        # generate x and y values of the graph (lists)
        for i in range(1992,2022):
            xvals.append(i)
        xvalsjson = json.dumps(xvals)
        yvals = datafunctions.create_graph(characteristic, crime, rate_or_number)
        yvalsjson = json.dumps(yvals)

    context = {
        'characteristic': characteristic,
        'crime': crime,
        'graphtitle': graphtitle,
        'formtitle': formtitle,
        'form': form,
        'xvals': xvalsjson,
        'yvals': yvalsjson
    }
    return render(request, 'home/data.html', context)

def findings(request):
    return render(request, 'home/findings.html')