from posixpath import split
import telnetlib
import ipaddress
import concurrent.futures
from datetime import date

# If finds login prompt, return address
def telnet_test(network):
    output = []
    for ip in network:
        try:
            tn = telnetlib.Telnet(str(ip))
            tn_read = tn.read_until(b": ", timeout=4)
            if tn_read != "":
                    output.append(str(ip))
                    print(f"{ip} Telnet Accepted")
        except:
            print(f"{ip} Telnet Refused or Host Not Available")
    return(output)

# Gets network, for readability 
def get_network(network, cidr):
    return (ipaddress.IPv4Network(f"{network}/{cidr}"))


# Test User input, create multi processes, then find addresses
if __name__ == "__main__":
    telnetHosts = []
    addressSplit = []
    networkSplit = []
    try:
    # User Input
        address, cidr = input("Network Addr: "), int(input("Netmask (CIDR): "))

        # Split Subnets for Multi Processing
        speed = min(max(int(input("Speed (1-4): ")), 1), 4)        
        cidrSplit = min(max(speed+cidr, 0), 32)

        networkSplit.append(get_network(address, cidrSplit))
        for i in range(1, (speed*speed)):
            temp = list(ipaddress.IPv4Network(f"{networkSplit[i-1]}").hosts())[-1] + 2
            networkSplit.append(get_network(temp, cidrSplit))
        
       # Mutli Process Creation
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(telnet_test, networkSplit[i]) for i in range(len(networkSplit))]
            for f in concurrent.futures.as_completed(results):
                telnetHosts.append(f.result())
        
        # Flatten lists, print sorted addresses
        telnetFlatten = sorted([item for sublist in telnetHosts for item in sublist])
        print(f"Hosts with Telnet\n{telnetFlatten}")

        # Save results
        if input("Save results? Y/N: ").upper == 'Y':
            with open(f"telnetfinder-{date.today()}.txt", "w") as output:
                output.write(str(telnetFlatten))

    except ValueError:
        print('address/netmask is invalid for IPv4:', address, cidr)
   
    
