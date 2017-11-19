import sys
import json

userinput = open(sys.argv[1],'r').read()
inputlist = userinput.split()

recipientName = inputlist[3]

print('hello,' , recipientName)
# print(json.dumps({'recipient_Name': recipientName}))