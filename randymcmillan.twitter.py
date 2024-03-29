#!/usr/bin/env python3
# https://github.com/geduldig/TwitterAPI
import sys
import os
import requests
import shutil
import importlib
from importlib.resources import read_text
import time
import blockcypher
import hashlib
import pyjq
# os.environ['PYTHONPATH']
sys.path.append('.')
sys.path.append("/usr/local/lib/python3.10/site-packages")
from TwitterAPI import TwitterAPI

def moveBlockTime():
    try:
        shutil.move(os.getcwd()+"/BLOCK_TIME", os.getcwd()+"/OLD_BLOCK_TIME")
    except:
        f = open("BLOCK_TIME", "w")
        f.write("" + 0 + "\n")
        f.close()

def getMillis():
    global millis
    millis = int(round(time.time() * 1000))
    return millis

def getSeconds():
    global seconds
    seconds = int(round(time.time()))
    return seconds

def blockTime():
    try:
        global block_time
        block_time = blockcypher.get_latest_block_height(coin_symbol='btc')
        global block_height
        block_height = repr(block_time)
        f = open("BLOCK_TIME", "w")
        f.write("" + block_height + "\n")
        f.close()
        return block_time
    except:
        return 0
        pass

def BTC_UNIX_TIME():
    global btc_unix_time
    btc_unix_time = str(blockTime())+":"+str(getSeconds())
    return btc_unix_time

def getData(filename):
    f = open(filename)
    global data
    data = f.read()
    f.close()
    return data

def tweetBlockTime(block_time):
    if (block_time != obt):
        # r = api.request('statuses/update', {'status': block_time+":"+getSeconds })
        r = api.request('statuses/update', {'status': BTC_UNIX_TIME() })
        # print(BTC_UNIX_TIME)
        # exit()
        if (r.status_code == 200):
            print('api.request SUCCESS')
        else:
            print('api.request FAILURE')
    else:
        print('tweetBlockTime() FAILURE')

def getMempoolAPI(url,DATA):
    # print(url)
    with open(DATA, 'wb') as f:
        r = requests.get(url, stream=True)
        f.writelines(r.iter_content(1024))
        response = getData(DATA)
        # print(getData(DATA))
        # print(response)

def searchBitcoin():
    r = api.request('search/tweets', {'q':'bitcoin'})
    for item in r:
        print(item)

BLOCK_TIP_HEIGHT        = os.path.expanduser('./BLOCK_TIP_HEIGHT')
DIFFICULTY              = os.path.expanduser('./DIFFICULTY')
OLD_BLOCK_TIME          = os.path.expanduser('./OLD_BLOCK_TIME')
ACCESS_TOKEN_SECRET     = os.path.expanduser('./twitter_access_tokens/access_token_secret.txt')
ACCESS_TOKEN            = os.path.expanduser('./twitter_access_tokens/access_token.txt')
CONSUMER_API_KEY        = os.path.expanduser('./twitter_access_tokens/consumer_api_key.txt')
CONSUMER_API_SECRET_KEY = os.path.expanduser('./twitter_access_tokens/consumer_api_secret_key.txt')

cak  = getData(CONSUMER_API_KEY)
cask = getData(CONSUMER_API_SECRET_KEY)
at   = getData(ACCESS_TOKEN)
ats  = getData(ACCESS_TOKEN_SECRET)
obt  = getData(OLD_BLOCK_TIME)

api  = TwitterAPI(cak,cask,at,ats)

getMempoolAPI('https://mempool.space/api/v1/difficulty-adjustment', DIFFICULTY)
getMempoolAPI('https://mempool.space/api/blocks/tip/height',        BLOCK_TIP_HEIGHT)
# searchBitcoin()
# print(blockTime())
# print(getMillis())
# print(getSeconds())
# tweetBlockTime(blockTime())
m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
print(m.digest())
# b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
print(m.digest_size)
# 32
print(m.block_size)
# 64
print(m.hexdigest())


def HEX_MESSAGE_DIGEST(recipient, message):
    n = hashlib.sha256()
    n.update(bytes(recipient, 'utf-8'))
    n.update(bytes(message, 'utf-8'))
    n.update(bytes(btc_unix_time, 'utf-8'))
    # print(n.digest())
    # b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
    # print(n.digest_size)
    # 32
    # print(n.block_size)
    # 64
    # print(n.hexdigest())
    return n.hexdigest()


def tweetMessageDigest(block_time):
    if (block_time != obt):

        # r = api.request('statuses/update',
        #                 {'status':
        #                  block_time+":"+getSeconds
        #                  })

        if is_tool('nostril'):
            message = "test twitter/nostr syndication"
            digest = HEX_MESSAGE_DIGEST(GPGID, message)
            r = api.request('statuses/update',
                            {'status':
                             "GPGID:" + GPGID
                             + ':MESSAGE:' + message
                             + ':DIGEST:' + digest
                             + ':TOOL:' + str(is_tool('nostril'))
                             + ':WHICHTOOL:' + str(which_tool('nostril'))
                             + ':BTC:UNIX:' + BTC_UNIX_TIME()
                             })
        else:
            message = "test twitter syndication"
            digest = HEX_MESSAGE_DIGEST(GPGID, message)
            r = api.request('statuses/update',
                            {'status':
                             "GPGID:"+GPGID
                             + ':MESSAGE:' + message
                             + ':DIGEST:' + digest
                             + 'BTC:UNIX:' + BTC_UNIX_TIME()
                             })
        # r = api.request('statuses/update', \
        # {'status': HEX_MESSAGE_DIGEST(GPGID,"test message")})
        # print(BTC_UNIX_TIME)
        # exit()
        if (r.status_code == 200):
            print('api.request SUCCESS')
        else:
            print('api.request FAILURE')

    else:
        print('tweetBlockTime() FAILURE')


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    # from distutils.spawn import find_executable
    # return find_executable(name) is not None
    return which(name) is not None


def which_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    # from distutils.spawn import find_executable
    # return find_executable(name) is not None
    return which(name) # is not None


NOSTRIL = is_tool('nostril')
print(NOSTRIL)
print(BTC_UNIX_TIME())

global GPGID
GPGID = 'BB06757B'
# HEX_MESSAGE_DIGEST(GPGID, "test message")
HEX_MESSAGE_DIGEST(GPGID, str(NOSTRIL))
tweetMessageDigest(blockTime())


