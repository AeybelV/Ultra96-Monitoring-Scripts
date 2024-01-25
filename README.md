# Ultra96 Daemons

A series of script for resource monitoring on the ultra96 SBC. 

These scripts run as daemons in the background. The service configs are located in `systemd` folder. Copy the contents of the `systemd` folder to /etc/systemd/system. Reload daemons and then start the services.

The stats monitors all publish to MQTT topics. The brokers, ports, and topic can be changed in the daemon configs in `systemd` folder. The broker, port, and topics are passed as parameters to the scripts.
