FROM public.ecr.aws/lambda/python:3.10
RUN mkdir -p opt/playlist_gen
WORKDIR /opt/playlist_gen
COPY requirements.txt .
COPY sentence_transformer/. . 
COPY lambda/. .
#install dependencies in requirements.txt 
RUN pip install -r requirements.txt 
EXPOSE 5000
CMD ["lambda_handler.handler"]

