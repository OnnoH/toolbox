# Port 5000 is in use on MacOS

When you do local (web)development, you might find yourself targeting ports 3000 or 5000 on your localhost.

The latest versions of MacOS claim port 5000 next to port 7000 for AirPlay.

This might cause startup failures for Docker containers for instance:

```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5000 -> 0.0.0.0:0: listen tcp 0.0.0.0:5000: bind: address already in use
```

Changing the port number to 5001 is an option of course, but then you might run into other connectivity issues. If changing the port is not an option, just open the **System Settings** on you Mac, search for `airpl` and select the **AirPlay Receiver** so you can switch it off. (You'll need elevated privileges for that, so keep your password ready.)

![AirPlay Receiver System Settings](images/SystemSettings/AirPlay%20Receiver.png)
