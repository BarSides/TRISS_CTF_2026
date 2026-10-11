FROM python:3.12-alpine
RUN adduser -D plc
WORKDIR /app
COPY plc.py ./
USER plc
ENV PORT=5021
EXPOSE 5021
CMD ["python3", "plc.py"]
