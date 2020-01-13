FROM tensorflow/tensorflow:2.1.0-gpu-py3 as builder

RUN pip3  install --user --upgrade --no-cache \
  setuptools click numpy pandas pathlib seaborn sklearn

FROM builder

WORKDIR /usr/src

RUN pip3 install wheel
RUN pip3 install gunicorn

COPY ./requirements.txt .
RUN pip3 install  --user  -r requirements.txt

COPY . .

CMD ["gunicorn", "wsgi:app", "--preload"]