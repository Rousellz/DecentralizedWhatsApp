FROM python:3-alpine

RUN apk update && apk add --no-cache iptables && echo "net.ipv4.ip_forward=1" | tee -a /etc/sysctl.conf && sysctl -p
RUN apk add procps iptables iproute2

CMD /bin/sh