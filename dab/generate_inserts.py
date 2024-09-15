# Generates SQL insert statements in order to populate a database with test data

import csv
import os
import sys
import sqlalchemy as sa


def mssql_engine(user=os.getenv('SA_USERNAME'), password=os.getenv('SA_PASSWORD'), host=os.getenv('SERVER_ADDRESS'), db=os.getenv('DB_NAME'), driver=os.getenv('DB_DRIVER')):
    engine = sa.create_engine(
        f'mssql+pyodbc://{user}:{password}@{host}/{db}?driver={driver}&Trusted_Connection=no&Encrypt=no')
    return engine


def get_table_structure(table_name: str):

    SQL_STATEMENT = """
    SELECT
        c.name,
        t.Name 'data_type',
        c.max_length,
        c.precision ,
        c.scale ,
        c.is_nullable,
        ISNULL(i.is_primary_key, 0) 'is_primary_key'
    FROM
        sys.columns c
    INNER JOIN
        sys.types t ON c.user_type_id = t.user_type_id
    LEFT OUTER JOIN
        sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id
    LEFT OUTER JOIN
        sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
    WHERE
        c.object_id = OBJECT_ID(:table_name)
    """

    engine = mssql_engine()
    with engine.connect() as conn:
        result = conn.execute(sa.text(SQL_STATEMENT), {
                              "table_name": table_name})
        column_list = result.mappings().all()

    return column_list


def create_insert_statement(table_name: str, column_list: str, column_values):
    table = get_table_structure(table_name)
    columns = (column_list.split(','))
    statement = 'insert into ' + table_name + ' (' + column_list + ') values ('
    for index, item in enumerate(columns):
        column_value = column_values[index]
        column_data = [d for d in table if d['name'] == item]
        if len(column_data) > 0:
            data_type = column_data[0]['data_type']
            if column_value == '':
                data_type = 'null'
            match data_type:
                case 'null':
                    statement = statement + 'null'
                case 'date':
                    statement = statement + (f"'{column_value}'")
                case 'datetime2':
                    statement = statement + (f"'{column_value}'")
                case 'varchar':
                    statement = statement + (f"'{column_value}'")
                case _:  # we can leave decimals as is
                    statement = statement + column_value
            statement = statement + ','
        else:
            print('Value for ' + item + ' not found!')
    statement = statement[:-1]
    statement = statement + ');'
    return statement


def process_csv_file(source_file_name: str, target_file_name: str, table_name: str):

    # Open file
    with open(source_file_name) as file_obj:
        # Create reader object by passing the file object to reader method
        column_list = next(file_obj).replace('\n', '').replace('\r', '')

        reader_obj = csv.reader(file_obj)

        f = open(target_file_name, 'w')
        # Iterate over each row in the csv file using reader object
        for row in reader_obj:
            statement = create_insert_statement(table_name, column_list, row)
            f.write(statement + "\n")
            # for i in range(len(row)):
            #     print(row[i])
        f.write("GO\n")
        f.close


# Parse command line parameters
source_file = sys.argv[1]
target_file = sys.argv[2]
table_name = sys.argv[3]

# Start processing
process_csv_file(source_file, target_file, table_name)
