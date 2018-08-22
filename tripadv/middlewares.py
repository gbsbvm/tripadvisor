# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 17:02:40 2016

@author: giotto
"""
import time
import random
from scrapy.conf import settings

from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

import logging
logger = logging.getLogger(__name__)


class CustomContextFactory(ScrapyClientContextFactory):
    """
    Custom context factory that allows SSL negotiation.
    """

    def __init__(self):
        # Use SSLv23_METHOD so we can use protocol negotiation
        self.method = SSL.SSLv23_METHOD


class RandomUserAgentMiddleware(object):
    '''it takes care of the User agents'''

    def process_request(self, request, spider):
        '''it randomly picks a useragent from the provided list list'''
        with open(settings['USER_AGENT_LIST_FILE'], 'r') as user_agents_list:
         #
            user_agents_list = [line.strip() for line in user_agents_list if line.strip(
            ) if not line.startswith('#')]

            random_user_agent = random.choice(user_agents_list)
            if random_user_agent:
                request.headers["User-Agent"] = random_user_agent
                # this is just to check which user agent is being used for request
#                logger.info('Random User-Agent: {} {}'.format(request.headers.get('User-Agent'), request))


class LimitHandlerMiddleware(object):
    '''It takes care of the server side rate-limits'''

    def process_response(self, request, response, spider):
        '''it put the spider in sleep for 20 minutes if the http response code
        is either 4xx or 5xx '''
        response_status = response.status
    #    logger.info('{} Response status {}'.format(
    #        str(response.url), str(response_status)))
        #if 399 < response_status < 600:
        # 404 is the code for deleted single user pages
        # if response_status != *** and response_status != ***:
        # logger.info('Just hit the limit, pausing for 20 minutes')
        # time.sleep(20 * 60)
        # logger.info('Woke up and back on business')

        return response


class ProxyMiddleware(object):
    '''It takes care of the eventual proxies'''

    def process_request(self, request, spider):
        '''it randomly picks a proxy address from the pool'''
        # http://www.proxynova.com/proxy-server-list/country-fr/
        with open(settings['PROXY_POOL_LIST_FILE'], 'r') as proxy_pool:

            request.meta['proxy'] = random.choice(proxy_pool)
# request.meta['proxy'] ='http://46.232.141.177:8080'#
# random.choice(proxy_pool)

            logger.info('Random Proxy: {} Random User-Agent: {} Request: {}'.format(
                request.meta.get('proxy'), request.headers.get('User-Agent'), request))
