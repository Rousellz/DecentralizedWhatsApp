from python:3.11-alpine

run apk add iptables && echo "net.ipv4.ip_forward=1" | tee -a /etc/sysctl.conf

# run apk add procps iptables iproute2

cmd /bin/shw