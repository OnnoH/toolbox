console.log("Executing Workspace pre-request script for " + pm.info.requestName + " in environment " + pm.environment.name)

if (pm.environment.get("client_application_name") || pm.environment.get("client_secret")) {
    console.log("Credentials set on " + pm.environment.name + ". Carry on.")
} else {
    pm.sendRequest("http://localhost:8000/inputs?client_application_name=x&client_secret=x", (error, response) => {
        if (error) {
            throw new Error("Unable to obtain form data.")
        } else {
            try {
                const form_data = response.json();
                pm.environment.set("client_application_name", form_data.client_application_name)
                pm.environment.set("client_secret", form_data.client_secret)
            }
            catch (exception) {
                throw new Error("Unable to parse parameter form.")
            }
        }
    });
}
