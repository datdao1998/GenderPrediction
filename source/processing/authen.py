import logging
import yaml

__key_dict__ = [{
    "project": "rd",
    "key": "abc"
}]

from exception.error import ErrorArgsOrHeader, ErrorAuthentication


def get_config():
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config["project"]


def validate_project(headerReq):
    project = headerReq.get("project", "")
    apikey = headerReq.get("apikey", "")

    cfg = get_config()

    if not project or not apikey:
        logging.warning("Header is empty")
        raise ErrorArgsOrHeader("Header is empty")
    else:
        try:
            if project in cfg.keys() and apikey == cfg[project]:
                return True
            else:
                logging.warning("Invalid project or apikey")
                raise ErrorAuthentication("Invalid project or apikey")
        except Exception:
            logging.warning("Invalid project or apikey")
            raise ErrorAuthentication("Invalid project or apikey")


