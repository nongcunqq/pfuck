# coding: utf-8

import cgi
import json

from bottle import route, template, request

from utils import log as logger

import configs.main
import configs.communicate
import configs.custom
import work.Register
import work.GetRedBag


@route('/', method='GET')
def index():
    configsSmsFile = cgi.escape(configs.custom.get('smsFile', ''))
    return template('tpl/index.html', htmlTitle=configs.main.APP_NAME, configsSmsFile=configsSmsFile)

@route('/getRedBag', method='GET')
def getRedBag():
    configsSmsFile = cgi.escape(configs.custom.get('smsFile', ''))
    return template('tpl/getRedBag.html', htmlTitle=configs.main.APP_NAME, configsSmsFile=configsSmsFile)

@route('/startRedBag', method="POST")
def startRedBag():
    workId = request.POST.get('id', '').strip()
    phoneNum = request.POST.get('phoneNum', '').strip()
    links = request.POST.get('links', '').strip()

    fetchVcode = request.POST.get('fetchVcode', '').strip()

    work.GetRedBag.GetRedBag(
        workId,
        phoneNum,
        links.split('\n'),
        fetchVcode == 'on'
    ).run()

@route('/start', method="POST")
def start():
    workId = request.POST.get('id', '').strip()
    phoneNum = request.POST.get('phoneNum', '').strip()
    reg = request.POST.get('reg', '').strip()
    getGift = request.POST.get('getGift', '').strip()
    makeRedBagLink = request.POST.get('makeRedBagLink', '').strip()
    fetchVcode = request.POST.get('fetchVcode', '').strip()

    work.Register.Register(
        workId,
        phoneNum,
        reg == 'on',
        getGift == 'on',
        makeRedBagLink == 'on',
        fetchVcode == 'on'
    ).run()

    return {
        'status': 'ok',
        'info': 'ok',
        'id': workId,
    }

@route('/log', method="GET")
def log():
    queryStr = request.GET.get('query', '').strip()

    query = json.loads(queryStr)

    result = {}
    for workId, offset in query.items():
        result[workId] = logger.readRecent(workId, offset)

    return result

@route('/communicate', method="POST")
def communicate():
    workId = request.POST.get('id', '').strip()
    key = request.POST.get('key', '').strip()
    value = request.POST.get('value', '').strip()

    configs.communicate.set(workId, key, value)

    return {
        'status': 'ok',
        'info': 'ok',
    }

@route('/saveConfig', method="POST")
def saveConfig():
    args = request.POST.decode('utf-8')
    for key, value in args.items():
        configs.custom.set(key, value)

    return {
        'status': 'ok',
        'info': 'ok',
    }

