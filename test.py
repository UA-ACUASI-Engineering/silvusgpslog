import subprocess

PORT = ':2947'


def singGPSListen(ip):
    
    while True:
        process = gpspipe(ip+PORT)

        while True:

            gpslog(process)

            status = ping(ip)
            if not status:
                break


def gpsListen(silvus_ip1, silvus_ip2, silvus_ip3):

    ipList = [silvus_ip1, silvus_ip2, silvus_ip3]
    
    while True:
        process = gpspipe(ipList)

        while True:
            for ip in ipList:

                status = ping(ip)
            
                if not status:
                   break
            
            for processNo in process:
                gpslog(processNo)

def ping(host):
    """
    Returns True if the specified host is reachable, False otherwise.
    """

    result = subprocess.run(['fping', '-Q', '100000', '-c1', '-t500', host], stdout = subprocess.DEVNULL)

    if result.returncode:
        print(f"{host} is not connected")

    return result.returncode == 0

def gpspipe(ip):
    process = subprocess.Popen(['gpspipe', '-r', ip], stdout = subprocess.PIPE)

    return process

def gpslog(process):
    output = process.stdout.readline().decode()
    if '$GPGGA' in output:
        print(output)







if __name__ == "__main__":
    silvus_ip1 = '172.20.81.233'
    silvus_ip2 = '172.20.125.84'
    silvus_ip3 = '172.20.153.102'

    # multGPSListen(silvus_ip1, silvus_ip2, silvus_ip3)

    singGPSListen(silvus_ip1)

    #gpsListen(silvus_ip1, silvus_ip2, silvus_ip3)

    # wireshark
    # switch to UDP instead of TCP
    # broadcast?
    # nmap
