# Microsoft SQL Server on Docker

A containerised database can be a convenient way to test your [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) applications. There are a lot of database flavours out there, but this how-to is about the [SQL Server](https://www.microsoft.com/en-gb/sql-server/sql-server-downloads) from Microsoft.

## Versions

There are a number of versions (see [comparison](https://expressdb.io/sql-server-express-feature-comparison.html)), the latest being (at time of writing) 2022. Note that 2017 and 2019 are also available on Linux (and Docker).

```shell
docker pull mcr.microsoft.com/mssql/server:2022-latest
```

## Client Software

Probably too much to list them all here, but for MacOS these are some good choices:

* [Jetbrains DataGrip](https://www.jetbrains.com/datagrip/)
* [DBeaver Community Edition](https://dbeaver.io/)
* [Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio)
* [CLI](https://github.com/microsoft/go-sqlcmd) `brew install sqlcmd`

## Compose

The easiest way of running the container is probably Docker Compose. Store the snippet below in a file called `sqlserver.yaml`.

```yaml
version: "3.2"
services:

  sql-server-db:
    container_name: sql-server-db
    image: mcr.microsoft.com/mssql:2022-latest
    ports:
      - "1433:1433"
    environment:
      ACCEPT_EULA: "Y"
      MSSQL_SA_PASSWORD: "Passw0rd"
      MSSQL_DATA_DIR: /var/opt/mssql/data
      MSSQL_PID: 'Developer' 
      MSSQL_TCP_PORT: 1433
    volumes:
      - ./data:/var/opt/mssql/data
      - ./log:/var/opt/mssql/log
      - ./secrets:/var/opt/mssql/secrets
```

If you want to persist your data, just create the folders under `volumes:`, otherwise just remove this section.

Start the server with `docker compose -f sqlserver.yaml -d up`. Note the warning when you're on an Apple Silicon Mx. Microsoft hasn't build the images for the Aarch64 architecture. Emulation of the x86_64 version works fine however, but the performance may not be ideal.

## Test

Enter the container :
```shell
docker exec -ti sql-server-db bash
```
and browse around or issue the following :

```shell
docker exec sql-server-db /opt/mssql-tools/bin/sqlcmd -U sa -P Passw0rd -Q "SELECT @@version"
```

Or use one of the client software options above (and let it download/install some drivers) and create a connection.

## Customise

It's possible to create your own variant of the image. Here are some [pointers](https://learn.microsoft.com/en-gb/sql/linux/sql-server-linux-docker-container-configure).

An example that will install `sqlpackage` taken from https://github.com/ormico/sqlpackage-docker :

```Dockerfile
FROM mcr.microsoft.com/mssql/server:2022-latest
LABEL maintainer="Zack Moore https://github.com/ormico/"
USER root
VOLUME download
ENV ACCEPT_EULA=Y
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        unzip \
        msodbcsql18 \
        mssql-tools
RUN wget -O sqlpackage.zip https://aka.ms/sqlpackage-linux \
    && unzip sqlpackage.zip -d /opt/sqlpackage \
    && chmod +x /opt/sqlpackage/sqlpackage \
    && rm /sqlpackage.zip
RUN wget "http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl3_3.1.5-1_amd64.deb" \
    && dpkg -i libssl3_3.1.5-1_amd64.deb \
    && rm libssl3_3.1.5-1_amd64.deb
USER mssql
ENV PATH=$PATH:/opt/mssql-tools/bin:/opt/sqlpackage
```

and build it via `docker build -t my-mssql .`.

If you're on a Silicon Mac the use of `sqlpackage` inside a container will probably end with a `Segmentation fault` which is not good.

## Export & Import

To get developers up and running quickly, Microsoft created a so-called *Data-tier application* a.k.a. DACPAC / BACPAC. There's some information about this [here](https://learn.microsoft.com/en-gb/sql/relational-databases/data-tier-applications/data-tier-applications?view=sql-server-ver16).

There are several ways to create those `.dacpac` and `.bacpac` files. One of them is using the `sqlpackage` mentioned above.

Instead of using the utility from the container you can also install it locally on your [Mac](https://learn.microsoft.com/en-gb/sql/tools/sqlpackage/sqlpackage-download?view=sql-server-ver16#macos).

Note the `sudo spctl --master-disable` and  command. The package contains a lot of unsigned `.dll` files. You can of course authorise them one by one via *System Settings* but that's not recommended ;-)

Be sure to run a couple of `sqlpackage` commands before turning the security back on with `sudo spctl --master-enable`.

### Testdata

```sql
create database my_database;
GO
use my_database;
GO
create schema my_schema;
GO
create table my_schema.my_table (name nvarchar(255));
GO
insert into my_schema.my_table (name) values ('Bob');
insert into my_schema.my_table (name) values ('Alice');
insert into my_schema.my_table (name) values ('John');
insert into my_schema.my_table (name) values ('Jane');
insert into my_schema.my_table (name) values ('Scott');
insert into my_schema.my_table (name) values ('Tiger');
GO
select name from my_schema.my_table;
GO
```

Paste the code above in a script window of your favourite client or save it in a file called `create-testdata.sql` and load it using the CLI.

```shell
cat create-testdata.sql | sqlcmd -S localhost -U sa -P Passw0rd -i /dev/stdin
```

### Export

To create a `.bacpac` from the created `my_database`:

```shell
sqlpackage /Action:Export /SourceServerName:"localhost" /SourceDatabaseName:"my_database" /SourceUser:"SA" /SourcePassword:"Passw0rd" /SourceEncryptConnection:False /SourceTrustServerCertificate:True /TargetFile:"my_database.bacpac"
```

### Import

Stop the container with `docker compose -f sqlserver.yaml down --volumes` and start it again `docker compose -f sqlserver.yaml up -d`. Verify that `my_database` is gone and then import the created `.bacpac`.

```shell
sqlpackage /Action:Import /TargetServerName:"localhost" /TargetDatabaseName:"my_database" /TargetUser:"SA" /TargetPassword:"Passw0rd" /TargetTrustServerCertificate:True /SourceFile:"my_database.bacpac"
```

### Create new image

To use a prepared container with testdata for your project, there's no need to execute all the commands. Instead, make an image of a running container :

```shell
docker commit sql-server-db my-mssql
```

This way there's no need for persisting data and you start fresh whenever you start a container of the `my-mssql` image.