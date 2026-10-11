FROM python:3.12-alpine
RUN adduser -D -H scoreboard
WORKDIR /app
COPY scoreboard.py flag.txt ./
RUN chmod 444 scoreboard.py flag.txt && chmod 555 /app
USER scoreboard
ENV PORT=1337
EXPOSE 1337
CMD ["python3", "scoreboard.py"]
