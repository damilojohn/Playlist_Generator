FROM python:3.10-bookworm
RUN  apt-get update
RUN pip install -r requirements.txt
WORKDIR /opt/playlist_gen
COPY . .
EXPOSE 8080
CMD [ "python3", "app.py" ]
