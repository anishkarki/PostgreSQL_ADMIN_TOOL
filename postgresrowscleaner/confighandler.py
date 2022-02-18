from configparser import ConfigParser
import os


def config(filename, section):
    parser = ConfigParser()
    parser.read(filename)
    print(parser.sections())
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename} file.')
    if db:
        return db
    else:
        return None

def config_grabber(filename, section, key):
    try:
        parser = ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            if parser.has_option(section, key):
                return parser.get(section, key)
            else:
                raise Exception(f'Key {key} not found in {section} section in {filename} file.')
        else:
            raise Exception(f'Table: {section} not found in {filename} file.')
    except Exception as e:
        print(e)
        return None

def add_config_tablecondition(filename, section, key, value):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        if parser.has_option(section, key):
            parser.set(section, key, value)
            with open(filename, 'w') as configfile:
                parser.write(configfile)
        else:
            raise Exception(f'Key {key} not found in {section} section in {filename} file.')
    else:
        raise Exception(f'Table: {section} not found in {filename} file.')
