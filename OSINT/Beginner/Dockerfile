FROM python:3.12-alpine
RUN adduser -D yinzr
WORKDIR /app
COPY app.py ./
COPY static ./static
USER yinzr
EXPOSE 8000
CMD ["python3", "app.py"]
