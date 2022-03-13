import telnetlib
import ipaddress
from joblib import Parallel, delayed

# If finds login prompt, return address
def telnetTest(network, output):
    for ip in network:
        try:
                tn = telnetlib.Telnet(str(ip))
                tn_read = tn.read_until(b": ",2)
                if tn_read != "":
                    output.append(str(ip))
                print(f"{ip} Telnet Accepted")
        except:
            print(f"{ip} Telnet Refused or Host Not Available")
    return(output)

# Test User input, then find addresses
if __name__ == "__main__":
    telnetHosts = []
    try:
        address = input("Network Addr: ")
        cidr = input("Netmask (CIDR): ")
        network = ipaddress.IPv4Network(f"{address}/{cidr}")
        Parallel(n_jobs=4)(delayed(telnetTest(network, telnetHosts)))
    except ValueError:
        print('address/netmask is invalid for IPv4:', address, cidr)
    


        
