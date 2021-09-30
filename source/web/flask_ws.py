import os
import logging
import traceback
import uuid
import json
from functools import wraps
from flask import Flask, Response, jsonify
from flask_cors import CORS, cross_origin
from waitress import serve
#from prometheus_flask_exporter import PrometheusMetrics
#from common.utils.time import timeit
from .exception import WSException

__all__ = ["FlaskWS"]


class FlaskWS(Flask):
    def __init__(self, import_name, app_name, host="0.0.0.0", port=8500, **kwargs):
        super(FlaskWS, self).__init__(import_name, **kwargs)

        self.app_name = app_name
        self.host = host
        self.port = port

        self.config["JSON_AS_ASCII"] = False
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        self.config["SECRET_KEY"] = app_name + "_" + uuid.uuid4().hex

        self.pmetrics = None

        CORS(self, supports_credentials=True)

    def __repr__(self):
        return "{} flask's service at {}:{}".format(self.app_name, self.host, self.port)

    # def init_prometheus(self, *args, **kwargs):
    #     self.pmetrics = PrometheusMetrics(self, *args, **kwargs)
    #     self.pmetrics.info("app_info", "{}'s information".format(self.app_name))

    @property
    def healthz(self):
        return jsonify({"code": 200, "message": repr(self)})

    def run(self, wsgi=False, **kwargs):
        logging.info("start {}...".format(repr(self)))

        try:
            assert wsgi

            command = "uwsgi --http-socket {host}:{port} --wsgi-file {file} --callable {app}".format(
                host=self.host,
                port=self.port,
                file=kwargs.pop("file"),
                app=kwargs.pop("app"),
            )
            for k in kwargs.pop("args", list()):
                command += " --{key}".format(key=k.replace("_", "-"))
            for k, v in kwargs.items():
                command += " --{key} {value}".format(key=k.replace("_", "-"), value=v)
            command = command.strip()

            logging.info("[wsgi]: {}".format(command))

            os.system(command)

        except:
            serve(self, host=self.host, port=self.port, **kwargs)
