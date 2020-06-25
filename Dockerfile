FROM python:3
WORKDIR /usr/src/FinApp
ADD test.py /usr/src/FinApp/
ADD /Database /usr/src/FinApp/Database/
ADD /Investment /usr/src/FinApp/Investment/
ADD /Menu /usr/src/FinApp/Menu/
ADD /configs /usr/src/FinApp/configs/
ADD /load /usr/src/FinApp/load/
RUN pip install python-telegram-bot
RUN pip install psycopg2-binary
RUN pip install yfinance
RUN pip install iexfinance
CMD [ "python", "test.py" ]
