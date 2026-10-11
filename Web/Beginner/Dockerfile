FROM python:3.12-alpine
RUN adduser -D pierogi
WORKDIR /app
COPY app.py ./
COPY static ./static
USER pierogi
EXPOSE 8000
CMD ["python3", "app.py"]
