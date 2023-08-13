FROM public.ecr.aws/lambda/python:3.10
#install dependencies in requirements.txt 
WORKDIR "${LAMBDA_TASK_ROOT}"
COPY requirements.txt .
COPY /lambda/. .
COPY /sentence_transformer/. .
RUN pwd
RUN ls
RUN pip install -r requirements.txt 
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
EXPOSE 5000
CMD ["lambda_handler.handler"]

