import pytest,copy

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger
from src.modules.irisv2.list.createAudience import CreateAudience
from src.dbCalls.campaignShard import list_Calls


@pytest.mark.run(order=50)
class Test_createMessage_Negative_MobilePush_Validations():

        def setup_class(self):
            constant.config.update({'node': copy.deepcopy(constant.node)})
            self.actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            self.actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])
            self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')


        def teardown_class(self):
            IrisHelper.updateOrgId(self.actualOrgId)
            IrisHelper.updateOrgName(self.actualOrgName)

        def setup_method(self, method):
            Logger.logMethodName(method.__name__)




        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
         ])

        def test_irisv2_message_create_negative_mobilePush_ContentType_Invalidandroid_type(self, campaignType,
                                                                                        testControlType,
                                                                                        listType,
                                                                                            channel, messageInfo):
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400,expectedErrorCode=[104],
                                         expectedErrorMessage=["Invalid request : type , Unknown value , allowed values are [TEXT, IMAGE]"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_InvalidiOS_type(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel, messageInfo):
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                             "Invalid request : type , Unknown value , allowed values are [TEXT, IMAGE]"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_Invaliddevice_type(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType,testControlType,messageInfo,self.listInfo,channel)
            content['messageContent']["message_content_id_1"]['androidContent'].update({"deviceType": ""})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                             "Invalid request : deviceType , Unknown value , allowed values are [ANDROID, IOS]"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_iOS_Invaliddevice_type(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent'].update({"deviceType": ""})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                             "Invalid request : deviceType , Unknown value , allowed values are [ANDROID, IOS]"])


        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_InvalideStyle(self, campaignType,
                                                                                                 testControlType,
                                                                                                 listType,
                                                                                                 channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent']["expandableDetails"].update({'style': 'BIG'})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                             "Invalid request : style , Unknown value BIG, allowed values are [BIG_TEXT, BIG_PICTURE]"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_IOS_InvalideStyle(self, campaignType,
                                                                                             testControlType,
                                                                                             listType,
                                                                                             channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent']["expandableDetails"].update(
                {'style': 'BIG'})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                                                  "Invalid request : style , Unknown value BIG, allowed values are [BIG_TEXT, BIG_PICTURE]"])


        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_IOS_WithoutImage_link(self, campaignType,
                                                                                            testControlType,
                                                                                            listType,
                                                                                            channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent']["expandableDetails"].update(
                {'image': ''})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : Image url not found for image type Mobile Push content."])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_WithoutImage_link(self, campaignType,
                                                                                             testControlType,
                                                                                             listType,
                                                                                             channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent']["expandableDetails"].update(
                {'image': ''})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : Image url not found for image type Mobile Push content."])



        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_IOS_WithoutstyleField(self, campaignType,
                                                                                                testControlType,
                                                                                                listType,
                                                                                                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent']["expandableDetails"].pop("style")

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Style must pe given."])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_android_WithoutstyleField(self, campaignType,
                                                                                             testControlType,
                                                                                             listType,
                                                                                             channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent']["expandableDetails"].pop("style")

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Style must pe given."])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_IOS_WithoutDeviceTypeField(self, campaignType,
                                                                                                testControlType,
                                                                                                listType,
                                                                                                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent'].pop("deviceType")

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Device type is required"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_android_WithoutDeviceTypeField(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent'].pop("deviceType")

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Device type is required"])



        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_IOS_Withoutmessage(self, campaignType,
                                                                                              testControlType,
                                                                                              listType,
                                                                                              channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent'].pop("message")
            Logger.log(content)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Message is required"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_Withoutmessage(self, campaignType,
                                                                                          testControlType,
                                                                                          listType,
                                                                                          channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent'].pop("message")
            Logger.log(content)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Message is required"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_IOS_Withouttitle(self, campaignType,
                                                                                      testControlType,
                                                                                      listType,
                                                                                      channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['iosContent'].pop("title")
            Logger.log(content)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Title is required"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_Withouttitle(self, campaignType,
                                                                                        testControlType,
                                                                                        listType,
                                                                                        channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent'].pop("title")

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Title is required"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Invalid_StoreTYpe(self, campaignType,
                                                                                            testControlType,
                                                                                            listType,
                                                                                            channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"].update({'storeType': 'ABC'})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                             "Invalid request : storeType , Unknown value ABC, allowed values are [REGISTERED_STORE, LAST_TRANSACTED_AT]"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Invalid_accountId(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"].update({'accountId': 1})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048,3045],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : no channel configs for accountId mentioned in content 1","Audience exception: group not found"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_without_accountId(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"].pop('accountId')

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3045,102,3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : AccountId is required.","Audience exception: group not found"])


        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": "https"},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])


        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_dataType_value(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)


            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                         expectedErrorMessage=[
                                             "Invalid request : type , Unknown value h, allowed values are [DEEP_LINK, EXTERNAL_URL]"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": ['EXTERNAL_URL',
                                                                                                       'https']},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_android_Primary_External_value(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)


            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : URL provided in CTA must be valid url"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value":
                                                                                                          [['Reply','EXTERNAL_URL',
                                                                                                           'https']]},
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": None
                                                                                                           },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_android_Secondary_External_value(self,
                                                                                                                   campaignType,
                                                                                                                   testControlType,
                                                                                                                   listType,
                                                                                                                   channel,
                                                                                                                   messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : URL provided in CTA must be valid url"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value":[['Send',
                                                                                                              'DEEP_LINK',
                                                                                                                 '18dfbbcc'
                                                                                                              ]] },
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                           },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_android_secondary_DeepLink_value(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)


            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048,3045],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : No deep link found in account {} with base url 18dfbbcc".format(content['messageContent']['message_content_id_1']['accountId']),"Audience exception: group not found"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                        },
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": [
                                                                                                            'DEEP_LINK',
                                                                                                            'a'
                                                                                                            '18dfbbcc'
                                                                                                            ]
                                                                                                   },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_android_primary_DeepLink_value(
                self, campaignType,
                testControlType,
                listType,
                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : No deep link found in account {} with base url a18dfbbcc".format(content['messageContent']['message_content_id_1']['accountId'])])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": [
                                                                                                           'DEEP_LINK',
                                                                                                           'a'
                                                                                                           'a18dfbbc'
                                                                                                       ]},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_ios_primary_DeepLink_value(
                self, campaignType,
                testControlType,
                listType,
                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : No deep link found in account {} with base url aa18dfbbc".format(content['messageContent']['message_content_id_1']['accountId'])])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": [
                                                                                                           'EXTERNAL_URL',
                                                                                                           'https']},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_iOS_Primary_External_value(self,
                                                                                                                   campaignType,
                                                                                                                   testControlType,
                                                                                                                   listType,
                                                                                                                   channel,
                                                                                                                   messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : URL provided in CTA must be valid url"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value":None
                                                                                                           },
                                                                                                   "primary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value":
                                                                                                           [['Reply',
                                                                                                             'EXTERNAL_URL',
                                                                                                             'https',None]]},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_iOS_Secondary_External_value(
                self,
                campaignType,
                testControlType,
                listType,
                channel,
                messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : URL provided in CTA must be valid url"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value":[['Send',
                                                                                                              'DEEP_LINK',
                                                                                                                 '15',
                                                                                                                 constant.config['iosSecondaryLink']['templateCtaId']

                                                                                                              ]]
                                                                                                   },
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_with_invalid_ios_secondary_DeepLink_value(
                self, campaignType,
                testControlType,
                listType,
                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            Logger.log('check this please',content['messageContent']['message_content_id_1']['accountId'])

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : No deep link found in account {} with base url 15".format(content['messageContent']['message_content_id_1']['accountId'])])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": [['SEND',
                                                                                                                  'DEEP_LINK',
                                                                                                                  'Auto Link',
                                                                                                                  'test'
                                                                                                                 ]]},

                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_invalid_templateId_ios_secondary_Deeplink(
                self, campaignType,
                testControlType,
                listType,
                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : Template id test not valid for category Id {}".format(constant.config['iosSecondaryLink']['categoryId'])])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": True,
                                                                                                       "value": [['SEND',
                                                                                                                  'DEEP_LINK',
                                                                                                                  'Auto Link',
                                                                                                                  None]]},


                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None
                                                                                                   },
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_without_templateId_ios_secondary_Deeplink(
                self, campaignType,
                testControlType,
                listType,
                channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3048],
                                         expectedErrorMessage=[
                                             "Invalid mobile push content : Template id should not be null or empty for category Id {}".format(constant.config['iosSecondaryLink']['categoryId'])])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])

        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_empty_title(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent'].update({"title": ""})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102,104],
                                         expectedErrorMessage=[
                                             "Invalid request : Title is required"])

        @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
            ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                               "android": {
                                                                                                   "contentType": "TEXT",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False},
                                                                                               "ios": {
                                                                                                   "contentType": "IMAGE",
                                                                                                   "secondary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "primary_cta": {
                                                                                                       "enable": False,
                                                                                                       "value": None},
                                                                                                   "custom": False}},
              'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
        ])
        def test_irisv2_message_create_negative_mobilePush_ContentType_Android_empty_message(self, campaignType,
                                                                                           testControlType,
                                                                                           listType,
                                                                                           channel, messageInfo):
            content = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, self.listInfo, channel)
            content['messageContent']["message_content_id_1"]['androidContent'].update({"message": ""})

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  payload=content,
                                                  updateNode=True, lockNode=True)

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102,104],
                                         expectedErrorMessage=[
                                             "Invalid request : Message is required"])
