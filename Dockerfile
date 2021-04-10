FROM public.ecr.aws/lambda/python:3.8

RUN pip install tweepy
RUN pip install Pillow -t .

COPY turn.py ./
COPY drawer.py ./
COPY secrets.py ./
COPY app.py ./

CMD ["app.handler"]
