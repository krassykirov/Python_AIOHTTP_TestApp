FROM library/python:3.8-slim-buster

COPY requirements.txt /app/
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD [ "python", "main.py" ]
