FROM python:3
WORKDIR /usr/src/FinApp
ADD FinAppMain.py /usr/src/FinApp/
ADD config.py /usr/src/FinApp/
ADD DBHelper.py /usr/src/FinApp/
RUN pip install python-telegram-bot
RUN pip install psycopg2
CMD [ "python", "FinAppMain.py" ]
