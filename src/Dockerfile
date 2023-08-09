FROM python:3.10-bookworm
RUN  apt-get update
WORKDIR /opt/playlist_gen
COPY /src/. .
RUN pip install -r src/requirements.txt
EXPOSE 8080
CMD [ "python3", "app.py" ]
