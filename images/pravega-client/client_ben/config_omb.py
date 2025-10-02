import os
import sys
import yaml

if len(sys.argv) != 5:
    print('Missing arguments')
    exit(1)

with open('omb/dell/myworkload.yaml', 'r') as file:
    config = yaml.safe_load(file)

config['name']         = sys.argv[1]
config['payloadFile']  = str(sys.argv[3])
config['messageSize']  = int(sys.argv[4])
config['producerRate'] = int(sys.argv[2])
print( yaml.dump(config) )
