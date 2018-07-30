import uuid
from flask import Blueprint, request, jsonify
from flask import current_app as app
from myapp_sogou.main.datasourceservice import DatasourceAuth
from myapp_sogou.libs.exceptions import BaseError
from myapp_sogou.libs.const import HttpStatusCode, ResponseCode


_auth = Blueprint('auth', __name__)


@_auth.route('/initAuth', methods=["GET"])
def auth():
    try:
        state = uuid.uuid4()
        response = DatasourceAuth(state=state).oauth_init()
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


@_auth.route('/tokenCallback', methods=["GET"])
def oauthcallback():
    try:
        auth_callback_url = app.config['AUTH_CALLBACK_URL']
        state, code, scope = request.args.get('state'), request.args.get('code'), request.args.get('scope')
        authorization_response_url = f'{auth_callback_url}?code={code}&scope={scope}'
        response = DatasourceAuth(state=state).oauth_callback(authorization_response_url)
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code


@_auth.route('/tokenRelease', methods=["GET"])
def release():
    raise NotImplementedError

@_auth.route('/sogou/conn', methods=["GET"])
def conn():
    try:
        state = uuid.uuid4()
        username, password, token = request.args.get('username'), request.args.get('password'), request.args.get('token')
        response = DatasourceAuth(state=state).conn(username, password, token)
        status_code = HttpStatusCode.HTTP_200_OK \
            if response.get('code') in [ResponseCode.ok] else HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        return jsonify(BaseError(msg=str(e)).object_repr), HttpStatusCode.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(response), status_code
