
FROM alpine

# Enable IP forwarding
RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# Set up the router to keep running
CMD ["sh", "-c", "sysctl -p && while true; do sleep 3600; done"]
