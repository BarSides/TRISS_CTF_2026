FROM python:3.12-alpine
RUN adduser -D bridges
WORKDIR /app
COPY app.py ./
COPY static ./static
USER bridges
EXPOSE 8000
CMD ["python3", "app.py"]
