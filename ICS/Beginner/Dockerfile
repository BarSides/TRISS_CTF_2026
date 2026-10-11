FROM python:3.12-alpine
RUN adduser -D plc
WORKDIR /app
COPY plc.py ./
USER plc
ENV PORT=5020
EXPOSE 5020
CMD ["python3", "plc.py"]
