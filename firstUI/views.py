from django.shortcuts import render
import pandas as pd
import pickle
# from sklearn.externals import joblib

file = open('./models/model.pkl', 'rb')
clf = pickle.load(file)
file.close()
# input_features=[100,1,21,1,0]
# modelreload=joblib.load('./models/model.pkl')
# modelreload.predict_proba([input_features])[0][1]
# input_features=[100,1,21,1,0]
# infprob = clf.predict_proba([input_features])[0][1]
# infp=int((infprob)*100)
# print(infp)


df3=pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')

def homepage(request):
    return render(request,'home.html')

def predpage(request):
    return render(request,'predictor.html')

def Infprob(request):
    if(request.method=='POST'):
        # name = str(request.POST.get('name'))
        age = int(request.POST.get('age'))
        # mobile = int(request.POST.get('mobile'))
        fever = int(request.POST.get('fever'))
        pain = int(request.POST.get('pain'))
        runnynose = int(request.POST.get('runnynose'))
        diffbreath = int(request.POST.get('diffbreath'))
        input_features=[fever,pain,age,runnynose,diffbreath]
        infprob = clf.predict_proba([input_features])[0][1]
        infp=int((infprob)*100)

        # temp['age']=request.POST.get('age')
        # temp['mobile']=request.POST.get('mobile')
        # temp['fever']=request.POST.get('fever')
        # temp['pain']=request.POST.get('pain')
        # temp['runnynose']=request.POST.get('runnynose')
        # temp['diffbreath']=request.POST.get('diffbreath')
        return render(request,'show.html',{'inf':infp})
    return render(request,'index.html')




def indexpage(request):
    confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    deathGLobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    recoverGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    totalCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    totaldeath = deathGLobal[confirmedGlobal.columns[-1]].sum()
    totalrecover = recoverGlobal[confirmedGlobal.columns[-1]].sum()
    barplotdata=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barplotdata=barplotdata.reset_index()
    barplotdata.columns=['Country/Region','values']
    barplotdata=barplotdata.sort_values(by='values',ascending=False)
    barplotvals=barplotdata['values'].values.tolist()
    countryNames=barplotdata['Country/Region'].values.tolist()
    dataForMap=mapdata(barplotdata,countryNames)
    showMap='True'
    context={'totalCount':totalCount,'totaldeath':totaldeath,'totalrecover':totalrecover,'countryNames':countryNames,'barplotvals':barplotvals,'dataForMap':dataForMap,'showMap':showMap}
    return render(request,'index.html',context)


def mapdata(barplotdata,countryNames):
    dataForMap=[]
    for i in countryNames:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=barplotdata[barplotdata['Country/Region']==i]['values'].sum()
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    return dataForMap

def indiCountryData(request):
    countryNamse=request.POST.get('countryName')
    confirmedGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',encoding='utf-8',na_values=None)
    deathGLobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    recoverGlobal=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    totalCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    totaldeath = deathGLobal[confirmedGlobal.columns[-1]].sum()
    totalrecover = recoverGlobal[confirmedGlobal.columns[-1]].sum()
    barplotdata=confirmedGlobal[['Country/Region',confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    barplotdata=barplotdata.reset_index()
    barplotdata.columns=['Country/Region','values']
    barplotdata=barplotdata.sort_values(by='values',ascending=False)
    barplotvals=barplotdata['values'].values.tolist()
    countryNames=barplotdata['Country/Region'].values.tolist()
    showMap='False'

    countryDataSpe=pd.DataFrame(confirmedGlobal[confirmedGlobal['Country/Region']==countryNamse][confirmedGlobal.columns[4:-1]].sum()).reset_index()
    countryDataSpe.columns=['country','values']
    countryDataSpe['lagVal']=countryDataSpe['values'].shift(1).fillna(0)
    countryDataSpe['incrementVal']=countryDataSpe['values']-countryDataSpe['lagVal']
    countryDataSpe['rollingMean']=countryDataSpe['incrementVal'].rolling(window=4).mean()
    countryDataSpe=countryDataSpe.fillna(0)
    datasetsForLine=[{'yAxisID': 'y-axis-1','label':'Daily Cumulated Data','data':countryDataSpe['values'].values.tolist(),'borderColor':'#03a9fc','backgroundColor':'#03a9fc','fill':'false'},
                    {'yAxisID': 'y-axis-2','label':'Rolling Mean 4 days','data':countryDataSpe['rollingMean'].values.tolist(),'borderColor':'#fc5203','backgroundColor':'#fc5203','fill':'false'}]
    axisvalues=countryDataSpe.index.tolist()                
    context={'axisvalues':axisvalues,'countryName':countryNamse,'totalCount':totalCount,'totaldeath':totaldeath,'totalrecover':totalrecover,'countryNames':countryNames,'barplotvals':barplotvals,'showMap':showMap,'datasetsForLine':datasetsForLine}
    return render(request,'index.html',context)