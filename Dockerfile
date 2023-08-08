FROM public.ecr.aws/lambda/python:3.10

WORKDIR /mnt/c/users/user/Playlist_Generator/
COPY /requirements.txt ./requirements.txt 
COPY /sentence_transformer/ ./sentence_transformer 

#install dependencies in requirements.txt 
RUN pip install -r requirements.txt 

#copy useful files and directories for our build 
COPY lambda_handler.py ./handler.py

EXPOSE 5000

CMD ["lambda_handler.handler"]

