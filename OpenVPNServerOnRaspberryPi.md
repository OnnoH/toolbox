# OpenVPN in a Docker container on a Raspberry Pi

- Install Docker on the Pi
- Clone the [OpenVPN for Docker](https://github.com/kylemanna/docker-openvpn.git) repository
- Enter the `docker-openvpn` folder
- Build the image

```shell
docker build -t your-prefix/open-vpn .
```

Follow the README in the repo or these _slightly modified_ instructions below:

- Initialise the data volume

```shell
export OVPN_DATA="ovpn-data"
export OVPN_IMAGE="your-prefix/open-vpn"
docker volume create --name ${OVPN_DATA}
docker run -v ${OVPN_DATA}:/etc/openvpn --rm ${OVPN_IMAGE} ovpn_genconfig -u udp://your.server.vpn
docker run -v ${OVPN_DATA}:/etc/openvpn --rm -it ${OVPN_IMAGE} ovpn_initpki
# (this can take a while)
```

- Start the server

```shell
docker run -v ${OVPN_DATA}:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN --restart=always ${OVPN_IMAGE}
```

- Generate a client certificate with a passphrase

```shell
docker run -v ${OVPN_DATA}:/etc/openvpn --rm -it ${OVPN_IMAGE} easyrsa build-client-full your-client-name
```

- Retrieve the client configuration with embedded certificates for the use within OpenVPN Connect

```shell
docker run -v ${OVPN_DATA}:/etc/openvpn --rm ${OVPN_IMAGE} ovpn_getclient your-client-name > your-client-name.ovpn
```

- Fetch the `.ovpn` file from your server
- Archive with the passphrase password

```shell
zip -er your-client-name.zip your-client-name.ovpn
```

- Distribute the zip to the 'client' and send the passphrase in a separate channel.
