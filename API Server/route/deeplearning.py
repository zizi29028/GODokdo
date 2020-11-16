from flask import request
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Resource
from utils import *

def route(api):
    deeplearning  = api.namespace('deeplearning', description='인공지능 모델을 작동시키기 위한 API 모음입니다.')
    
    @deeplearning.route('/data/sentences')
    class Resource_translate(Resource):
        @as_json
        @login_required(deeplearning)
        @deeplearning.response(200, 'OK')
        def get(self):
            with OpenMysql() as conn:
                result = conn.execute("SELECT `no`, `contents` FROM `documents` WHERE `status`=%s", 'verified')
                documents = {}
                for i in result:
                    documents[i['no']] = {'no':i['no'], 'contents': i['contents']}

                result = conn.execute("SELECT `documents`.`no`, `code`, `errors`.`text` FROM `documents` JOIN `errors` ON `documents`.`no`=`errors`.`document_no` WHERE `status`=%s", 'verified')
                
                for i in result:
                    if ('errors' not in documents[i['no']]):
                        documents[i['no']]['errors'] = []
                    documents[i['no']]['errors'].append({'code':i['code'], 'keyword':i['text']})
                
                dataset = []
                for i in documents:
                    dataset.append(documents[i])
                return {"list": dataset}, 200