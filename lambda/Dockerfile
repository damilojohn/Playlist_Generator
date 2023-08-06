FROM public.ecr.aws/lambda/python:3.10

COPY ../requirements.txt requirements.txt 

#install dependencies in requirements.txt 
RUN pip install -r requirements.txt 

#copy useful files and directories for our build 
COPY lambda/lambda_handler.py api.py 

CMD ["lambda.lambda_handler"]

