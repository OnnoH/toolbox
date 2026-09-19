# Run Python script as a service

Start your Python script with a 'portable' shebang (https://realpython.com/python-shebang/)

```shell
#!/usr/bin/env python3
```

and make sure it can be executed

```shell
chmod +x /home/pi/some-service.py
```

Head over to the folder containing service definitions.

```shell
cd /lib/systemd/system/
```

Create a new service definition file using elevated privileges.

```shell
sudo vi some.service
```

Add some content explained here:

- https://wiki.archlinux.org/title/Systemd
- https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files
- https://coreos.com/os/docs/latest/getting-started-with-systemd.html

```
[Unit]
Description=Some Service
After=multi-user.target

[Service]
Type=simple
ExecStart=/home/pi/some-service.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

and change the access to the file

```shell
sudo chmod 644 /lib/systemd/system/some.service
```

Then activate the service.

```shell
sudo systemctl daemon-reload
sudo systemctl enable some.service
sudo systemctl start some.service
```

Check the status with

```shell
sudo systemctl status some.service
```

or watch the logs

```shell
sudo journalctl -f -u some.service
```

and stop it when done

```shell
sudo systemctl stop some.service
```

or remove it all-together

```shell
sudo systemctl stop some.service
sudo systemctl disable some.service
sudo systemctl daemon-reload
sudo rm /usr/lib/systemd/system/some.service
sudo rm /lib/systemd/system/some.service
sudo systemctl reset-failed
```
