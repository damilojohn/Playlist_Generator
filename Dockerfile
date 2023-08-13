FROM public.ecr.aws/lambda/python:3.10
#install dependencies in requirements.txt 
WORKDIR "${LAMBDA_TASK_ROOT}"
RUN pip install -r requirements.txt .
COPY /lambda/. .
RUN pwd
RUN ls
EXPOSE 5000
CMD ["lambda_handler.handler"]

