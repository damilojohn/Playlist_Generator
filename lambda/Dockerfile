FROM public.ecr.aws/lambda/python:3.10

COPY src/requirements.txt requirements.txt 

#install dependencies in requirements.txt 
RUN pip install -r requirements.txt 

#copy useful files and directories for our build 
COPY src/app.py app.py 
COPY serverless/api.py api.py 

CMD ["api.handler"]

