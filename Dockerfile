FROM python:3.10-alpine
WORKDIR .
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Logrotate
COPY docker/logrotate_app_logs /etc/logrotate.d/log-file
RUN chmod 644 /etc/logrotate.d/log-file

EXPOSE 5000
COPY . .
CMD ["python", "main.py"]