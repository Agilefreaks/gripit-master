# gripit-modbus-master

# Install additional packages for raspbian


To install systemd run:

`sudo apt-get install systemd`

Configuring as default
In order to use systemd you should also install systemd-sysv which provides the symlinks links for /sbin/init.

`sudo apt-get install systemd-sysv`

In order to boot your system with the newly installed systemd, simply reboot.

`sudo reboot`

# Install Service


Need to copy gripit.service file to:

`cd /lib/systemd/system`


Edit gripit.service:

You need to set path to your python main script file.

```
[Service]
Type=idle
ExecStart=/usr/bin/python3 {path}
```

Path example:
`/home/pi/Desktop/gripit-modbus-master/gripit/main.py`


To enable service on boot:

`sudo systemctl enable gripit.service`


To see status of service:

`sudo systemctl status gripit.service`


To start/stop/restart service:

`sudo systemctl [start/stop/restart] gripit.service`

# Logs - registers


To see registers:

`cd /usr/local/gripit/logs`