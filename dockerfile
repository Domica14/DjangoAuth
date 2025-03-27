FROM python:3.13

RUN mkdir /AuthService

WORKDIR /AuthService

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /AuthService/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /AuthService/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]