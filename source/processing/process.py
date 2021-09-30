import pickle as pkl
import re
from unidecode import unidecode
import logging
import numpy as np
import traceback

vietnamese_data_path = 'data/vietnamese/'
us_uk_data_path = 'data/english/'
vietnamese_model_path = 'model/vietnamese/'
us_uk_model_path = 'model/us_uk/'


def extract_name_vietnamese(res_name):
    if res_name == '':
        return None

    if len(res_name.split(" ")) == 1:
        return res_name, res_name, res_name

    with open(vietnamese_data_path + 'first_name.txt', 'r') as f:
        lines = f.readlines()
    name_patts = []
    for line in lines:
        name_patts.append(line.strip())
    mid = []
    last = ""
    name_extract = res_name.lower().strip()
    name = name_extract
    oke = True
    for ind, t in enumerate(name_extract.split(" ")):
        for l in name_patts:
            if t == l and oke:
                oke = False
                if ind > 0:
                    name = ''
                    for x in range(ind, len(name_extract.split(" "))):
                        name += name_extract.split(" ")[x] + " "
                    for x in range(0, ind):
                        name += name_extract.split(" ")[x] + " "
                name = name.replace(l, "", 1).strip()
                break
    arr_name = name.split(" ")
    for k in range(len(arr_name) - 1, -1, -1):
        if len(arr_name[k]) > 0:
            last = arr_name[k]
            break
    if len(arr_name) > 1:
        mid = arr_name[:-1]
    return name, mid, last


def predict_name_vietnamese(res_name):
    classic_middle_name_male = ['van', 'văn']
    classic_middle_name_female = ['thi', 'thị']
    try:
        name, mid, last = extract_name_vietnamese(res_name)
        if len(mid) > 0:
            if any(mid[0] == m for m in classic_middle_name_male):
                return 1, 1
            if any(mid[0] == f for f in classic_middle_name_female):
                return 0, 1
        mnb, vectorizer = load_model_vietnamese()
        X_test = vectorizer.transform([name])
        return int(mnb.predict(X_test)[0]), np.max(mnb.predict_proba(X_test)[0])
    except Exception:
        logging.error(traceback.format_exc())
        return None


def extract_name_us_uk(res_name):
    res_name = res_name.lower()
    res_name_split = res_name.split(" ")[::-1]
    if len(res_name_split) == 1:
        return res_name
    with open(us_uk_data_path + 'us_uk.txt', 'r') as f:
        lines = f.readlines()
    oke = True
    for split in res_name_split:
        if any(k.replace("\n", "") == split for k in lines):
            res_name = res_name.replace(split, "")
            oke = False
        if not oke:
            break
    return res_name.strip()


def predict_name_us_uk(res_name):
    name = extract_name_us_uk(res_name)
    mnb, vectorizer = load_model_us_uk()
    X_test = vectorizer.transform([name])
    return int(mnb.predict(X_test)[0]), np.max(mnb.predict_proba(X_test)[0])


def predict_name_vietnamese_list(res_name_arr):
    classic_middle_name_male = ['van', 'văn']
    classic_middle_name_female = ['thi', 'thị']
    try:
        name = []
        mid = []
        last = []
        for res_name in res_name_arr:
            if extract_name_vietnamese(res_name) is None:
                name.append("Quoc Dat")
                mid.append("Quoc Dat")
                continue
            name_idx, mid_idx, last_idx = extract_name_vietnamese(res_name)
            name.append(name_idx)
            mid.append(mid_idx)
            last.append(last_idx)
        mnb, vectorizer = load_model_vietnamese()
        X_test = vectorizer.transform(name)
        res = mnb.predict(X_test)
        prob = np.max(mnb.predict_proba(X_test), axis=1)
        for idx, res_cpn in enumerate(res):
            if len(mid[idx]) > 0:
                if any(mid[idx][0] == m for m in classic_middle_name_male):
                    res[idx] = 1
                    prob[idx] = 1
                    continue
                if any(mid[idx][0] == f for f in classic_middle_name_female):
                    res[idx] = 0
                    prob[idx] = 1
                    continue
        return res, prob

    except Exception:
        return None


def predict_name_us_uk_list(res_name_arr):
    logging.info("ARRAY : " + str(len(res_name_arr)))
    try:
        name = []
        for res_name in res_name_arr:
            name_idx = extract_name_us_uk(res_name)
            name.append(name_idx)
        mnb, vectorizer = load_model_us_uk()
        X_test = vectorizer.transform(name)
        return mnb.predict(X_test), np.max(mnb.predict_proba(X_test), axis=1)

    except Exception:
        return None


def load_model_vietnamese():
    mnb = pkl.load(open(vietnamese_model_path + 'model.pkl', 'rb'))
    vectorizer = pkl.load(open(vietnamese_model_path + 'count_vector.pkl', 'rb'))
    return mnb, vectorizer


def load_model_us_uk():
    mnb = pkl.load(open(us_uk_model_path + 'model.pkl', 'rb'))
    vectorizer = pkl.load(open(us_uk_model_path + 'count_vector.pkl', 'rb'))
    return mnb, vectorizer


def check_valid(text):
    invalid = ['!', '@', '#', '$', '%', '^', '&', '*', '/']
    if any(str(text).__contains__(i) for i in invalid):
        return False
    return True


def check_value(text):
    lg = ['en', 'vi']
    if not any(l == text for l in lg):
        return False
    return True


def check_language_match_name(language, name):
    if language == 'en':
        if len(name.split(" ")) > 2 and not str(name).__contains__("-"):
            return False
        if not unidecode(name) == name:
            return False
    return True
