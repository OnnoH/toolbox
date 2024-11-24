CREATE TABLE [sales].[CUSTOMER] (
      ID INT IDENTITY(1,1) NOT NULL
    , NAME VARCHAR(200)
    , ADDRESS VARCHAR(200)
    , PHONE VARCHAR(200)
    , ACTIVE VARCHAR(1)
    , CONSTRAINT PK_ID PRIMARY KEY CLUSTERED ("ID")
);