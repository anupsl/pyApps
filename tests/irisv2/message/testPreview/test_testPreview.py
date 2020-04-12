import pytest

from src.modules.irisv2.message.testAndPreviewDBAssertion import PreviewDBAssertion
from src.modules.irisv2.message.testPreview import TestPreview

@pytest.mark.run(order=49)
class Test_testPreview_UploadList():
    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'SMS', 1),

    ])
    def test_irisv2_message_Sanity_testPreview_mobile_plain_ProdSanity(self, campaignType, testControlType, channel,
                                                            numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'SMS', 1),
        ('LIVE', 'CUSTOM', 'SMS', 1),
        ('LIVE', 'SKIP', 'SMS', 1),
        ('LIVE', 'ORG', 'SMS', 10),
    ])
    def test_irisv2_message_testPreview_mobile_plain(self, campaignType, testControlType, channel,
                                                            numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers,numberOfCustomTag', [
        ('LIVE', 'ORG', 'SMS', 1, 1),
        ('LIVE', 'CUSTOM', 'SMS', 1, 2),
        ('LIVE', 'SKIP', 'SMS', 1, 5),
        ('LIVE', 'ORG', 'SMS', 10, 5)
    ])
    def test_irisv2_message_testPreview_mobile_plain_customTag(self, campaignType, testControlType, channel,
                                                               numberOfIdentifiers, numberOfCustomTag):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers,
                                                                     numberOfCustomTag=numberOfCustomTag)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'EMAIL', 1),
        ('LIVE', 'CUSTOM', 'EMAIL', 1),
        ('LIVE', 'SKIP', 'EMAIL', 1)
    ])
    def test_irisv2_message_testPreview_email_plain(self, campaignType, testControlType, channel,
                                                    numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers,numberOfCustomTag', [
        ('LIVE', 'ORG', 'EMAIL', 1, 1),
        ('LIVE', 'CUSTOM', 'EMAIL', 1, 2),
        ('LIVE', 'SKIP', 'EMAIL', 1, 5)
    ])
    def test_irisv2_message_testPreview_email_plain_customTag(self, campaignType, testControlType, channel,
                                                              numberOfIdentifiers, numberOfCustomTag):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers,
                                                                     numberOfCustomTag=numberOfCustomTag)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'SMS', 1),
        ('LIVE', 'CUSTOM', 'SMS', 1),
        ('LIVE', 'SKIP', 'SMS', 1)
    ])
    def test_irisv2_message_testPreview_mobile_coupons(self, campaignType, testControlType, channel,
                                                       numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers, couponEnabled=True)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers,numberOfCustomTag', [
        ('LIVE', 'ORG', 'SMS', 10, 5)
    ])
    def test_irisv2_message_testPreview_mobile_coupon_customTag(self, campaignType, testControlType, channel,
                                                                numberOfIdentifiers, numberOfCustomTag):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers,
                                                                     numberOfCustomTag=numberOfCustomTag,
                                                                     couponEnabled=True)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'EMAIL', 1),
        ('LIVE', 'CUSTOM', 'EMAIL', 1),
        ('LIVE', 'SKIP', 'EMAIL', 1)
    ])
    def test_irisv2_message_testPreview_email_coupon(self, campaignType, testControlType, channel,
                                                     numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers, couponEnabled=True)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'SMS', 1),
        ('LIVE', 'CUSTOM', 'SMS', 1),
        ('LIVE', 'SKIP', 'SMS', 1)
    ])
    def test_irisv2_message_testPreview_mobile_points(self, campaignType, testControlType, channel,
                                                      numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers, pointsEnabled=True)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,numberOfIdentifiers', [
        ('LIVE', 'ORG', 'EMAIL', 1),
        ('LIVE', 'CUSTOM', 'EMAIL', 1),
        ('LIVE', 'SKIP', 'EMAIL', 1)
    ])
    def test_irisv2_message_testPreview_email_points(self, campaignType, testControlType, channel,
                                                     numberOfIdentifiers):
        testPreviewResponse, testPreviewPayload = TestPreview.create(campaignType, testControlType, channel,
                                                                     numberOfIdentifiers, pointsEnabled=True)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], numberOfIdentifiers).check()
