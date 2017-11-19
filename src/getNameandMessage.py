import sys
import json

userinput = open(sys.argv[1],'r').read()
inputlist = userinput.split()

recipientName = inputlist[1]
message = ' '.join(inputlist[2:])

# print('recipientName:', recipientName)
# print('message:', message)

print(json.dumps({'recipient_Name': recipientName, 'message': message}))
