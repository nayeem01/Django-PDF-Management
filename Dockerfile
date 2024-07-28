FROM python:3

WORKDIR /app
COPY requirements.txt ./
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

