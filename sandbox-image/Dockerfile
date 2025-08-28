FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium-browser \
    xvfb \
    x11vnc \
    websockify \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set up a startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports
EXPOSE 5900
EXPOSE 9222

CMD ["/start.sh"]
