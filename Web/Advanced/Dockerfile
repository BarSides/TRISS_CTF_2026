FROM python:3.12-alpine
RUN adduser -D chat
WORKDIR /app
COPY app.py ./
COPY static ./static
USER chat
EXPOSE 8000
CMD ["python3", "app.py"]
