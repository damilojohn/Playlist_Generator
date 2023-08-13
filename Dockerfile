FROM public.ecr.aws/lambda/python:3.10
RUN mkdir -p /opt/playlist_gen
WORKDIR /opt/playlist_gen
COPY requirements.txt ./lambda
COPY /sentence_transformer/. ./sentence_transformer 
COPY /lambda/. ./lambda
WORKDIR /opt/playlist_gen/lambda
RUN pwd
RUN ls
#install dependencies in requirements.txt 
RUN pip install -r requirements.txt 
EXPOSE 5000
CMD ["lambda_handler.handler"]

