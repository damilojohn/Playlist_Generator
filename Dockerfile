FROM public.ecr.aws/lambda/python:3.10
#install dependencies in requirements.txt 
WORKDIR "${LAMBDA_TASK_ROOT}"
COPY requirements.txt .
COPY /lambda/. .
RUN pwd
RUN ls
RUN pip install -r requirements.txt 
EXPOSE 5000
CMD ["lambda_handler.handler"]

