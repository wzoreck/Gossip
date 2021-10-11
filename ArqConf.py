#pip install configparser
import configparser
import sys

def Main():

    config = configparser.RawConfigParser()
    config.read(sys.argv[1])

    print(config.get('config', 'ip'))

if __name__ == "__main__":
    Main()