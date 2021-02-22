FROM python:3.8.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver" ]

#CMD [ "gunicorn", "--timeout", "0", "--access-logfile", "-", "--workers", "2", "--threads", "2", "--bind", "0.0.0.0:8080", "blimp.wsgi:application" ]