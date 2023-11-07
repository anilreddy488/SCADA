from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from .models import *
from django.contrib.auth import logout
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import os
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from django.http import HttpResponse
from django.db.models import Sum
import datetime
from dateutil.relativedelta import relativedelta
import docx
from docx.shared import Inches
from django.db import connection
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
import pandas as pd
import numpy as np
from .admin import DemandDataResource  # Import your resource class
from tablib import Dataset




def import_data_from_excel(file_path):
    try:
        # Read the Excel file using pandas
        df_demanddata = pd.read_excel(file_path, sheet_name='DemandData')
        df_gridfreq = pd.read_excel(file_path, sheet_name='GridFreq')
        df_schdrwldata = pd.read_excel(file_path, sheet_name='SchDrwlData')
        df_centralsectordata = pd.read_excel(file_path, sheet_name='CentralSectorData')
        df_levelstoragedata = pd.read_excel(file_path, sheet_name='LevelStorageData')
        df_inflowdischarge = pd.read_excel(file_path, sheet_name='InflowDischarge')
        df_weather = pd.read_excel(file_path, sheet_name='WeatherandOtherParameters')
        df_coalparticulars = pd.read_excel(file_path, sheet_name='CoalParticulars')
        df_wagonparticulars = pd.read_excel(file_path, sheet_name='WagonParticulars')

        # Loop through the rows and update existing model instances or create new ones
        for index, row in df_demanddata.iterrows():
            gen_station_id = row['ID']
            date = row['Date']
            
            # Check if the record exists, and create it if not
            instance, created = DemandData.objects.get_or_create(GenStationID=gen_station_id, Date=date)
            
            # Update the fields
            instance.MorningPeak = row['MorningPeak']
            instance.EveningPeak = row['EveningPeak']
            instance.Energy = row['Energy']
            instance.save()

        for index, row in df_gridfreq.iterrows():
            date = row['Date']
            
            # Check if the record exists, and create it if not
            instance, created = GridFreq.objects.get_or_create(Date=date)
            # Update the fields
            instance.FreqMorning = row['MorningFreq']
            instance.FreqEvening = row['EveningFreq']
            instance.TimeMaxDemandMorning = row['MoringMaxTime']
            instance.TimeMaxDemandEvening = row['EveningMaxTime']
            instance.save()

        for index, row in df_schdrwldata.iterrows():
            state_id = row['StateID']
            date = row['Date']
            # Try to get the existing record
            instance, created = SchDrwlData.objects.get_or_create(StateID=state_id, Date=date)
            # Update the fields
            instance.StateName = row['StateName']
            instance.Schedule = row['Schedule']
            instance.Drawl = row['Drawl']
            instance.save()


        for index, row in df_centralsectordata.iterrows():
            central_station_id = row['CentralStationID']
            date = row['Date']
            # Check if the record exists, and create it if not
            instance, created = CentralSectorData.objects.get_or_create(CentralStationID=central_station_id, Date=date)
            # Update the fields
            instance.CenStationName = row['CenStationName']
            instance.Energy = row['Energy']
            instance.save()

        for index, row in df_levelstoragedata.iterrows():
            dam_id = row['DamID']
            date = row['Date']
            # Check if the record exists, and create it if not
            instance, created = LevelStorageData.objects.get_or_create(DamID=dam_id, Date=date)
            # Update the fields
            instance.DamName = row['DamName']
            instance.Level = row['Level']
            instance.save()

        for index, row in df_inflowdischarge.iterrows():
            reservoir_id = row['ReservoirID']
            date = row['Date']
            # Check if the record exists, and create it if not
            instance, created = InflowsDischarge.objects.get_or_create(ReservoirID=reservoir_id, Date=date)
            # Update the fields
            instance.Type = row['Type']
            instance.Name = row['Name']
            instance.DamName = row['DamName']
            instance.InfDis00to24 = row['InfDis00to24']
            instance.InfDis06to06 = row['InfDis06to06']
            instance.save()

        for index, row in df_weather.iterrows():
            weather_id = row['WID']
            date = row['Date']
            # Check if the record exists, and create it if not
            instance, created = WeatherandOtherParameters.objects.get_or_create(WID=weather_id, Date=date)
            # Update the fields
            instance.Type = row['Type']
            instance.Name = row['Name']
            instance.Value = row['Value']
            instance.save()

        for index, row in df_coalparticulars.iterrows():
            genstation_id = row['GenStationID']
            date = row['Date']
            # Check if the record exists, and create it if not
            instance, created = CoalParticulars.objects.get_or_create(GenStationID=genstation_id, Date=date)
            # Update the fields
            instance.GenStationName = row['GenStationName']
            instance.OpenBal = row['OpenBal']
            instance.Receipts = row['Receipts']
            instance.Consumption = row['Consumption']
            instance.AvgCoalperDay = row['AvgCoalperDay']
            instance.save()

        for index, row in df_wagonparticulars.iterrows():
            genstation_id = row['GenStationID']
            date = row['Date']
            # Check if the record exists, and create it if not
            instance, created = WagonParticulars.objects.get_or_create(GenStationID=genstation_id, Date=date)
            # Update the fields
            instance.GenStationName = row['GenStationName']
            instance.OpenBal = row['OpenBal']
            instance.Receipts = row['Receipts']
            instance.Tippled = row['Tippled']
            instance.Pending = row['Pending']
            instance.save()

        return True, None  # Success
    except Exception as e:
        return False, str(e)  # Error message






def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            success, message = import_data_from_excel(file)
            if success:
                return render(request, 'dailyreport/success.html')
            else:
                return render(request, 'dailyreport/error.html', {'error_message': message})
    else:
        form = ExcelUploadForm()

    return render(request, 'dailyreport/upload_excel.html', {'form': form})






def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'dailyreport/home.html')

@login_required(login_url='login')
def generate_station(request):
    form = GeneratingStationForm()
    if request.method == 'POST':
        form = GeneratingStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generate_station')
    stations = GeneratingStation.objects.all()  # Retrieve all generating stations
    context = {'form': form, 'stations': stations}  # Include stations in the context
    return render(request, 'dailyreport/generate_station.html', context)

@login_required(login_url='login')
def update_generating_station(request, pk):
    station = GeneratingStation.objects.get(pk=pk)
    form = GeneratingStationForm(instance=station)
    if request.method == 'POST':
        form = GeneratingStationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('generate_station')
    context = {'form': form}
    return render(request, 'dailyreport/update.html', context)

@login_required(login_url='login')
def grid_frequency(request):
    form = GridFreqForm()
    if request.method == 'POST':
        form = GridFreqForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generate_station')
    freq = GridFreq.objects.all()  # Retrieve all generating stations
    context = {'form': form, 'freq': freq}  # Include stations in the context
    return render(request, 'dailyreport/generate_station.html', context)


@login_required(login_url='login')
def pump_station(request):
    form = PumpStationForm()
    if request.method == 'POST':
        form = PumpStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pump_station')
    stations = PumpStation.objects.all()
    context = {'form': form, 'stations': stations}
    return render(request, 'dailyreport/pump_station.html', context)


@login_required(login_url='login')
def update_pump_station(request, pk):
    station = PumpStation.objects.get(pk=pk)
    form = PumpStationForm(instance=station)
    if request.method == 'POST':
        form = PumpStationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('pump_station')
    context = {'form': form}
    return render(request, 'dailyreport/update.html', context)


@login_required(login_url='login')
def demand_data(request):
    form = DemandDataForm()
    if request.method == 'POST':
        form = DemandDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demand_data')
    data = DemandData.objects.all()
    context = {'form': form,'data':data}
    return render(request, 'dailyreport/demand_data.html', context)

@login_required(login_url='login')
def pump_load_data(request):
    form = PumpLoadDataForm()
    if request.method == 'POST':
        form = PumpLoadDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pump_load_data')
    data = PumpLoadData.objects.all()
    context = {'form': form,'data':data}
    return render(request, 'dailyreport/pump_load_data.html', context)

@login_required(login_url='login')
def state(request):
    form = StateForm()
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('state')
    states = State.objects.all()  # Retrieve all generating stations
    context = {'form': form, 'states': states}  # Include stations in the context
    return render(request, 'dailyreport/state.html', context)

@login_required(login_url='login')
def schdrwl_data(request):
    form = SchDrwlDataForm()
    if request.method == 'POST':
        form = SchDrwlDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schdrwl_data')
    context = {'form': form}
    return render(request, 'dailyreport/schdrwldata.html', context)



@login_required(login_url='login')
def export_to_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="custom_report.txt"'
    today = datetime.date.today()
    yesterday = today - relativedelta(days=1)
    daybeforeyesterday = today - relativedelta(days=2)
    cur_month = yesterday.month
    cur_year = yesterday.year
    monthstartday = f'{cur_year}-{cur_month}-01'
    fin_year_startday = f'{cur_year-1}-04-01'

    previous_year_day = yesterday - relativedelta(years=1)
    

    query_Gen = """WITH present_data AS
               (SELECT GenStationID, MorningPeak, EveningPeak, Energy 
               FROM dailyreport_DemandData
               WHERE Date=%(yesterday)s),
               last_year_data AS
               (SELECT GenStationID, Energy 
               FROM dailyreport_DemandData
               WHERE Date=%(previous_year_day)s)
               SELECT GenStationName, GenType, InstalledCap, p.MorningPeak, p.EveningPeak, p.Energy ,l.Energy, p.GenStationID
               FROM present_data AS p 
               LEFT OUTER JOIN last_year_data AS l
               ON p.GenStationID=l.GenStationID
               INNER JOIN dailyreport_GeneratingStation AS g
               ON g.GenStationID=p.GenStationID
               """

    query_TsdemandMonthCum = """
               SELECT SUM(Energy) 
               FROM dailyreport_DemandData
               WHERE Date BETWEEN %(monthstartday)s AND %(yesterday)s AND GenStationID=36
               """

    query_TsdemandFinYearCum = """
               SELECT SUM(Energy) 
               FROM dailyreport_DemandData
               WHERE (Date BETWEEN %(fin_year_startday)s AND %(yesterday)s) AND GenStationID=36
               """

    query_gridfreq = """SELECT FreqMorning,FreqEvening,TimeMaxDemandMorning,TimeMaxDemandEvening
               FROM dailyreport_GridFreq
               WHERE Date=%(yesterday)s"""

    query_centralgen = f"""
               WITH month_data AS 
               (SELECT CentralStationID, CenStationName, Energy, STRFTIME('%%Y-%%m', Date) AS month,Date
               FROM dailyreport_centralsectordata)
               SELECT CentralStationID, CenStationName, Energy, Date
               FROM month_data
               WHERE month='{cur_year}-{cur_month:02}'
               """

    query_schdrwl = f"""
               WITH month_data AS 
               (SELECT StateID, StateName, Schedule, Drawl, STRFTIME('%%Y-%%m', Date) AS month, Date
               FROM dailyreport_SchDrwlData)
               SELECT StateID, StateName, Schedule, Drawl, Date
               FROM month_data
               WHERE month='{cur_year}-{cur_month:02}'
               """

    query_levelstorage = f"""
               SELECT *
               FROM dailyreport_LevelStorage
               """
    query_levelstoragedata = """
               WITH present_data AS
               (SELECT d.DamID, d.DamName, d.Level, ls.Storage 
               FROM dailyreport_LevelStorageData AS d
               LEFT OUTER JOIN dailyreport_LevelStorage AS ls
               ON d.DamID=ls.DamID AND d.Level=ls.Level
               WHERE Date=%(yesterday)s),

               last_year_data AS
               (SELECT d.DamID, d.DamName, d.Level, ls.Storage 
               FROM dailyreport_LevelStorageData AS d
               LEFT OUTER JOIN dailyreport_LevelStorage AS ls
               ON d.DamID=ls.DamID AND d.Level=ls.Level
               WHERE Date=%(previous_year_day)s),

               yesterday_data AS
               (SELECT DamID, Level
               FROM dailyreport_LevelStorageData AS d
               WHERE Date=%(daybeforeyesterday)s)

               SELECT p.DamID, p.DamName, p.Level, p.Storage, l.Level, l.Storage, p.Level-y.Level AS LevelRaise
               FROM present_data AS p 
               LEFT OUTER JOIN last_year_data AS l
               ON p.DamID=l.DamID
               LEFT OUTER JOIN yesterday_data AS y
               ON p.DamID=y.DamID
               """

    query_inflowsdischarge = """
               SELECT ReservoirID, Name, Type, DamName, InfDis00to24, InfDis06to06, Date 
               FROM dailyreport_InflowsDischarge
               WHERE Date=%(yesterday)s
               """

    query_weatherandotherparameters = """
               SELECT WID, Name, Type, Value, Date 
               FROM dailyreport_WeatherandOtherParameters
               WHERE Date=%(yesterday)s
               """

    query_coalparticulars = """
               SELECT GenStationID, GenStationName, OpenBal, Receipts, Consumption, AvgCoalperDay, Date 
               FROM dailyreport_CoalParticulars
               WHERE Date=%(yesterday)s
               """

    query_wagonparticulars = """
               SELECT GenStationID, GenStationName, OpenBal, Receipts, Tippled, Pending, Date 
               FROM dailyreport_WagonParticulars
               WHERE Date=%(yesterday)s
               """
                
    with connection.cursor() as cursor:
        cursor.execute(query_Gen, {'yesterday': yesterday, 'previous_year_day': previous_year_day})
        gen_data = cursor.fetchall()
        print(gen_data)
        cursor.execute(query_TsdemandMonthCum, {'yesterday': yesterday, 'monthstartday': monthstartday})
        tsdemand_monthcum = cursor.fetchall()
        
        cursor.execute(query_TsdemandFinYearCum, {'yesterday': yesterday, 'fin_year_startday': fin_year_startday})
        tsdemand_finyearcum = cursor.fetchall()

        cursor.execute(query_TsdemandFinYearCum, {'yesterday': yesterday, 'fin_year_startday': fin_year_startday})
        tsdemand_finyearcum = cursor.fetchall()

        instance, created = DemandData.objects.get_or_create(GenStationID=37, Date=yesterday)
        instance.Energy = tsdemand_monthcum[0][0]
        instance.save()

        instance, created = DemandData.objects.get_or_create(GenStationID=38, Date=yesterday)
        instance.Energy = tsdemand_finyearcum[0][0]
        instance.save()

       
        cursor.execute(query_gridfreq, {'yesterday': yesterday})
        gridfreq_data = cursor.fetchall()

        cursor.execute(query_centralgen, {'cur_year': cur_year,'cur_month':cur_month})
        centralgendata = cursor.fetchall()

        cursor.execute(query_schdrwl,{'cur_year': cur_year,'cur_month':cur_month})
        schdrwldata = cursor.fetchall()

        cursor.execute(query_levelstoragedata,{'yesterday': yesterday, 'previous_year_day': previous_year_day, 'daybeforeyesterday':daybeforeyesterday})
        levelstoragedata = cursor.fetchall()

        cursor.execute(query_inflowsdischarge,{'yesterday': yesterday})
        inflowsdischargedata = cursor.fetchall()

        cursor.execute(query_weatherandotherparameters,{'yesterday': yesterday})
        weatherandotherdata = cursor.fetchall()

        cursor.execute(query_coalparticulars,{'yesterday': yesterday})
        coaldata = cursor.fetchall()

        cursor.execute(query_wagonparticulars,{'yesterday': yesterday})
        wagondata = cursor.fetchall()

        cursor.close()

        gen_data=pd.DataFrame(gen_data,columns=['GenStationName', 'GenType', 'InstalledCap', 'MorningPeak', 'EveningPeak', 'Energy' ,'PrevEnergy','GenStationID'])
        print(gen_data)
        gridfreq_data=pd.DataFrame(gridfreq_data,columns=['FreqMorning','FreqEvening','TimeMaxDemandMorning','TimeMaxDemandEvening'])

        centralgendata=pd.DataFrame(centralgendata,columns=['CentralStationID', 'CenStationName', 'Energy', 'Date'])

        schdrwldata=pd.DataFrame(schdrwldata,columns=['StateID', 'StateName', 'Schedule', 'Drawl', 'Date'])

        inflowsdischargedata=pd.DataFrame(inflowsdischargedata,columns=['ReservoirID', 'Name', 'Type', 'DamName', 'InfDis00to24', 'InfDis06to06', 'Date'])
        inf_ujurala = inflowsdischargedata[(inflowsdischargedata['Type']=='Inflow') & (inflowsdischargedata['DamName']=='Upper Jurala')]
        inf_nsagar = inflowsdischargedata[(inflowsdischargedata['Type']=='Inflow') & (inflowsdischargedata['DamName']=='NSagar')]
        inf_srisailam = inflowsdischargedata[(inflowsdischargedata['Type']=='Inflow') & (inflowsdischargedata['DamName']=='Srisailam')]
        inf_pulichintala = inflowsdischargedata[(inflowsdischargedata['Type']=='Inflow') & (inflowsdischargedata['DamName']=='Pulichintala')]
        dis_ujurala = inflowsdischargedata[(inflowsdischargedata['Type']=='Discharge') & (inflowsdischargedata['DamName']=='Upper Jurala')]
        dis_ljurala = inflowsdischargedata[(inflowsdischargedata['Type']=='Discharge') & (inflowsdischargedata['DamName']=='Lower Jurala')]
        dis_nsagar = inflowsdischargedata[(inflowsdischargedata['Type']=='Discharge') & (inflowsdischargedata['DamName']=='NSagar')]
        dis_srisailam= inflowsdischargedata[(inflowsdischargedata['Type']=='Discharge') & (inflowsdischargedata['DamName']=='Srisailam')]


        levelstoragedata=pd.DataFrame(levelstoragedata,columns=['DamID','DamName','Level', 'Storage', 'PrevLevel', 'PrevStorage', 'LevelRaise'])

        levelstoragedata['EquivalentEnergy']=levelstoragedata['Storage']*np.array([5.5,5.5,5.5,5.5,5.5,5.5,5.5,5.5])
        levelstoragedata['FRL']=np.array([1633,1045,885,590,175,1405,1091,1718])
        levelstoragedata['MDDL']=np.array([1582,1033,800,510,140,1376,1064,1699])

        weatherandotherdata = pd.DataFrame(weatherandotherdata,columns=['WID', 'Name', 'Type', 'Value', 'Date'])
        weatherdata=weatherandotherdata[weatherandotherdata['Type']=='Weather']
        otherdata=weatherandotherdata[weatherandotherdata['Type']=='River']

        coaldata = pd.DataFrame(coaldata,columns=['GenStationID', 'GenStationName', 'OpenBal', 'Receipts', 'Consumption', 'AvgCoalperDay', 'Date'])
        coaldata['Balance'] = coaldata['OpenBal']+coaldata['Receipts']-coaldata['Consumption']

        wagondata = pd.DataFrame(wagondata,columns=['GenStationID', 'GenStationName', 'OpenBal', 'Receipts', 'Tippled', 'Pending', 'Date'])

        centralgendata_cum=centralgendata[['CentralStationID','Energy']].groupby(['CentralStationID']).sum()
        centralgendata_cum.rename({'Energy':'MonthCumulative'},inplace=True,axis=1)
        centralgendata_today=centralgendata[centralgendata['Date']==yesterday]
        centralgendata_today=centralgendata_today.merge(centralgendata_cum,how='left',on='CentralStationID')

        schdrwldata_cum=schdrwldata[['StateID','Schedule','Drawl']].groupby(['StateID']).sum()
        schdrwldata_cum.rename({'Schedule':'MonthCumSch','Drawl':'MonthCumDrawl'},inplace=True,axis=1)
        schdrwldata_today=schdrwldata[schdrwldata.Date==yesterday]
        schdrwldata_today=schdrwldata_today.merge(schdrwldata_cum,how='left',on='StateID')
        schdrwldata_today['Diff']=schdrwldata_today['Schedule']-schdrwldata_today['Drawl']
        schdrwldata_today['CumDiff']=schdrwldata_today['MonthCumSch']-schdrwldata_today['MonthCumDrawl']

        thermal=gen_data[gen_data["GenType"] == 'Thermal']

        hydel=gen_data[gen_data["GenType"] == 'Hydel']

        genco=pd.concat([thermal,hydel],axis=0)

        genco_total=genco.sum()

        central_sector=gen_data[gen_data["GenType"] == 'Central Sector']

        lta=gen_data[gen_data["GenType"] == 'LTA']
        
        APISGS=gen_data[gen_data["GenType"] == 'APISGS']

        solar=gen_data[gen_data["GenType"] == 'Private_solar']

        nonconventional=gen_data[gen_data["GenType"] == 'Private_Nonconventional']

        private=gen_data[gen_data["GenType"] == 'Private']

        private_total=pd.concat([private,solar,nonconventional],axis=0)

        state_purchases=gen_data[gen_data["GenType"] == 'State Purchases']

        third_party_purchase=gen_data[gen_data["GenType"] == 'Third Party Purchases']

        third_party_sales=gen_data[gen_data["GenType"] == 'Third Party Sales']

        gen_total=pd.concat([genco_total,central_sector,lta,APISGS,private_total,state_purchases,third_party_purchase,third_party_sales],axis=0)
        gen_total=gen_total[['InstalledCap','MorningPeak','EveningPeak','Energy','PrevEnergy']].sum()
       
        pump=gen_data[gen_data["GenType"] == 'Pump']

        pump_total=pump[['InstalledCap','MorningPeak','EveningPeak','Energy','PrevEnergy']].sum()

        gen_total_wo_pump=gen_total.sub(pump_total)

        load_factor=(gen_total_wo_pump["Energy"]*1000*100/24/gen_total_wo_pump["InstalledCap"]).round(2)


        instance, created = DemandData.objects.get_or_create(GenStationID=39, Date=yesterday)
        instance.Energy = load_factor
        instance.save()

        subindex=['i','ii','iii','iv','v','vi','vii','viii']

    

    # Create the report content as a string
    report_content = f"""
                 TRANSMISSION CORPORATION OF TELANGANA LTD
               GRID OPERATION -- FINAL REPORT FOR {yesterday.strftime('%d/%m/%Y')}
===============================================================================
                          Generation at Peak Demand in MW     Generation In MU  
Sl Generating                 Morning     Evening          {yesterday.strftime('%A')}{' '*(10-len(yesterday.strftime('%A')))} | {previous_year_day.strftime('%A')}
No Station            {gridfreq_data.iloc[0,0]:.2f}HZ/{gridfreq_data.iloc[0,2].strftime('%H:%M')}Hrs  {gridfreq_data.iloc[0,1]:.2f}HZ/{gridfreq_data.iloc[0,3].strftime('%H:%M')}Hrs  {yesterday.strftime('%d/%m/%Y')}  |  {previous_year_day.strftime('%d/%m/%Y')}
                    INS.CAP    (EX-BUS)    (EX-BUS)         (EX-BUS)  | (EX-BUS)
---------------------(MW)-------------------------------------------------------
(1)   (2)                         (3)          (4)              (5)         (6)
--------------------------------------------------------------------------------
 I) TS GENCO"""

    # Add the data rows to the report content
    for i in range(hydel.shape[0]):
      row_content = f"""
      {hydel.iloc[i,0]:<17}{hydel.iloc[i,2]:>10}{hydel.iloc[i,3]:>12}{hydel.iloc[i,4]:>12}{hydel.iloc[i,5]:>12}|{hydel.iloc[i,6]}"""
      report_content += row_content

    row_content = f"""
        TS Hydel-->    {hydel["InstalledCap"].sum():>10}{hydel["MorningPeak"].sum():>12}{hydel["EveningPeak"].sum():>12}{hydel["Energy"].sum():>12}|{hydel["PrevEnergy"].sum()}
        """       
    report_content += row_content


    for i in range(thermal.shape[0]):
      row_content = f"""
      {thermal.iloc[i,0]:<17}{thermal.iloc[i,2]:>10}{thermal.iloc[i,3]:>12}{thermal.iloc[i,4]:>12}{thermal.iloc[i,5]:>12}|{thermal.iloc[i,6]}"""
      report_content += row_content

    row_content = f"""
        TS Thermal-->  {thermal["InstalledCap"].sum():>10}{thermal["MorningPeak"].sum():>12}{thermal["EveningPeak"].sum():>12}{thermal["Energy"].sum():>12}|{thermal["PrevEnergy"].sum()}"""       
    report_content += row_content

    row_content = f"""

        TSGENCO Total->{genco["InstalledCap"].sum():>10}{genco["MorningPeak"].sum():>12}{genco["EveningPeak"].sum():>12}{genco["Energy"].sum():>12}|{genco["PrevEnergy"].sum()}"""       
    report_content += row_content

    for i in range(lta.shape[0]):
      row_content = f"""
      {lta.iloc[i,0]:<17}{lta.iloc[i,2]:>10}{lta.iloc[i,3]:>12}{lta.iloc[i,4]:>12}{lta.iloc[i,5]:>12}|{lta.iloc[i,6]}"""
      report_content += row_content

    row_content = f"""
II CENTRAL SECTOR"""       
    report_content += row_content
    row_content = f"""
      {central_sector.iloc[0,0]:<17}{central_sector.iloc[0,2]:>10}{central_sector.iloc[0,3]:>12}{central_sector.iloc[0,4]:>12}{central_sector.iloc[0,5]:>12}|{central_sector.iloc[0,6]}"""
    report_content += row_content

    row_content = f"""
III TSSHARE OF APISGS->{APISGS.iloc[0,2]:>10}{APISGS.iloc[0,3]:>12}{APISGS.iloc[0,4]:>12}{APISGS.iloc[0,5].round(2):>12}|{APISGS.iloc[0,6]}"""       
    report_content += row_content

    row_content = f"""


                 TRANSMISSION CORPORATION OF TELANGANA LTD
               GRID OPERATION -- FINAL REPORT FOR {today.strftime('%d/%m/%Y')}
===============================================================================
                          Generation at Peak Demand in MW     Generation In MU  
Sl Generating                 Morning     Evening          {yesterday.strftime('%A')}{' '*(10-len(yesterday.strftime('%A')))} | {previous_year_day.strftime('%A')}
No Station            {gridfreq_data.iloc[0,0]:.2f}HZ/{gridfreq_data.iloc[0,2].strftime('%H:%M')}Hrs  {gridfreq_data.iloc[0,1]:.2f}HZ/{gridfreq_data.iloc[0,3].strftime('%H:%M')}Hrs  {yesterday.strftime('%d/%m/%Y')}  |  {previous_year_day.strftime('%d/%m/%Y')}
                    INS.CAP    (EX-BUS)    (EX-BUS)         (EX-BUS)  | (EX-BUS)
---------------------(MW)-------------------------------------------------------
(1)   (2)                         (3)          (4)              (5)         (6)
--------------------------------------------------------------------------------
"""
    report_content += row_content

    row_content = f"""
IV  PRIVATE SECTOR"""       
    report_content += row_content
    for i in range(private.shape[0]):
      row_content = f"""{private.iloc[i,0]:<20}{private.iloc[i,2]:>10}{private.iloc[i,3]:>12}{private.iloc[i,4]:>12}{private.iloc[i,5]:>12}|{private.iloc[i,6]:>12}"""
      report_content += row_content

    return 0

    row_content = f"""
      SOLAR             {solar["InstalledCap"].sum():>12}{' ':12}{' ':12}{solar["Energy"].sum().round(2):>12}|{solar["PrevEnergy"].sum():>12}"""       
    report_content += row_content
    for i in range(solar.shape[0]):
      row_content = f"""
       {subindex[i]}){' '*(1-i)}{solar.iloc[i,0]:<16}{solar.iloc[i,2]:>10}{solar.iloc[i,3]:>12}{solar.iloc[i,4]:>12}{solar.iloc[i,5]:>12}|{solar.iloc[i,6]:>12}"""
      report_content += row_content

    row_content = f"""
      NONCONVENTIONAL   {nonconventional["InstalledCap"].sum():>12}{' ':12}{' ':12}{nonconventional["Energy"].sum().round(2):>12}|{nonconventional["PrevEnergy"].sum():>12}"""       
    report_content += row_content
    for i in range(nonconventional.shape[0]):
      row_content = f"""
       {subindex[i]}){' '*(1-i)}{nonconventional.iloc[i,0]:<16}{nonconventional.iloc[i,2]:>10}{nonconventional.iloc[i,3]:>12}{nonconventional.iloc[i,4]:>12}{nonconventional.iloc[i,5]:>12}|{nonconventional.iloc[i,6]:>12}"""
      report_content += row_content
 
    row_content = f"""
      PVT SECTOR TOTAL    {private_total["InstalledCap"].sum().round(2):>10}{' ':12}{' ':12}{private_total["Energy"].sum().round(2):>12}|{private_total["PrevEnergy"].sum():>12}"""       
    report_content += row_content

    row_content = f"""

V   STATE PURCHASES         {state_purchases["InstalledCap"].sum().round(2):>8}{' ':12}{' ':12}{state_purchases["Energy"].sum().round(2):>12}|{state_purchases["PrevEnergy"].sum():>12}"""       
    report_content += row_content

    for i in range(state_purchases.shape[0]):
      row_content = f"""
      {subindex[i]}){' '*(2-i)}{state_purchases.iloc[i,0]:<16}{state_purchases.iloc[i,2]:>10}{state_purchases.iloc[i,3]:>12}{state_purchases.iloc[i,4]:>12}{state_purchases.iloc[i,5]:>12}|{state_purchases.iloc[i,6]:>12}"""
      report_content += row_content

    row_content = f"""

VI  THIRD PARTY PURCHASES {third_party_purchase.iloc[0,2]:>10}{third_party_purchase.iloc[0,3]:>12}{third_party_purchase.iloc[0,4]:>12}{third_party_purchase.iloc[0,5].round(2):>12}|{third_party_purchase.iloc[0,6]:>12}"""
    report_content += row_content

    row_content = f"""

VII THIRD PARTY SALES     {third_party_sales.iloc[0,2]:>10}{third_party_sales.iloc[0,3]:>12}{third_party_sales.iloc[0,4]:>12}{third_party_sales.iloc[0,5].round(2):>12}|{third_party_sales.iloc[0,6]:>12}"""
    report_content += row_content

    row_content = f"""

VIII TOTAL DEMAND & CONSUMP {gen_total["InstalledCap"]:>8}{gen_total["MorningPeak"]:>12}{gen_total["EveningPeak"]:>12}{gen_total["Energy"].round(2):>12}|{gen_total["PrevEnergy"]:>12}
        (WITH PUMPS)"""
    report_content += row_content

    row_content = f"""

IX  {pump.iloc[0,0]:<20}{' ':>12}{pump.iloc[0,3]:>12}{pump.iloc[0,4]:>12}{pump.iloc[0,5]:>12}|{pump.iloc[0,6]:>12}
    """
    report_content += row_content

    row_content = f"""

X   {pump.iloc[1,0]:<20}{' ':>12}{pump.iloc[1,3]:>12}{pump.iloc[1,4]:>12}{pump.iloc[1,5]:>12}|{pump.iloc[1,6]:>12}
    """
    report_content += row_content

    row_content = f"""
XI  TS DEMAND(EX-BUS)     {gen_total_wo_pump["InstalledCap"]:<10}{gen_total_wo_pump["MorningPeak"]:>12}{gen_total_wo_pump["EveningPeak"]:>12}{'':>12}|{gen_total_wo_pump["PrevEnergy"]:>12}
         ENERGY (MU)      {'':>10}{'':>12}{'':>12}{gen_total_wo_pump["Energy"]:>12}|{gen_total_wo_pump["PrevEnergy"]:>12}"""
    report_content += row_content

    row_content = f"""
XII LOAD FACTOR        {'':<12}{'':>12}{'':>12}{load_factor:>12}%|{gen_data[gen_data['GenStationID']==39][['PrevEnergy']].iloc[0,0]:>12}%
"""
    report_content += row_content





    row_content = f"""

            {'':<13}CENTRAL PROJECTS GENERATION (MU)
            {'':<13}===========================================
            {'':<13}{'Station':<13}{'Generation':<13}{'Month':<13}
            {'':<13}{'':<13}{'On Date':<13}{'Cumulative':<13}
            {'':<13}-------------------------------------------"""       
    report_content += row_content

    for i in range(centralgendata_today.shape[0]):
      row_content = f"""
            {'':<13}{centralgendata_today.iloc[i,1]:<15}{centralgendata_today.iloc[i,2]:>10}{centralgendata_today.iloc[i,4]:>10}"""
      report_content += row_content

    row_content = f"""

    TOTAL SCHEDULES & DRAWALS FROM CENTRAL NETWORK INCLUDING CENTRAL GENERATING STATIONS (MU)
    ================================================================================
    {'State':^13}{'Energy':<12}{'Actual':<12}{'Excess/':<12}{'Cumulative for the Month/':<24}{'Cum Excess/':<12}
    {'':^13}{'Scheduled':<12}{'Util.':<12}{'Deficit':<12}{'Share':<12}{'Utilisation':<12}{'Deficit':<12}
    --------------------------------------------------------------------------------"""       
    report_content += row_content

    for i in range(schdrwldata_today.shape[0]):
      row_content = f"""
      {schdrwldata_today.iloc[i,1]:<15}{schdrwldata_today.iloc[i,2]:>10}{schdrwldata_today.iloc[i,3]:>10}{schdrwldata_today.iloc[i,7]:>10}{schdrwldata_today.iloc[i,5]:>10}{schdrwldata_today.iloc[i,6]:>10}{schdrwldata_today.iloc[i,8]:>10}"""
      report_content += row_content

    row_content = f"""

            GENERATION SUMMARY AS ON {yesterday.strftime('%d/%m/%Y')} (MU)
    ======================================================================================
    {'TS HYDEL GEN .........':<25}{hydel["Energy"].sum().round(2):>8}{'':<20}{'CGS UTIL............':<25}{central_sector.iloc[0,5]:>8}
    {'TS THERMAL GEN........':<25}{thermal["Energy"].sum().round(2):>8}{'':<20}{'TS SHARE of APISGS..':<25}{APISGS.iloc[0,5]:>8}
    {'TS GENCO TOTAL........':<25}{genco["Energy"].sum().round(2):>8}{'':<20}{'PRIVATE SECTOR......':<25}{private_total["Energy"].sum().round(2):>8}
    {'SINGARENI... .........':<25}{lta.loc[17,'Energy'].round(2):>8}{'':<20}{'STATE PURCHASES.....':<25}{state_purchases["Energy"].sum().round(2):>8}
    {'NTPC TSTPP-U1(INFIRM).':<25}{lta.loc[18,'Energy'].round(2):>8}{'':<20}{'3RD PARTY PURC+SALES':<25}{(third_party_purchase.iloc[0,5]+third_party_sales.iloc[0,5]).round(2):>8}
    {'CHATTISGARH SPDCL.....':<25}{lta.loc[19,'Energy'].round(2):>8}{'':<20}{'SSLB PUMP CONSUMP...':<25}{pump.iloc[0,5]:>8}
    {'':<25}{'':>8}{'':<20}{'NSR PUMP CONSUMP....':<25}{pump.iloc[1,5]:>8}
    {'':<25}{'':>8}{'':<20}{'TOTAL':>25}{gen_total_wo_pump["Energy"]:>8}
    --------------------------------------------------------------------------------------
    
    {'TS GRID DEMAND for {yesterday} (in MU)':<55}:{gen_total_wo_pump["Energy"]:>10}    |{gen_total_wo_pump['PrevEnergy']:>10}
    {'Cumulative for the Month Total (in MU)':<55}:{tsdemand_monthcum[0][0]:>10}    |{gen_data[gen_data['GenStationID']==37][['PrevEnergy']].iloc[0,0]:>10}
    {'Cumulative for the Year Total (in MU) (From 1st April)':<55}:{tsdemand_finyearcum[0][0]:>10}    |{gen_data[gen_data['GenStationID']==38][['PrevEnergy']].iloc[0,0]:>10}
    
    
    
    
    """
    report_content += row_content

    row_content = f"""

                RESERVOIR LEVEL PARTICULARS AS ON {today.strftime('%d/%m/%Y')} (MU)
    =================================================================================================
    {'RESERVOIR':<15}|{'LAST YEAR':^17}|{'THIS YEAR':^17}|{'LEVEL RAISE/':^12}|{'EQUIVALENT':^10}|{'FRL(ft)':^10}|{'MDDL(ft)':^10}
    {'':<15}|{'LEVEL':^8}|{'STORAGE':^8}|{'LEVEL':^8}|{'STORAGE':^8}|{'FALL OVER':^12}|{'ENERGY':^10}|{'':>10}|{'':>10}
    {'':<15}|{'(ft)':^8}|{'(Tmc)':^8}|{'(ft)':^8}|{'(Tmc)':^8}|{'PREV DAY(ft)':^12}|{'(mu)':^10}|{'':>10}|{'':>10}
    -------------------------------------------------------------------------------------------------
"""           
    report_content += row_content

    for i in range(levelstoragedata.shape[0]):
      row_content = f"""    {levelstoragedata.iloc[i,1]:<15}|{levelstoragedata.iloc[i,2]:>8.2f}|{levelstoragedata.iloc[i,3]:>8.2f}|{levelstoragedata.iloc[i,4]:>8.2f}|{levelstoragedata.iloc[i,5]:>8.2f}|{levelstoragedata.iloc[i,6]:>12.2f}|{levelstoragedata.iloc[i,7]:>10.2f}|{levelstoragedata.iloc[i,8]:>10.2f}|{levelstoragedata.iloc[i,9]:>10.2f}
"""
      report_content += row_content


    row_content = f"""

                                    INFLOWS AND DISCHARGES
    ========================================================================================
       {'Inflows in Cusecs @ 06:00 Hrs':^31}  |  {'Discharges in Cusecs':^35}
    ----------------------------------------------------------------------------------------
    1. {'Upper Jurala':<25}{inflowsdischargedata.iloc[0,5]:>6}{'1.':>4}{'Upper Jurala':<6}{dis_ujurala.iloc[0,5]:>25}
       {'':<25}{'':>6}{'':>4}{'Lower Jurala':<25}{dis_ljurala.iloc[0,5]:>6}
    2. {'Srisailam':<25}{'':>6}{'2.':>4}{'Srisailam':<24}
        {inf_srisailam.iloc[0,1]:<24}{inf_srisailam.iloc[0,5]:>6}{'':>5}{dis_srisailam.iloc[0,1]:<24}{dis_srisailam.iloc[0,4]:>6}{dis_srisailam.iloc[0,5]:>13}
        {inf_srisailam.iloc[1,1]:<24}{inf_srisailam.iloc[1,5]:>6}{'':>5}{dis_srisailam.iloc[1,1]:<24}{dis_srisailam.iloc[1,4]:>6}{dis_srisailam.iloc[1,5]:>13}
        {inf_srisailam.iloc[2,1]:<24}{inf_srisailam.iloc[2,5]:>6}{'':>5}{dis_srisailam.iloc[2,1]:<24}{dis_srisailam.iloc[2,4]:>6}{dis_srisailam.iloc[2,5]:>13}
        {inf_srisailam.iloc[3,1]:<24}{inf_srisailam.iloc[3,5]:>6}{'':>5}{dis_srisailam.iloc[3,1]:<24}{dis_srisailam.iloc[3,4]:>6}{dis_srisailam.iloc[3,5]:>13}
        {'':<24}{'':>6}{'':>5}{dis_srisailam.iloc[4,1]:<24}{dis_srisailam.iloc[4,4]:>6}{dis_srisailam.iloc[4,5]:>13}
        {'':<24}{'':>6}{'':>5}{dis_srisailam.iloc[5,1]:<24}{dis_srisailam.iloc[5,4]:>6}{dis_srisailam.iloc[5,5]:>13}
        {'':<24}{'':>6}{'':>5}{dis_srisailam.iloc[6,1]:<24}{dis_srisailam.iloc[6,4]:>6}{dis_srisailam.iloc[6,5]:>13}
        
        {'Total':<24}{inf_srisailam.InfDis06to06.sum():>6}{'':>5}{'Total':<24}{dis_srisailam.InfDis00to24.sum():>6}{dis_srisailam.InfDis06to06.sum():>13}
    3. {"N' Sagar":<25}{'':>6}{'3.':>4}{"N' Sagar":<12}
        {inf_nsagar.iloc[0,1]:<24}{inf_nsagar.iloc[0,5]:>6}{'':>5}{dis_nsagar.iloc[0,1]:<24}{dis_nsagar.iloc[0,4]:>6}{dis_nsagar.iloc[0,5]:>13}
        {inf_nsagar.iloc[1,1]:<24}{inf_nsagar.iloc[1,5]:>6}{'':>5}{dis_nsagar.iloc[1,1]:<24}{dis_nsagar.iloc[1,4]:>6}{dis_nsagar.iloc[1,5]:>13}
        {'Total':<24}{inf_nsagar.InfDis06to06.sum():>6}{'':>5}{dis_nsagar.iloc[2,1]:<24}{dis_nsagar.iloc[2,4]:>6}{dis_nsagar.iloc[2,5]:>13}
    4. {'Pulichintala':<25}{inf_pulichintala.iloc[0,5]:<6}{'':>5}{dis_nsagar.iloc[3,1]:<24}{dis_nsagar.iloc[3,4]:>6}{dis_nsagar.iloc[3,5]:>13}
        {otherdata.iloc[0,1]:<25}{otherdata.iloc[0,3]:>6}{'':>5}{dis_nsagar.iloc[4,1]:<24}{dis_nsagar.iloc[4,4]:>6}{dis_nsagar.iloc[4,5]:>13}
        {otherdata.iloc[1,1]:<25}{otherdata.iloc[1,3]:>6}{'':>5}{dis_nsagar.iloc[5,1]:<24}{dis_nsagar.iloc[5,4]:>6}{dis_nsagar.iloc[5,5]:>13}
        {otherdata.iloc[2,1]:<25}{otherdata.iloc[2,3]:>6}{'':>5}{dis_nsagar.iloc[6,1]:<24}{dis_nsagar.iloc[6,4]:>6}{dis_nsagar.iloc[6,5]:>13}
        {otherdata.iloc[3,1]:<25}{otherdata.iloc[3,3]:>6}{'':>5}{'Total':<24}{dis_nsagar.InfDis00to24.sum():>6}{dis_nsagar.InfDis06to06.sum():>13}




    WEATHER:
        {weatherdata.iloc[0,3]}
        {weatherdata.iloc[1,3]}
        {weatherdata.iloc[2,3]}
        
"""   

    report_content += row_content

    row_content = f"""

    STATUS OF COAL SUPPLIES TO THERMAL STATIONS ON :  {yesterday.strftime('%d/%m/%Y')}

    ===========================================================================
     {'Station':<20}{'Op. Balance':^20}{'Receipts':^20}{'Consumption':^20}{'Balance':^20}{'Average coal':^20} 
     {'':^20}{'(MTs)':^20}{'(MTs)':^20}{'(MTs)':^20}{'(MTs)':^20}{'required/day for':^20}
     {'':^20}{'':^20}{'':^20}{'':^20}{'':^20}{'full Generation(MTs)':^20}
    ---------------------------------------------------------------------------
"""           
    report_content += row_content

    for i in range(coaldata.shape[0]):
      row_content = f"""    {coaldata.iloc[i,1]:<20}{coaldata.iloc[i,2]:>20}{coaldata.iloc[i,3]:>20}{coaldata.iloc[i,4]:20}{coaldata.iloc[i,7]:>20}{coaldata.iloc[i,5]:>20}
"""
      report_content += row_content

    row_content = f"""

                            COAL WAGONS POSITION

   ==========================================================================
     {'Station':<20}{'Op. Balance':^20}{'Receipts':^20}{'Consumption':^20}{'Balance':^20}
   --------------------------------------------------------------------------
"""           
    report_content += row_content

    for i in range(wagondata.shape[0]):
      row_content = f"""    {wagondata.iloc[i,1]:<20}{wagondata.iloc[i,2]:>20}{wagondata.iloc[i,3]:>20}{wagondata.iloc[i,4]:>20}{wagondata.iloc[i,5]:>20}
"""
      report_content += row_content


    # Save the report content to the response
    response.write(report_content)

    return response











