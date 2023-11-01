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
filename=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\assets\country-db\qq\LocList.xml'
r=load_json(filename)
coutr=[ x['@Name'] for x in r['Location']['CountryRegion']]
for c in r['Location']['CountryRegion']:
    if c['@Name']=='美国':
        states=[x['@Name'] for x in c['State']]
        print(states)
# print(coutr)
# with open('1.json','w') as f:
#         f.write(jsons.dumps(r))      
