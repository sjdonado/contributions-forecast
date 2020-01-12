FROM nvidia/cuda:10.0-devel as builder

RUN apt-get update \
  && apt-get install -y apt-utils \
  && apt-get install -y git locales

RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN link /usr/bin/python3.6 /usr/local/bin/python

RUN pip3 install --upgrade pip

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN pip3 install --upgrade --no-cache \
  'setuptools==41.0.1' \
  'click==7.0' \
  'numpy==1.16.3' \
  'pandas==0.24.2' \
  'pathlib==1.0.1' \
  'tensorflow-gpu==2.0.0'

RUN pip3 install --upgrade --no-cache seaborn sklearn


FROM builder

WORKDIR /usr/src

RUN pip3 install wheel
RUN pip3 install gunicorn

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "wsgi:app"]