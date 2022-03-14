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


# Test User input, create multi processes, then find addresses
if __name__ == "__main__":
    telnetHosts = []
    splitAddress = []
    networkSplit = []
    try:
        # User Input
        address = input("Network Addr: ")
        cidr = int(input("Netmask (CIDR): "))

        # Split Subnets for Multi Processing
        speed = min(max(int(input("Speed (1-4): ")), 1), 4)        
        cidrSplit = min(max(speed+cidr, 0), 32)
        splitAddress.append(ipaddress.IPv4Address(f"{address}"))
        for i in range(1, (speed*speed)):
            splitAddress.append(list(ipaddress.IPv4Network(f"{splitAddress[i-1]}/{cidrSplit}").hosts())[-1] + 2)  
        for i in range(len(splitAddress)):
            networkSplit.append(ipaddress.IPv4Network(f"{splitAddress[i]}/{cidrSplit}"))

       # Mutli Process Creation
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(telnet_test, networkSplit[i]) for i in range(len(networkSplit))]
            for f in concurrent.futures.as_completed(results):
                telnetHosts.append(f.result())
        
        telnetFlatten = [item for sublist in telnetHosts for item in sublist]
        print(f"Hosts with Telnet\n{sorted(telnetFlatten)}")

        
        if input("Save results? Y/N: ").upper == 'Y':
            with open(f"telnetfinder-{date.today()}.txt", "w") as output:
                output.write(str(telnetFlatten))      
     
    except ValueError:
         print('address/netmask is invalid for IPv4:', address, cidr)
 
