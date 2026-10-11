FROM python:3.12-alpine
RUN adduser -D -H dispatch
WORKDIR /app
COPY dispatch.py flag.txt ./
RUN chmod 444 dispatch.py flag.txt && chmod 555 /app
USER dispatch
ENV PORT=1337
EXPOSE 1337
CMD ["python3", "dispatch.py"]
