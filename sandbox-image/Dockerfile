FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    chromium-browser \
    xvfb \
    x11vnc \
    websockify \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy tool-api
COPY ./tool-api /app/tool-api
RUN pip3 install -r /app/tool-api/requirements.txt

# Set up a startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports
EXPOSE 5900
EXPOSE 9222
EXPOSE 8081

CMD ["/start.sh"]
