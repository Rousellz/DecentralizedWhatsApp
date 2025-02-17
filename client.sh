#!/bin/sh
echo "Rutas antes de cambiar:"
ip route

ip route del default
ip route add default via 10.0.10.254

echo "Rutas después de cambiar:"
ip route


python /home/app/client_app.py