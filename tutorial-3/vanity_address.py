import sys
sys.path.append('../libraries')
import address

if (len(sys.argv) != 2):
    print("usage: python vanity_address.py [desired_prefix]")
    exit()

if (sys.argv[1][0] != "4"):
    print "Monero addresses must start with the character 4"
    exit()

## create random addresses until one of them matches the desired prefix
## bruteforcing takes a while
while(1):
    rand_address = address.generate_random_address()
    if (rand_address[0:len(sys.argv[1])] == sys.argv[1]):
        print(rand_address)
        exit()
    else:
        print("searching")
