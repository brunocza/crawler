# FROM umihico/aws-lambda-selenium-python:latest
FROM umihico/aws-lambda-selenium-python:3.9.13-selenium4.4.3

# RUN yum install -y google-chrome-stable
COPY handler.py ./
COPY settings.py ./
COPY concorrencia.csv ./
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "handler.blablacar" ]

