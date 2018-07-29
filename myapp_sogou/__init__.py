import os
import traceback
from flask import Flask
from eureka.client import EurekaClient, EurekaRegisterError
from myapp_sogou.config.app_config import load_config


def make_app(version):
    app = Flask(__name__)
    config_obj = load_config(version)

    app.config.from_object(config_obj)
    app.secret_key = os.urandom(24)

    register_routes(app)

    if hasattr(config_obj, 'EUREKA') and config_obj.EUREKA:
        register_eureka(config_obj)

    return app


def register_routes(app):
    """Register Blueprint routes."""
    try:
        from myapp_sogou.routes.service import _service
        from myapp_sogou.routes.auth import _auth
    except ImportError:
        raise ImportError()
    app.register_blueprint(_service)
    app.register_blueprint(_auth)


def register_eureka(config_obj):
    try:

        eureka = EurekaClient(
            app_name=config_obj.APP_NAME,
            port=config_obj.PORT,
            ip_addr=config_obj.IP_ADDR,
            eureka_url=config_obj.EUREKA_URL,
            uid=config_obj.IP_ADDR
        )
        ok = eureka.startup()
        assert ok is True, 'Eureka registered failed.'
    except Exception:
        raise EurekaRegisterError(traceback.format_exc())