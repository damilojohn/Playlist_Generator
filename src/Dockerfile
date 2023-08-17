FROM python:3.10

RUN set -ex && mkdir /repo 
WORKDIR /repo 

COPY src/requirements.txt ./requiremtns.txt /repo/

RUN pip install --upgrade pip ==23.1.2 
RUN pip install -r requirements.txt 
ENV PYTHONPATH ".:"

#copy only the needed directories 
COPY src/app.py app.py 
# use docker run -it --rm -p $PORT:11717 to run the web server and listen on host $PORT
ENTRYPOINT ["python3","src/app.py","--port","11717"]

FROM python:3.10-bookworm
RUN  apt-get update
RUN mkdir -p /opt/playlist_gen
WORKDIR /opt/playlist_gen
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python3", "app.py" ]
