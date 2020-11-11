FROM python:3.7

RUN pip install pipenv
WORKDIR /home/app
COPY . .
WORKDIR /home/app/informer
RUN pipenv install
ENV PYTHONPATH=/home/app
EXPOSE 8000
CMD ["pipenv", "run", "python", "main.py"]
