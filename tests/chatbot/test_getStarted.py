import pytest , logging
from src.modules.social.chatbot import chatbotComponents
from src.Constant.constant import constant

@pytest.mark.chatbot
@pytest.mark.getStarted
def get_started(initializer, loader):
    log = logging.getLogger('get_started')
    message = 'Get Started'
    gatewayresponse = initializer.get('gateway').sendTextMessage(message)
    
    if gatewayresponse.response == 'success':
        log.info('Response for sentTextMessage made for get started was success')
        machine1 = constant.config['shard1']
        machine2 = constant.config['shard2']
        result = chatbotComponents.getchatThreadIDs(loader.get('recipient_id'), loader.get('page_id'), machine1)
    else:
        assert False, 'Gateway Response was not Success :' + str(gatewayresponse)
