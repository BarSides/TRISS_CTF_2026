# Serves the committed binary over TCP with socat. The download players get is
# the exact same ELF this image runs, so local testing matches the server.
FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /app

COPY files/scoreboard /app/scoreboard
# The real flag lives only on the server. Change it here if needed.
RUN echo 'BarSides{the_jumbotron_reads_your_mind}' > /app/flag.txt \
    && chmod 0555 /app/scoreboard \
    && chmod 0444 /app/flag.txt

USER ctf
EXPOSE 5000

# -T 120 drops idle connections; fork handles one player per connection.
CMD ["socat", "-T", "120", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:/app/scoreboard,chdir=/app,stderr"]
