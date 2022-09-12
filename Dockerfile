FROM python:3.9
COPY src /src
COPY utilities /utilities
COPY app.py ./app.py
COPY requirements.txt ./requirements.txt
WORKDIR .
RUN pip install -r requirements.txt
CMD python -m flask run --host=0.0.0.0 --port=7000