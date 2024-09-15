# Data API Builder

(building on [MS SQL on MacOs with Docker](./MSSQLOnMacOSDocker.md))

Data API Builder (DAB) is a powerful tool that provides an automatically generated GraphQL and/or REST access to your database. In this recipe we're going to take a look in how to spin up a database server, create a database with schemas and tables, generate and import fake test data, that we then can access via DAB.

## Prerequisites

* Docker - https://www.docker.com/
* Homebrew - https://brew.sh/

Everything below should be run from the [dab](../dab/) folder.

## Environment

Look at the `.env` file and set the variables (especially the password ;-) according to your setup. Make them available for the scripts.

```shell
source .env
```

## MS SQL Server

Getting a server up and running is easy as pie when using Docker.

```shell
# Get the image
docker pull mcr.microsoft.com/mssql/server:2022-latest
# and start a container with it
docker run --name my_dbserver --detach --publish ${SERVER_PORT}:1433 --env "ACCEPT_EULA=Y" --env "MSSQL_SA_PASSWORD=${SA_PASSWORD}" mcr.microsoft.com/mssql/server:2022-latest
```

## Tooling

### Database GUI

There are many applications to choose from. Here are three:
* Azure Data Studio - https://learn.microsoft.com/en-us/azure-data-studio/
* DataGrip - https://www.jetbrains.com/datagrip/
* DBeaver - https://dbeaver.io

### Python
The code is this recipe has been executed using version 3.12 of Python. It will probably work with older and/or newer versions too but ymmv.

```shell
brew install python@3.12

# create a virtual environment and activate it
python3.12 -m venv ./venv 
source ./venv/bin/activate 

# and while you're at it, but probably not necessary:
python3.12 -m pip install --upgrade pip

# and the libraries
pip3.12 install -r requirements.txt
```

### ODBC

What is [ODBC](https://learn.microsoft.com/en-us/sql/odbc/reference/what-is-odbc?view=sql-server-ver15)

For Linux and Mac there's a package available.
```shell
brew install unixodbc
```

Some more references:
* https://dfalbel.github.io/posts/odbc-macos/
* https://www.unixodbc.org/
* https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver16

### MS SQL Tools
Tools to interact with MS SQL Server, sqlcmd being the most prominent. But also the correct ODBC driver is needed.

```shell
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```


## Database

See [create_database.sh](../dab/create_database.sh) and [create_database.sql](../dab/create_database.sql).

In the [tables](../dab/tables/) folder, there are some scripts to create the table structure.

Of course there are plenty of resources on the web that provide examples. E.g.
https://github.com/microsoft/sql-server-samples/tree/master/samples/databases, and of course you may have a use case already.


Adjust these to your liking and execute when ready:

```shell
chmod u+x create_database.sh

./create_database.sh
```

## Generate Test Data
There are a number of tools out there that will generate random data, that you can use when developing and testing your applications.

Some of them are online (probably with a required account registration):

* https://generatedata.com/
* https://www.mockaroo.com/
* https://www.rndgen.com/data-generator

Some of them require a paid license (but offer a trial period):

* https://www.red-gate.com/products/sql-data-generator/

Or in the public domain:

* https://github.com/alan-turing-institute/sqlsynthgen/blob/main/sqlsynthgen/settings.py
* https://github.com/shuttle-hq/synth
* https://faker.readthedocs.io/en/master/
* https://snowfakery.readthedocs.io/en/latest/


### Snowfakery
This generator is tightly coupled to SalesForce and finds its base in Faker, but because of its customisability a good choice for creating testdata. This step is not needed when you used the `requirements.txt` step mentioned above.

```shell
pip3.12 install snowfakery

# or following the official docs:

pip3.12 install pipx
pipx install snowfakery
```

**Customise**

Creating your own custom generators is easy. The plugin mechanism provides two methods, both are used in this recipe.

https://spinningcode.org/2021/05/snowfakery-custom-plugins-part-1/
https://spinningcode.org/2021/06/snowfakery-custom-plugins-part-2/
https://github.com/acrosman/snowfakery_extras/blob/main/Readme.md

The example below show the folder structure and some methods in the __init__.py file.

**Example**

Folder Structure
```
fakeittillyoumakeit
└── plugins
    ├── faker_addons
    │   └── __init__.py
    └── randomString.py
```
(these Python files are in this repository)

As you can see, the first plugin is a collection of Python methods that belong to the class Provider and referred to in the YAML by
```yaml
- plugin: faker_addons.Provider
```
The second one is another implementation.

[**random_string.py**](../dab/plugins/random_string.py)

This one uses the SnowfakeryPlugin and is referred to in the YAML by

```yaml
- plugin: random_string.RandomString
```

Example usage:

```yaml
- object: table
  count: '10'
  fields:
    gibberish:
      RandomString.random_string:
        length: 60
        fixed: false
        case: CAPITALISE
```


[**snowfakery_example.yaml**](../dab/snowfakery/example.yaml)

The YAML will generate data for most of the columns (some nullable columns left intentionally blank), using fake: with both out-of-the-box generators or the custom ones as well as hard-coded values. As you can imagine, this can become a lengthy file because of the number of columns. Creating that by hand might be a cumbersome job. Therefore the following script can scaffold a YAML file for you. It's opinionated of course, but changes to the fake generators are easily made.

See [generate_sf_yaml.py](../dab/generate_sf_yaml.py)

Execute this Python script to generate a Snowfakery YAML for the given table:

```shell
python3.12 generate_sf_yaml.py <schema.table> <number of records to generate> <output file>
```

E.g.

```shell
python3.12 generate_sf_yaml.py sales.customer 100 customer.yaml
```

Then start Snowfakery with that YAML and let it output a CSV.

```shell
snowfakery customer.yaml --output-format=csv

# or use the example from this repository
snowfakery snowfakery/example.yaml --output-format=csv

```

The CSV that's created (in this case : example.csv) with the specified number of lines (in this case : 100) gets an ID column at the end, free of charge and you can't suppress that (yet). Removing it can be done as follows:

```bash
sed -e 's/[^,]*$//' -e 's/.$//' -i '' customer.csv
```

### Import Test Data
Getting that generated data into your database can be done in various ways. A few of them are listed below, but the focus will be on Python using SQL Alchemy.

**PowerShell**

https://www.sqlteam.com/articles/fast-csv-import-in-powershell-to-sql-server

**MS SQL Server BCP**
https://learn.microsoft.com/en-us/sql/relational-databases/import-export/bulk-import-and-export-of-data-sql-server?view=sql-server-ver16

**Jailer**

https://wisser.github.io/Jailer/home.htm

**Python**

The following Python code generates insert into statements for the given table, based on the CSV input.

See [generate_insert.py](../dab/generate_inserts.py).

Call it like this:

```shell
python3.12 generate_inserts.py <input file> <output file> <schema.table_name>
```

E.g.
```shell
python3.12 generate_inserts.py customer.csv customer_data.sql sales.customer

# and execute the generated script with the following command:
sqlcmd -S ${SERVER_ADDRESS} -U ${SA_USERNAME} -P ${SA_PASSWORD} -d ${DB_NAME} -i customer_data.sql -C
```

There you have it! A randomly populated table. Use the 
GUI to check the result ;-)

## Data API Builder

Of course using a GUI to access your databases and data is an option, but not within a services oriented application environment. Then, an API makes more sense. Microsoft has come up with a tool that generates such an API straight of your database with only a configuration file.

https://devblogs.microsoft.com/azure-sql/data-api-builder-ga/
https://learn.microsoft.com/en-gb/azure/data-api-builder/

Although you can use DAB with a variety of database servers, the use of MS SQL Server is assumed here as this is the case for this entire recipe.

Because the heavy lifting is done by the .NET 8 framework, it is of course a prerequisite. Download the SDK here: https://dotnet.microsoft.com/en-us/download

After that, run the installer package and check the availability by running the dotnet command.

Then install the DAB:
```shell
dotnet tool install --global Microsoft.DataApiBuilder
```

Configuration is done via a JSON file and you can create a default one:

```shell
dab init --database-type "mssql" --host-mode "Development" --connection-string "Server=${SERVER_ADDRESS},${SERVER_PORT};User Id=${SA_USERNAME};Database=${DB_NAME};Password=${SA_PASSWORD};TrustServerCertificate=True;Encrypt=True;"

dab add Customer --source "sales.customer" --permissions "anonymous:*"
```

Once this configuration file is in place, execute:

```shell
dab start
```

and open your favourite browser at http://localhost:5000 and check the health.

In order to access the REST API, open http://localhost:5000/api/Customer
or if we want to go GraphQL then Pop the Banana Cake out of the oven http://localhost:5000/graphql/
and paste this query in the request box or create one yourself.

```graphql
query ActiveCustomers {
  customers(filter: { ACTIVE: { eq: "Y" } }) {
    items {
      NAME
    }
  }
}
```

and press play ..eh.. run.

DAB is highly configurable and that requires a recipe in itself. The configuration above only scratches the surface.

## TODO

* Use references to generate related data for the other tables.