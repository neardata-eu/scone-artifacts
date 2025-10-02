import os
import sys
import json

if len(sys.argv) != 2:
    print('Missing arguments')
    exit(1)

with open(sys.argv[1], 'r') as file:
    data = json.load(file)

print( data.get('totalMessagesSent') )
