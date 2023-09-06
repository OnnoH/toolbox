# Webserver

For security reasons it's not possible for Postman to read content of a filesystem. To circumvent this issue a webserver
can be started and used in a script e.g. to pull in a payload.

## Start Simple

Spinning up a webserver is easy as pie when using Python:

```shell
python3 -m http.server 8000
```

Of course you can change `8000` with any port number that's not in use on your machine.

If you open up a tab in your favourite browser and go to `http://localhost:8000/`, you should see a list of files
that are present in the folder you started the web server from.

## Instruct Postman to fetch a file

To read the contents of a file to be used in a (pre)request script, use the [Postman API](https://www.postman.com/postman/workspace/postman-public-workspace/documentation). E.g.

```javascript
pm.sendRequest("http://localhost:8000/config.json", (error, response) => {
    if (error) {
        throw new Error("Unable to load configuration.")
    } else {
        const config = response.json()
        ...
        doSomethingWithConfig(config)
        ...
    }
});
```

## Getting User Input

Sadly Postman doesn't offer the possibility to show a dialog, that will allow us to input data (e.g. credentials)
and pass it on to the request.

This [popup solution](https://github.com/Tiiberiu/http_popup) is a generic solution to provide this capability. It's modified to accomodate both the dialog and

```shell
python3 webserver.py
```

and call the URL with query parameters (like `.../inputs?client_application_name=x&client_secret=x`) it from a Postman script

```javascript
pm.sendRequest("http://localhost:8000/inputs?client_application_name=x&client_secret=x", (error, response) => {
    if (error) {
        throw new Error("Unable to fetch parameters.")
    } else {
        const params = response.json()
        ...
        pm.environment.set("client_application_name", params.client_application_name)
        pm.environment.set("client_secret", params.client_secret)
        ...
    }
});
```

Note that combining requests requires chaining them.
