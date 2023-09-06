console.log("Executing pre-request script for " + pm.info.requestName + " in environment " + pm.environment.name)

const grant_type = "client_credentials"
const tenant = "YOUR AZURE ACTIVE DIRECTORY TENANT ID GOES HERE"

function getClientApplicationId(clients) {
    const client = clients.filter(function(element) {
        return element.name === pm.environment.get("client_application_name")
    })
    return (client.length >= 1) ? client[0].applicationId : {}
}

function getRequestConfig(requests) {
    const request = requests.filter(function(element) {
        return element.name === pm.info.requestName
    })
    return (request.length >= 1) ? request[0] : {}
}

function getProvider(providers) {
    const provider = providers.filter(function(element) {
        return element.environment === pm.environment.name
    })
    return (provider.length >= 1) ? provider[0] : {}
}

pm.sendRequest("http://localhost:8000/config.json", (error, response) => {
    if (error) {
        throw new Error("Unable to load Kong configuration.")
    } else {
        try {
            const config = response.json()
            const old_scope = pm.environment.get("scope")
            const request = getRequestConfig(config.requests)
            const provider = getProvider(request.providers)
            const scope = provider.id + "/.default"
            const current_date = Number(Date.now())
            const expiration_date = Number(pm.environment.get("token_expires_on"))

            pm.environment.set("client_application_id", getClientApplicationId(config.clients))
            pm.environment.set("scope", scope)
            pm.environment.set("server", provider.server)

            if (!pm.environment.get("token") ||  expiration_date < current_date || scope != old_scope) {
                pm.sendRequest({
                    url: 'https://login.microsoftonline.com/' + tenant + '/oauth2/v2.0/token',
                    method: 'POST',
                    header: 'Content-Type: application/x-www-form-urlencoded',
                    body: {
                        mode: 'urlencoded',
                        urlencoded: [
                            { key: "client_id", value: pm.environment.get("client_application_id"), disabled: false },
                            { key: "scope", value: pm.environment.get("scope"), disabled: false },          
                            { key: "client_secret", value: pm.environment.get("client_secret"), disabled: false },
                            { key: "grant_type", value: grant_type, disabled: false },
                        ]
                    }
                }, function (err, res) {
                    if (err) {
                        throw new Error("Unable to fetch token.")
                    } else {
                        try {
                            const body = res.json();
                            const expires_on = current_date + (parseInt(body.expires_in) * 1000)
                            pm.environment.set("token_expires_on", expires_on)
                            pm.environment.set("token", body.token_type + " " + body.access_token)
                        } catch(exception) {
                            throw new Error("Unable to parse token.")
                        }
                    }
                })
            }
        } catch(exception) {
            throw new Error("Unable to parse Kong configuration.")
        }
    }
})
