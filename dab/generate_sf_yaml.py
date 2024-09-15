# Generates YAML file for Snowfakery for the given table.

import os
import sys
import sqlalchemy as sa
import ruamel.yaml


class NonAliasingRTRepresenter(ruamel.yaml.representer.RoundTripRepresenter):
    # Prevent the creation of aliases in the YAML
    def ignore_aliases(self, data):
        return True


# Leave null values empty
def none_representer(self, data):
    return self.represent_scalar(u'tag:yaml.org,2002:null', u'')


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


def get_comment(column):
    comment = '#'
    comment += ' type=' + column['data_type']
    comment += ' max_length=' + column['max_length']
    comment += ' precision=' + column['precision']
    comment += ' scale=' + column['scale']
    comment += ' is_nullable=' + column['is_nullable']
    comment += ' is_primary_key=' + column['is_primary_key']


def get_faker(column):
    column_name = column['name']
    data_type = column['data_type']
    max_length = column['max_length']

    faker = ''

    if column_name.find('_ind') != -1:
        data_type = 'yes_no'
    if column_name.find('_bdrg') != -1:
        data_type = 'amount'
    if column_name.find('_perc') != -1:
        data_type = 'percentage'

    match data_type:
        case 'null':
            pass
        case 'yes_no':
            faker = {'fake': 'yes_no'}
        case 'amount':
            faker = {'fake': 'amount'}
        case 'percentage':
            faker = {'fake': 'percentage'}
        case 'date':
            faker = {'fake': 'Date'}
        case 'datetime2':
            faker = {'fake': 'Date'}
        case 'varchar':
            faker = {'RandomString.random_string': {
                'length': max_length, 'fixed': False, 'case': 'CAPITALISE'}}
        case 'decimal':
            faker = {'fake': 'pydecimal'}
        case 'integer':
            faker = {'fake': 'randomint'}
        case _:
            pass

    return faker


def create_snowfakery_yaml(table_name: str, no_rows: int, target_yaml: str):
    table_struct = get_table_structure(table_name)

    if table_name.find('.') == -1:
        table_name_without_schema = table_name
    else:
        table_name_without_schema = table_name[table_name.find('.')+1:]

    # Create YAML object and configure
    yaml_header = """
    - snowfakery_version: 3
    - var: snowfakery_locale
      value: nl_NL
    - plugin: faker_addons.Provider
    - plugin: random_string.RandomString
    """

    yaml_object = ruamel.yaml.YAML()
    yaml_object.Representer = NonAliasingRTRepresenter
    yaml_object.representer.add_representer(type(None), none_representer)
    yaml_object.preserve_quotes = True
    yaml1 = yaml_object.load(yaml_header)

    object = {'object': table_name_without_schema}
    object.update({'count': no_rows})
    object.update({'fields': {}})
    fields = object['fields']

    for column in table_struct:
        faker = get_faker(column)
        field = {column['name']: faker}
        fields.update(field)

    yaml1.append(object)
    with open(target_yaml, 'wb') as stream:
        yaml_object.dump(yaml1, stream)

    stream.close


# Parse command line parameters
table_name = sys.argv[1]
no_rows = sys.argv[2]
target_file = sys.argv[3]

create_snowfakery_yaml(table_name, no_rows, target_file)

