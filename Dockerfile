FROM python:3.6.1

WORKDIR /a2

ADD . /a2

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","web_app.py"]


