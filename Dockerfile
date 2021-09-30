FROM asc686f61/chatbot_base_ml:v1.32

RUN pip3 install --upgrade pip

RUN pip3 install scikit-learn==0.20.3 pandas

COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt
RUN pip3 install -U git+https://github.com/ASC689561/cow.git@v4.7#egg=cow
ADD ./source /code

WORKDIR /code
ENTRYPOINT python3 app.py
