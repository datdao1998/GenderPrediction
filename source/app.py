from flask import request
import cow
from web.flask_ws import FlaskWS

from processing.process import *

app = FlaskWS(__name__, "Gender Prediction", host="0.0.0.0", port=8500)

import logging.config

import yaml
from exception.error import NotFoundData, InvalidNameCharacter, \
    InvalidLanguageCharacter, \
    LanguageValueNotFound, LanguageAndNameNotMatch, NotFoundNameArray, ErrorAuthentication

from processing.authen import validate_project


# {"gender": 0, "accuracy": }
@app.route("/healthz", methods=["GET"])
@cow.auto_try_catch
def healthz():
    return "Welcome to Gender Micro Service"


@app.route("/prediction", methods=["GET"])
@cow.auto_try_catch
def predict_gender_by_name():
    if not validate_project(request.headers):
        raise ErrorAuthentication("Invalid project or apikey")

    name = request.args.get('name')
    language = request.args.get('language').lower()
    # logger.info("Language = " + language)

    if (name is None or name == '') or (language is None or language == ''):
        raise NotFoundData("Language or Name are None")

    if not check_valid(name):
        raise InvalidNameCharacter("Name must start with character and contain alphabet and space")

    if not check_valid(language):
        raise InvalidLanguageCharacter("Language must start with character and contain alphabet and space")

    if not check_value(language):
        raise LanguageValueNotFound("Language must be en(US_UK) or vi(Vietnamese)")

    if not check_language_match_name(language, name):
        raise LanguageAndNameNotMatch("Name must in chosen language")

    # name, language: f"Handle request with: \n\tLanguage: {language} \tName:{name}"
    # logger.info(f"Handle request with: \n\tLanguage: {language} \tName:{name}")

    headers = ["gender", "acc"]

    if language == 'vi':
        gender, prob = predict_name_vietnamese(name)
        return dict(zip(headers, [int(gender), 100 * round(prob, 6)]))

    if language == 'en':
        gender, prob = predict_name_us_uk(name)
        return dict(zip(headers, [int(gender), 100 * round(prob, 6)]))
    # logger.info(f"Language not in Vietnamese or US_UK")
    return None


@app.route("/prediction", methods=["POST"])
@cow.auto_try_catch
def predict_gender_by_list_name():
    if not validate_project(request.headers):
        raise ErrorAuthentication("Invalid project or apikey")

    language = request.json.get('language').lower()
    name = request.json.get('name')

    if not check_valid(language):
        raise InvalidLanguageCharacter("Language must start with character and contain alphabet and space")

    if not check_value(language):
        raise LanguageValueNotFound("Language must be vi(Vietnamese) or en(US or UK)")

    if len(name) == 0:
        raise NotFoundNameArray("List name is empty")

    error = []
    for i, n in enumerate(name):
        if n is None or n == '':
            error.append(i)
            continue
        if not check_valid(n):
            error.append(i)
            continue
        if not check_language_match_name(language, n):
            error.append(i)
            continue

    # logger.info(f"Handle request with: \n\tLanguage: {language} \tName:{name}")
    # for Vietnam name
    if language == 'vi':
        gender, prob = predict_name_vietnamese_list(name)
        headers = ["gender", "acc"]
        ans = list()
        for idx in range(0, len(gender)):
            if idx in error:
                ans.append(dict(zip(headers, [int(0), 0.0])))
                continue
            ans.append(dict(zip(headers, [int(gender[idx]), 100 * round(prob[idx], 6)])))
        # logger.info(f"Response: \n\tGender Suggestion: {ans}")
        return ans

    # for US_UK name
    if language == 'en':
        gender, prob = predict_name_us_uk_list(name)
        headers = ["gender", "acc"]
        ans = list()
        for idx in range(0, len(gender)):
            if idx in error:
                ans.append(dict(zip(headers, [int(0), 0.0])))
                continue
            ans.append(dict(zip(headers, [int(gender[idx]), 100 * round(prob[idx], 6)])))
        # logger.info(f"Response: \n\tGender Suggestion: {ans}")

        return ans
    # logger.info(f"Language not in vn(Vietnamese) or en(US or UK)")
    return None


if __name__ == "__main__":
    app.run()
