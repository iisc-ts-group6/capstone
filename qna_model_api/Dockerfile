# pull python base image
FROM python:3.10-slim-buster

# specify working directory
WORKDIR .

# ARG ENV_FILE
# COPY .env /app/.env
# RUN pip install python-dotenv
# RUN python -c "import os; import dotenv; dotenv.load_dotenv('/app/.env')"

# copy application files
ADD . .

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port for application
EXPOSE 8001

# start fastapi application
CMD ["python", "app/main.py"]