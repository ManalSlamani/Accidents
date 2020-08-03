from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.db.models import Count, Q
from .models import accidents
from chartit import DataPool, Chart



# Create your views here.
def home(request):
    return render(request, 'home/welcome.html')


def get_data(request, *args, **kwargs):
    # data = Sheet1.objects.values('wilaya').annotate(total=Count('wilaya')).order_by('wilaya')

    dataa = accidents.objects.all()
    return render(request, 'home/lineChart.htm', {'dataa': dataa})

    #return JsonResponse(data, safe=False)
def dashboard(request):
    dashboard = DataPool(
        series=
        [{'options': {
            #    'source': SalesReport.objects.all()},
            'source': accidents},
            # 'source': SalesReport.objects.filter(sales__lte=10.00)},
            'terms': [{'jour': 'jour',
                       'nbre_dec': 'nbre_dec'}]
        },

        ])

    def dayname(jour):
        names = {'dimanche': 'Dim', 'lundi': 'Lun', 'mardi': 'Mar', 'mercredi': 'Mer', 'jeudi': 'Jeu', 'vendredi': 'Ven',
                 'samedi': 'Sam'}
        return names[jour]
        # Step 2: Create the Chart object

    cht = Chart(
        datasource=dashboard,
        series_options=
        [{'options': {
            'type': 'column',
            'stacking': False},
            'terms': {
                'jour': [
                    'nbre_dec']
            }}],
        chart_options=
        {'title': {
            'text': 'Nombre de deces par jour'},
            'xAxis': {
                'title': {'text': 'Total Deces'}},
            'yAxis': {
                'title': {'text': 'jour de semaine'}},
            'legend': {
                'enabled': True},
            'credits': {
                'enabled': True}},

        x_sortf_mapf_mts=(None, dayname, False))
    # Step 3: Create a second chart object
    cht2 = Chart(
        datasource=dashboard,
        series_options=
        [{'options': {
            'type': 'pie',
            'plotBorderWidth': 1,
            'zoomType': 'xy',

            'legend': {
                'enabled': True,
            }},

            'terms': {
                'jour': [
                    'nbre_dec']
            }}],

        chart_options=
        {'title': {
            'text': 'Deces par jour - Pie Chart'},
            'xAxis': {
                'title': {'text': 'Deces total'}},
            'yAxis': {
                'title': {'text': 'jour'}},

            'legend': {
                'enabled': True},
            'credits': {
                'enabled': True}},

        x_sortf_mapf_mts=(None, dayname, False))
    # Step 4: Send the chart object to the template.
    return render(request, 'home/chart.html',
                  {'chart_list': [cht, cht2]})

