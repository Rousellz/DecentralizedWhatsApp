#!/bin/sh
echo "Rutas antes de cambiar:"
ip route

ip route del default
ip route add default via 10.0.11.254


echo "Rutas después de cambiar:"
ip route

CMD_ARG=${1:-first-server}
echo "Ejecutando: python /home/app/server_app.py $CMD_ARG"
python /home/app/server_app.py $CMD_ARG

# python /home/app/server_app.py first-server