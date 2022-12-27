FROM python:3.9

WORKDIR /usr/src/app

COPY . .
RUN pip install --upgrade pip
RUN pip install -U pip wheel cmake
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
CMD ["bin/sh", "-c", "python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000