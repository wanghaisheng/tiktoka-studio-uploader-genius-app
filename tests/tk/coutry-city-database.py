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
# r=load_json(filename)
# datas={}
# countrycodes={}
# coutr=[ x['@Name'] for x in r['Location']['CountryRegion']]
# for rawcountry in r['Location']['CountryRegion']:
#     print(f'country is {rawcountry} ')
#     countrycode=rawcountry['@Code']
#     if rawcountry['@Code']=='1':
#         countrycode='CHN'

#     countrycodes[countrycode]=rawcountry['@Name']
#     print(f"countrycode:{countrycode}")

#     if 'State' in rawcountry:
#         datas[countrycode]=rawcountry['State']
#         states=rawcountry['State']
#         cities={}
#         print(f'=========there are {len(states)} states are======{states}====')
#         if len(states)==1:
#             statecode='states'

#             for index,s in enumerate(states):
#                 print(f'no {index} state is {s}')
#                 # statecode=s['@Code']
#                 if 'City' in states:
#                     print('-----',states)
#                     for c in states['City']:
#                         print(c)
#                         # print(f"----{len(c['City'])}------{c} {type(c)}")                
#                         cities[c['@Code']]=c['@Name']
#                 else:
#                     cities[s['@Name']]={}
#                     print(cities)
#         else:

#             for index,s in enumerate(states):
#                 print(f'no {index} state is {s}')
#                 statecode=s['@Code']    
#                 print(f'statecode is {statecode}')
#                 cities[statecode]={}

#                 if 'City' in s:
#                     rawcity=s['City']
#                     print(f"there are {len(rawcity)} cities")
#                     if len(rawcity)==1:
#                         cities[statecode][rawcity['@Code']]=rawcity['@Name']
#                     else:
#                         print(f'--rawcity  is ---{rawcity}')
#                         cities[statecode][rawcity['@Code']]=rawcity['@Name']
#                 else:
#                     cities[s['@Name']]={}
#                     print(cities)

#         datas[countrycode]=cities
#     else:
#         datas[countrycode]={}    
#         print('there is no states')
#         # print(s)
# # print(coutr)
# datas['country']=countrycodes
# # provinces=[x['@Name'] for x in datas['CHN']]
# # print( provinces)
# # cities=[x['@Name'] for x in datas['CHN']['@Name'=='Anhui']]

  


import xml.etree.ElementTree as et

tree = et.parse(filename)
# 根节点
root = tree.getroot()
datas={}
countries={}

for states in root:
    print('country is:',states.attrib['Name'],states.attrib['Code'])
    countries[states.attrib['Code']]=states.attrib['Name']
    print(f"country has states:{len(states)}")
    if states.attrib['Name']:
    #     cities={}

    #     datas['CHN']={}
    #     if len(states)==0:

    #         datas['CHN']={}
    #     elif len(states)==1:
    #         tmp=[]
    #         for c in states[0]:
    #             print(c.attrib['Name'],c.attrib['Code'])
    #             tmp.append(c.attrib['Name'])
    #         datas['CHN']['states']=tmp
    #     else:
    #         for s in states:
    #             print('state is ',s.attrib['Name'],s.attrib['Code'])
    #             tmp=[]

    #             for c in s:
    #                 print('city is ',c.attrib['Name'],c.attrib['Code'])

    #                 tmp.append(c.attrib['Name'])
    #             cities[s.attrib['Name']]=tmp
    #         print('cities',cities)
    #         datas['CHN']=cities

    # else:
        cities={}

        datas[states.attrib['Code']]={}
        if len(states)==0:

            datas[states.attrib['Code']]={}
        elif len(states)==1:
            tmp=[]
            for c in states[0]:
                print(c.attrib['Name'],c.attrib['Code'])
                tmp.append(c.attrib['Name'])
            datas[states.attrib['Code']]['states']=tmp
        else:
            for s in states:
                print('state is ',s.attrib['Name'],s.attrib['Code'])
                tmp=[]

                for c in s:
                    print('city is ',c.attrib['Name'],c.attrib['Code'])

                    tmp.append(c.attrib['Name'])
                cities[s.attrib['Name']]=tmp
            print('cities',cities)
            datas[states.attrib['Name']]=cities


datas['countries']=countries
with open('2.json','w') as f:
    f.write(jsons.dumps(datas))    