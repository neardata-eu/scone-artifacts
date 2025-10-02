import os
import sys
import yaml

if len(sys.argv) != 5:
    print('Missing arguments')
    exit(1)

with open('prb/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

config['name']          = sys.argv[1]
config['payload_file']  = str(sys.argv[3])
config['message_num']   = int(sys.argv[4])
config['producer_rate'] = int(sys.argv[2])
print( yaml.dump(config) )
