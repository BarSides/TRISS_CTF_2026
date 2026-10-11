FROM python:3.12-alpine
RUN adduser -D sieve
WORKDIR /app
COPY app.py filter.py model.json ./
COPY static ./static
USER sieve
EXPOSE 8000
CMD ["python3", "app.py"]
