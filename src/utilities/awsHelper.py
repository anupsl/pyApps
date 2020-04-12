from src.Constant.constant import constant
from src.utilities.logger import Logger
import boto3

class AWSHelper():
    
    @staticmethod   
    def downloadFileFromS3(self):
        pass
    
    @staticmethod
    def readFileFromS3(bucketName, keyName):
        bucketName = AWSHelper.updateBucketName(bucketName)
        Logger.log('Reading File from BucketName :{} and keyName :{}'.format(bucketName, keyName))
        session = boto3.Session(aws_access_key_id=constant.awsKey, aws_secret_access_key=constant.awsSecret)
        s3 = session.resource('s3')
        data = s3.Object(bucketName, keyName).get()['Body'].read().decode('utf-8')
        return data.split('\n')

    @staticmethod
    def updateBucketName(bucketName):
        bucketName = bucketName.replace('more', 'sg')
        return bucketName
        
