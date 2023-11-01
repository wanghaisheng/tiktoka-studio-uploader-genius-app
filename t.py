import xmltodict
import jsons
def load_json(xml_path):
    #获取xml文件
    xml_file = open(xml_path, 'r')
    #读取xml文件内容
    xml_str = xml_file.read()
    #将读取的xml内容转为json
    json = xmltodict.parse(xml_str)
    return json
filename=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\assets\country-db\qq\LocList.xml'
r=load_json(filename)
with open('1.json','w') as f:
        f.write(jsons.dumps(r))      
print(r['Location']['CountryRegion'])