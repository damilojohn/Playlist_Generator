FROM public.ecr.aws/lambda/python:3.10
#install dependencies in requirements.txt 
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY /lambda/. "${LAMBDA_TASK_ROOT}"
EXPOSE 5000
CMD ["lambda_handler.handler"]

