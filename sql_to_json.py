from dataclasses import dataclass, field
from convert_types import get_type
import re

FLAG_TABLE_NAME   = 100
FLAG_ATTRIBUTES   = 101
FLAG_PRIMARY_KEYS = 102
FLAG_RELATIONS    = 103


@dataclass
class Table:
    name: str = ''
    attributes: list = field(default_factory=list)
    relations: list = field(default_factory=list)


@dataclass
class Attribute:
    name: str = ''
    type: str = ''
    default: object = None
    nullable: bool = False
    primaryKey: bool = False
    unique: bool = False
    autoincrement: bool = False


@dataclass
class Relation:
    table: str
    fk: str
    references: str


def get_tables(file='files/sql.sql'):
    flag = FLAG_TABLE_NAME
    tables = []
    with open(file, 'r') as reader:
        lines = reader.readlines()
        table = Table()
        for line in lines:
            line = line.lower()

            if line.find('primary key') > -1 and flag == FLAG_ATTRIBUTES:
                for attr in table.attributes:
                    if line.find('`' + attr.name + '`') > -1:
                        attr.primaryKey = True
                flag = FLAG_PRIMARY_KEYS

            # SET ATTRIBUTES FOR TABLE
            if flag == FLAG_ATTRIBUTES:
                splited_line = line.split(' ')
                attr = Attribute()
                attr.name = line.split("`")[1].strip()
                attr.type = re.sub(r'\([0-9]+\)', '', line.split()[1])
                attr.type = get_type(attr.type)
                attr.nullable = line.find('not null') == -1
                attr.autoincrement = line.find('auto_increment') > -1
                if line.find('default') > -1:
                    attr.default = splited_line[splited_line.index('default') + 1].strip().rstrip(',')
                table.attributes.append(attr)

            # SET UNIQUE FIELDS
            if line.find('unique index') > -1:
                for attr in table.attributes:
                    if line.find('`'+attr.name+'`') > -1:
                        attr.unique = True

            # SET TABLE NAME
            if line.find('create table') > -1 and flag == FLAG_TABLE_NAME:
                table = Table()
                table.name = line.split("`")[3].strip()
                flag = FLAG_ATTRIBUTES

            # CLOSE TABLE
            if line.find('engine') > -1 < line.find(';'):
                tables.append(table)
                table = Table()
                flag = FLAG_TABLE_NAME

    return tables


def command_generate(tables=[]):
    # sequelize model:create --name User --attributes "username:[type:string,unique:true]"
    command = ""
    extCont = 0
    for table in tables:
        extCont += 1
        cmdLine = 'npx sequelize model:create --name {} --attributes '.format(
            "".join([(v.capitalize()) for v in table.name.split('_')]))
        cont = 0
        for attr in table.attributes:
            cont += 1
            if not attr.name == 'id':
                comma = "," if cont < len(table.attributes) else ""
                cmdLine = cmdLine + '{}:{}{}'.format(attr.name, attr.type, comma)
        breakLine = "" if extCont == len(tables) else " && \n "
        command += cmdLine +  breakLine
    return command


#print(command_generate(get_tables()))