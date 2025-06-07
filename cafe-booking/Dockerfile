FROM python:3.12

RUN apt-get update && apt-get install -y

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80

#CMD ["gunicorn", "--bind", "0.0.0.0:80", "cafe_booking.wsgi:application"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "--timeout", "120", "cafe_booking.wsgi:application"]