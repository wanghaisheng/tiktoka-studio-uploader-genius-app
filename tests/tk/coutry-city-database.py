import xmltodict
import jsons
def load_json(xml_path):
    #获取xml文件
    xml_file = open(xml_path, 'r',encoding='utf-8')
    #读取xml文件内容
    xml_str = xml_file.read()
    #将读取的xml内容转为json
    json = xmltodict.parse(xml_str)
    return json
filename=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\assets\country-db\qq\en_loclist.xml'
r=load_json(filename)
datas={}
country={}
coutr=[ x['@Name'] for x in r['Location']['CountryRegion']]
for s in r['Location']['CountryRegion']:
    # print(f"country name:{s['@Name']}")
    # print(f"country code:{s['@Code']}")
    countrycode=s['@Code']
    if s['@Code']=='1':
        countrycode='CHN'
    country[countrycode]=s['@Name']

    if 'State' in s:
        datas[countrycode]=s['State']
        states=s['State']
        cities={}
        for c in states:
            print(c['@Name'],c['@Code'])
            if 'City' in c:
                cities[c['@Name']]=c['City']
            else:
                cities[c['@Name']]={}

        datas[countrycode]=cities
    else:
        datas[countrycode]={}    
        print('there is no states')
        # print(s)
# print(coutr)
datas['country']=country
# provinces=[x['@Name'] for x in datas['CHN']]
# print( provinces)
# cities=[x['@Name'] for x in datas['CHN']['@Name'=='Anhui']]

with open('2.json','w') as f:
        f.write(jsons.dumps(datas))      
