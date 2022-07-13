FROM python:3.10.5

ENV db_host=127.0.0.1
ENV user=root
ENV password=
ENV db_name=chat_db

COPY . /app/server

WORKDIR /app/server

RUN python -m pip install --upgrade pip && pip install wheel

RUN pip3 install -r requirements.txt
EXPOSE 3333

CMD ["python", "app.py"]