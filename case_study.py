import re

""" 
Provided data.

Larger data with the required features can be tested as well.

"""

data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'



""" My solution """
# Store the data in 2D list, which can be mapped to Pandas Datagram if 
# more complicated data processing is needed
datagram = [row.split(';') for row in data.split("\n")]
datagram.pop()

m = len(datagram)
n = len(datagram[0])

# The following is in case the entries of the talble is too large for
# us to find the index of a feature
FlightCode, AirlineCode, To_From = -1, -1, -1
for i, v in enumerate(datagram[0]):
    if v == "FlightCodes":
        FlightCode = i
    elif v == "Airline Code":
        AirlineCode = i
    elif v == "To_From":
        To_From = i
        

# 1. FlightCode problem
# Assume at least one number presented in the column
for i in range(1, m):
    cur = datagram[i][FlightCode]
    if cur == "":
        continue
    val = int(float(cur))
    for j in range(i, 0, -1):
        datagram[j][FlightCode] = str(val+10*(j-i))
    for j in range(i+1, m):
        datagram[j][FlightCode] = str(val+10*(j-i))
    break

# 2. To_From problem
# Assume every row must have a to_from
# Make To_From two columns at its original column
datagram[0][To_From: To_From + 1] = ["To", "From"]
for i in range(1, m):
    cur = datagram[i][To_From].split('_')
    datagram[i][To_From: To_From + 1] = list(map(str.upper, cur))

# 3. Airline Code problem
# Assume we only need to keep letters and white space
for i in range(1, m):
    datagram[i][AirlineCode] = re.sub(
        "[^A-Z\s]", "", datagram[i][AirlineCode], 0, re.IGNORECASE).strip()

# Helper function to visually view the result
def prettyPrint(dGram):
    """print the datagram in a customized table form"""
    rCount, cCount = len(dGram), len(dGram[0])
    cMaxSizes = [0]*cCount

    for i in range(rCount):
        for j in range(cCount):
            cMaxSizes[j] = max(cMaxSizes[j],len(dGram[i][j]))
    
    print("",end=" | ")
    for j in range(cCount):
        cur = dGram[0][j]
        cur += " "*(cMaxSizes[j]-len(cur))
        print(cur,end=" | ")
    print("\n"+"-"*(sum(cMaxSizes)+cCount*3+2))

    for i in range(1, rCount):
        print("",end=" | ")
        for j in range(cCount):
            cur = dGram[i][j]
            cur += " "*(cMaxSizes[j]-len(cur))
            print(cur,end=" | ")
        print()

prettyPrint(datagram)
