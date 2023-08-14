FROM public.ecr.aws/lambda/python:3.10
#install dependencies in requirements.txt 
WORKDIR "${LAMBDA_TASK_ROOT}"
COPY requirements.txt .
COPY /lambda/. .
COPY /sentence_transformer/. .
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt 
RUN mkdir -p playlist_gen_cache/cache
ENV TRANSFORMERS_CACHE=/playlist_gen_cache/cache/
RUN pwd
RUN ls
EXPOSE 5000
CMD ["lambda_handler.handler"]

