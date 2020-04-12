from src.initializer.generateThrift import reonDimension
class ReonObject(object):
    def __init__(self):
        self.TMetaClient = {'ETL': 0, 'READ_API': 1, 'WRITE_API': 2, 'ETL_VALIDATOR': 3}
        self.TDimOperationType = {'SEARCH':0,'DISTINCT':1}

    def TDimParams(self,searchText):
        tmpDict = {
            'searchText':searchText,
            'dimConstraints':[]
        }
        return reonDimension.TDimParams(**tmpDict)
