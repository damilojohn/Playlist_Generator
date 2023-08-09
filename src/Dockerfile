FROM python:3.10-bookworm
RUN  apt-get update
RUN pwd
RUN pip install -r src/requirements.txt
WORKDIR /opt/playlist_gen
COPY . .
EXPOSE 8080
CMD [ "python3", "app.py" ]
