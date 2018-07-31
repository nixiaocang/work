from flask import jsonify, Blueprint, request
from myapp_baidu.libs.exceptions import BaseError
from myapp_baidu.libs.const import HttpStatusCode, ResponseCode
from myapp_baidu.main.datasourceservice import DatasourceService
import json

_service = Blueprint('service', __name__)


@_service.route('/saas/readProfileList', methods=["POST"])
def profiles():
    try:
        token_process_info = request.json['tokenProgressInfo']
        response = DatasourceService(token_process_info).get_profiles()
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


@_service.route('/saas/readReportList', methods=["POST"])
def reports():
    try:
        token_process_info = request.json['tokenProgressInfo']
        response = DatasourceService(token_process_info).get_reports()
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


@_service.route('/saas/readMetrics', methods=["POST"])
def metrics():
    try:
        token_process_info = request.json['tokenProgressInfo']
        profile_id = request.json['profileId']
        response = DatasourceService(token_process_info).get_metrics(profile_id)
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


@_service.route('/saas/readDimensions', methods=["POST"])
def dimensions():
    try:
        token_process_info = request.json['tokenProgressInfo']
        profile_id = request.json['profileId']
        response = DatasourceService(token_process_info).get_dimensions(profile_id)
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


@_service.route('/saas/getData', methods=["POST"])
def fetch():
    try:
        data_request_param = request.json
        token_process_info = data_request_param['tokenProgressInfo']
        response = DatasourceService(token_process_info).get_data(data_request_param)
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code

@_service.route('/saas/baidu/plan', methods=["POST"])
def get_plan_data():
    try:
        data = str(request.data, encoding='utf-8')
        data_request_param = json.loads(data)
        response = DatasourceService(token_process_info=None).get_plan_data(data_request_param)
        status_code = HttpStatusCode.HTTP_200_OK \
                if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


