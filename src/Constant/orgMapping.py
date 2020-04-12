from src.Constant.tills import Tills
from src.Constant.loyalty import Loyalty
from src.Constant.orgDetails import OrgDetails
from src.Constant.veneno import Veneno


class OrgMapping(Tills, Loyalty, OrgDetails, Veneno):
    orgMapping = {
        'nightly' : {
            'nsadmin' : {'orgId' : 1773},
            'luci': {'orgId': 50371},
            'darknight': {'orgId': 786},
            'chatbot':{'orgId':591, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':786},
            'peb':{ 'orgId': 794 },  # 840
            'emf':{ 'orgId': 794 },  # 840
            'campaignsui':{'orgId':1193},
            'campaign_shard':{'orgId':1193},
            'veneno':{'orgId':786},
            'iris':{'orgId':786},
            'irisv2':{'orgId':50371},
            'creatives':{'orgId':786},
            'timeline' : {'orgId' : 1193},
            'social' : {'orgId':786}
        },
        'staging' : {
            'nsadmin' : {'orgId' : 1448},
            'luci': {'orgId': 373},
            'darknight': {'orgId': 373},
            'chatbot':{'orgId':591, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':373},
            'peb':{ 'orgId': 549 },
            'emf':{ 'orgId': 50193 },
            'campaignsui':{'orgId':568},
            'campaign_shard':{'orgId':568},
            'veneno':{'orgId':568},
            'iris':{'orgId':373},
            'irisv2':{'orgId':50156},
            'creatives':{'orgId': 373},
            'timeline' : {'orgId' : 373},
            'social' : {'orgId':373}            
        },
        'india' : {
            'nsadmin' : {'orgId' : 1391},
            'chatbot':{'orgId':591, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':998},
            'luci': {'orgId': 998},
            'darknight': {'orgId': 998},
            'peb':{ 'orgId': 927 },
            'emf':{ 'orgId': 927 },
            'campaignsui':{'orgId':998},
            'campaign_shard':{'orgId':998},
            'veneno':{'orgId':998},
            'iris':{'orgId':998},
            'irisv2':{'orgId':1732},
            'creatives':{'orgId': 998},
            'timeline' : {'orgId' : 998},
            'social' : {'orgId':998}            
        },
        'more' : {
            'nsadmin' : {'orgId' : 150531},
            'chatbot':{'orgId':591, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':1346},
            'luci': {'orgId': 150007},
            'darknight': {'orgId': 150007},
            'peb':{ 'orgId': 150442 },
            'emf':{ 'orgId': 150442 },
            'campaignsui':{'orgId':150007},
            'campaign_shard':{'orgId':150007},
            'veneno':{'orgId':150007},
            'iris':{'orgId':150007},
            'irisv2':{'orgId':151115},
            'creatives':{'orgId': 150007},
            'timeline' : {'orgId' : 150007},
            'social' : {'orgId':150007}            
        },
        'eu' : {
            'nsadmin' : {'orgId' : 100254},
            'chatbot':{'orgId':100027, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':100027},
            'luci': {'orgId': 100027},
            'darknight': {'orgId': 100027},
            'peb':{ 'orgId': 100020 },
            'emf':{ 'orgId': 100020 },
            'campaignsui':{'orgId':100027},
            'campaign_shard':{'orgId':100027},
            'veneno':{'orgId':100027},
            'iris':{'orgId':100027},
            'irisv2':{'orgId':100525},
            'creatives':{'orgId': 100027},
            'timeline' : {'orgId' : 100027},
            'social' : {'orgId':100027}
        },
        'china' : {
            'nsadmin' : {'orgId' : 200037},
            'chatbot':{'orgId':591, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':1346},
            'luci': {'orgId': 200021},
            'campaign_shard':{'orgId':200021},
            'peb':{ 'orgId': 200024 },
            'emf':{ 'orgId': 200024 },
            'campaignsui':{'orgId':200021},
            'veneno':{'orgId':200021},
            'iris':{'orgId':200021},
            'irisv2':{'orgId':200021},
            'creatives':{'orgId': 200021},
            'timeline' : {'orgId' : 200021},
            'social' : {'orgId':200021}
        },
        'local':  {
            'nsadmin' : {'orgId' : 0},
            'chatbot':{'orgId':591, 'recipient_id':1421308334574333, 'page_id':253324011815732},
            'marketing':{'orgId':786},
            'campaignsui':{ 'orgId':786 },
            'peb':{ 'orgId':0 },
            'emf':{ 'orgId':0 },
            'iris':{'orgId':0},
            'creatives':{'orgId': 0},
        }        
    }
