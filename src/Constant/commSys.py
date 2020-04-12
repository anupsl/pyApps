
class CommSys():

    prodNumbers = { 'prodMobile1' : '919886925833', # for APAC / APAC2 SMS test
                    'prodMobile2' : '917259163604', # for APAC / APAC2 SMS test
                    'prodMobile3' : '8618711873625', # used for China SMS test
                    'prodMobile4' : '447700900077', # used for EU SMS test
                    'prodEmail1' : 'sriharsha.bk@capillarytech.com', 
                    'prodEmail2' : 'vengat.raman@capillarytech.com'}

# file attachment for email
    clusterFileHandle = {
        'nightly' : '8fc97a909e786775a4d5fc4b08ad01255d47683b', 
        'staging': '02a1740c8e61c1898b6d0682cb36669880355cc9',
        'eu' : 'e90eaff119a8e8da9e386c1b7de22f5f09bb0562', 
        'china' : '36f215c12e136e405999626b66fce7a9833f8177',
        'more' : '863d1d74c1a8eeb0ea3e8663da578a88e21441a5', 
        'india' : '1cc92b19c0c9be7f5d0ab29cff1aad4b2bbdf41b'
    }

    dlrUrl = {
        'nightly' : 'http://delvreports.nightly.capillary.in',
        'staging' : 'http://delvreports.staging.capillary.in',
        'more' : 'http://apac2.delvreports.capillarytech.com',
        'india' : 'http://delvreports.capillary.in',
        'china' : 'http://delvreports.capillarytech.cn.com',
        'eu' : 'http://delvreports.capillary.eu'
    }
    dummyGatewayIP = {'nightly' : '0.0.0.0', 'staging' : '0.0.0.0'}
