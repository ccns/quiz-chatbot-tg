import configparser

config = configparser.ConfigParser()
config.read('.config')
HOST = config['Bot']['Host']