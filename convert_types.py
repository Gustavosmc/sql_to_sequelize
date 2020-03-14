MYSQL_SEQUELIZE_MAP = {
    'int': 'integer',
    'integer': 'integer',
    'double': 'double',
    'tinyint': 'tinyint',
    'tinyint': 'boolean',
    'smallint': 'smallint',
    'bigint': "bigint",
    'datetime': 'date',
    'date': 'dateonly',
    'float': 'float',
    'varchar': 'string',
    'blob': 'blob',
    'char': 'string',
    'text': 'text',
    'polygon': 'polygon',
    'point': 'point'
}


def get_type(key):
    ret = ''
    try:
        ret = MYSQL_SEQUELIZE_MAP[key]
    except Exception as ex:
        ret = ""
    return ret