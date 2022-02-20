#!/usr/bin/env python3

# https://github.com/geduldig/TwitterAPI
import sys
import os
import logging
import hashlib
# import importlib
# from importlib.resources import read_text
# import json
# import pickle
import shutil
import time
import requests
import blockcypher
import unix_time
# import pyjq
# import gnupg



# os.environ['PYTHONPATH']
sys.path.append('.')
sys.path.append("/usr/local/lib/python3.7/site-packages")
from TwitterAPI import TwitterAPI

# Setup logging
global LOGGER
LOGGER = True
logging.basicConfig(level=logging.INFO ,format='%(asctime)s %(message)s', datefmt='%j.%Y %I:%M:%S %p')
logger = logging.getLogger()

global CONFIG
CONFIG                  = str('twitter_access_tokens')
global SESSION_ID_LOCK
SESSION_ID_LOCK        = os.path.expanduser(os.getcwd()+'/SESSION_ID_LOCK')
global BLOCK_TIP_HEIGHT
BLOCK_TIP_HEIGHT        = os.path.expanduser(os.getcwd()+'/BLOCK_TIP_HEIGHT')
global DIFFICULTY
DIFFICULTY              = os.path.expanduser(os.getcwd()+'/DIFFICULTY')
global OLD_BLOCK_TIME
OLD_BLOCK_TIME          = os.path.expanduser(os.getcwd()+'/OLD_BLOCK_TIME')
global ACCESS_TOKEN_SECRET
ACCESS_TOKEN_SECRET     = os.path.expanduser(os.getcwd()+'/'+CONFIG+'/access_token_secret.txt')
global ACCESS_TOKEN
ACCESS_TOKEN            = os.path.expanduser(os.getcwd()+'/'+CONFIG+'/access_token.txt')
global CONSUMER_API_KEY
CONSUMER_API_KEY        = os.path.expanduser(os.getcwd()+'/'+CONFIG+'/consumer_api_key.txt')
global CONSUMER_API_SECRET_KEY
CONSUMER_API_SECRET_KEY = os.path.expanduser(os.getcwd()+'/'+CONFIG+'/consumer_api_secret_key.txt')
global DIGEST
DIGEST = ""
global DATA
DATA = ""

def getData(filename):
    f = open(filename)
    DATA = str(f.read())
    f.close()
    # if (LOGGER): print(DATA) #unsecure
    return DATA


cak  = getData(CONSUMER_API_KEY)
cask = getData(CONSUMER_API_SECRET_KEY)
at   = getData(ACCESS_TOKEN)
ats  = getData(ACCESS_TOKEN_SECRET)
obt  = getData(OLD_BLOCK_TIME)

try:
    session_id_lock  = getData(SESSION_ID_LOCK)
    if (session_id_lock == str(0)): logger.info(session_id_lock+"eq")
    if (session_id_lock != str(0)): logger.info(session_id_lock+"neq")
except:
    logger.info(session_id_lock+"except")

api  = TwitterAPI(cak,cask,at,ats)
if (LOGGER): print(api)

def moveBlockTime():
    try:
        shutil.move(os.getcwd()+"/BLOCK_TIME", os.getcwd()+"/OLD_BLOCK_TIME")
    except:
        logger.info("moveBlockTime() failed!")
        f = open("BLOCK_TIME", "w")
        f.write("" + 0 + "\n")
        f.close()
        pass

def getMillis():
    global millis
    millis = int(round(time.time() * 1000))
    return millis

def getSeconds():
    global seconds
    seconds = int(round(time.time()))
    return seconds

def blockTime():
    global block_time
    global block_height
    try:
        block_time = blockcypher.get_latest_block_height(coin_symbol='btc')
        block_height = repr(block_time)
        f = open("BLOCK_TIME", "w")
        f.write("" + block_height + "\n")
        f.close()
        return block_time
    except:
        return 0
        pass

def BTC_TIME():
    global btc_time
    btc_time = str(blockTime())
    return btc_time

def BTC_UNIX_TIME_MILLIS():
    global btc_unix_time_millis
    global SESSION_ID
    btc_unix_time_millis = str(BTC_TIME())+":"+str(getMillis())
    SESSION_ID = btc_unix_time_millis
    f = open("SESSION_ID", "w")
    f.write("" + SESSION_ID + "\n")
    f.close()
    f = open("SESSION_ID.lock", "w")
    f.write("" + SESSION_ID + "\n")
    f.close()
    return btc_unix_time_millis

def BTC_UNIX_TIME_SECONDS():
    global btc_unix_time_seconds
    btc_unix_time_seconds = str(BTC_TIME())+":"+str(getSeconds())
    return btc_unix_time_seconds

def UNIX_TIME_MILLIS():
    global unix_time_millis
    unix_time_millis = str(getMillis())
    return unix_time_millis

def UNIX_TIME_SECONDS():
    global unix_time_seconds
    unix_time_seconds = str(getSeconds())
    return unix_time_seconds

def tweet_blocktime():
    if BTC_TIME() != obt:
        request = api.request('statuses/update', {'status': BTC_UNIX_TIME_MILLIS()})
        if (LOGGER): logger.info(request)
        if (request.status_code == 200):
            logger.info('api.request SUCCESS')
        else:
            logger.info('api.request FAILURE')
    else:
        logger.info('tweetBlockTime() FAILURE')

def getMempoolAPI(url,DATA):
    if (LOGGER): logger.info(url)
    with open(DATA, 'wb') as f:
        request = requests.get(url, stream=True)
        f.writelines(request.iter_content(1024))
        response = getData(DATA)
        if (LOGGER): logger.info(getData(DATA))
        if (LOGGER): logger.info(response)

def searchGPGR(GPGR):
    try:
        global r
        request = api.request('search/tweets', {'q':GPGR})
        try:
            with open(GPGR+"_"+btc_unix_time_millis, 'w+') as f:
                f.write(request.text)
                f.close
        except:
            logger.info("TRY GPGR FAILED!")
            pass
    except:
        logger.info("GPGR SEARCH FAILED!")
        pass

def searchGPGS(GPGS):
    try:
        global s
        s = api.request('search/tweets', {'q':GPGS})
        try:
            with open(GPGS+"_"+btc_unix_time_millis, 'w+') as f:
                f.write(s.text)
                f.close
        except:
            logger.info("TRY GPGS FAILED!")
            pass
    except:
        logger.info("GPGS SEARCH FAILED!")
        pass


getMempoolAPI('https://mempool.space/api/v1/difficulty-adjustment', DIFFICULTY)
getMempoolAPI('https://mempool.space/api/blocks/tip/height',        BLOCK_TIP_HEIGHT)

if (LOGGER): logger.info(blockTime())
if (LOGGER): logger.info(getMillis())
if (LOGGER): logger.info(getSeconds())

def test_hash_lib():

    global TEST_256
    TEST_256 = hashlib.sha256()
    # empty string test
    assert TEST_256.digest_size == pow(2,5)
    assert TEST_256.block_size == pow(2,6)
    assert "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" == TEST_256.hexdigest()
    return TEST_256.hexdigest()

def HEX_MESSAGE_DIGEST(recipient, message, sender):

    n_256 = hashlib.sha256()
    # test empty string
    assert n_256.hexdigest() == test_hash_lib()

    if (LOGGER): logger.info("%s",n_256.digest())
    if (LOGGER): logger.info(n_256.hexdigest())
    if (LOGGER): logger.info(n_256.digest_size)
    if (LOGGER): logger.info(n_256.block_size)
    n_256.update(bytes(recipient, 'utf-8'))
    if (LOGGER): logger.info(n_256.digest())
    if (LOGGER): logger.info(n_256.hexdigest())
    if (LOGGER): logger.info(n_256.digest_size)
    if (LOGGER): logger.info(n_256.block_size)
    n_256.update(bytes(message, 'utf-8'))
    if (LOGGER): logger.info(n_256.digest())
    if (LOGGER): logger.info(n_256.hexdigest())
    if (LOGGER): logger.info(n_256.digest_size)
    if (LOGGER): logger.info(n_256.block_size)
    n_256.update(bytes(BTC_UNIX_TIME_MILLIS(), 'utf-8'))
    if (LOGGER): logger.info(n_256.digest())
    if (LOGGER): logger.info(n_256.hexdigest())
    if (LOGGER): logger.info(n_256.digest_size)
    if (LOGGER): logger.info(n_256.block_size)
    n_256.update(bytes(sender, 'utf-8'))
    if (LOGGER): logger.info(n_256.digest())
    if (LOGGER): logger.info(n_256.hexdigest())
    if (LOGGER): logger.info(n_256.digest_size)
    if (LOGGER): logger.info(n_256.block_size)

    if (LOGGER): logger.info(n_256.hexdigest())

    return n_256.hexdigest()

def message_header():
    global HEADER
    # BODY = str(":GPGR:"+GPGR+':DIGEST:'+DIGEST+':BTC:UNIX:'+BTC_UNIX_TIME_MILLIS()+":GPGS:"+GPGS+":")
    HEADER = str(":GPGR:DIGEST:BTC_TIME:UNIX_TIME_MILLIS:GPGS:LOC:")
    if (LOGGER): logger.info(HEADER)
    return HEADER
def message_body():
    LOC="https://github.com/0x20bf-org/0x20bf/blob/main/message_to_7C048F04.txt.gpg"
    DIGEST = HEX_MESSAGE_DIGEST(GPGR, MESSAGE ,GPGS)
    global BODY
    BODY = str(
        ":"+GPGR+
        ':'+DIGEST+
        ':'+BTC_TIME()+":"+UNIX_TIME_MILLIS()+":"+GPGS+":"+LOC+":")
    if (LOGGER): logger.info(BODY)
    return BODY
def tweet_message(block_time):
    header = ""#message_header()
    body = message_body()
    if (LOGGER): logger.info(header+"\n"+body)
    # exit()
    if (block_time != obt):
        request = api.request('statuses/update', {'status': header+"\n"+body})
        if (request.status_code == 200):
            logger.info('api.request SUCCESS')
        else:
            logger.info('api.request FAILURE')
    else:
        logger.info('tweetBlockTime() FAILURE')

# logger.info(BTC_UNIX_TIME_MILLIS())

global GPGR
# GPGR='4DC9817F' #bitkarrot
# GPGR='BB06757B' #RECIPIENT
GPGR='7C048F04'
logger.info(GPGR)
global GPGS
GPGS='BB06757B' #SENDER
logger.info(GPGS)
global MESSAGE
MESSAGE='text human readable message'
if (LOGGER): print(HEX_MESSAGE_DIGEST(GPGR, MESSAGE, GPGS))
HEX_MESSAGE_DIGEST(GPGR, MESSAGE, GPGS)
# tweet_message_digest(blockTime())
# logger.info(str(message_body()))
test_hash_lib()
# tweet_blocktime()
message_header()
message_body()
tweet_message(BTC_TIME())
# searchGPGR(GPGR)
# searchGPGS(GPGS)

