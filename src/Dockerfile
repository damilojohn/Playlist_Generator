FROM python:3.10-bookworm
RUN  apt-get update
RUN cd src
WORKDIR /opt/playlist_gen
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python3", "app.py" ]
