FROM python:3.12-alpine
RUN adduser -D inky
WORKDIR /app
COPY app.py ./
COPY static ./static
USER inky
EXPOSE 8000
CMD ["python3", "app.py"]
