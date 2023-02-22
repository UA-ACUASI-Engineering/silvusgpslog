import subprocess
import time
import select
import socket

PORT = ':2947'


def multGPSListen(silvus_ip1, silvus_ip2, silvus_ip3):
    silvus_ip1 = silvus_ip1+PORT
    silvus_ip2 = silvus_ip2+PORT
    silvus_ip3 = silvus_ip3+PORT

    timeout = 0.5

    gpspipes = [subprocess.Popen(['gpspipe', '-r', silvus_ip1], stdout=subprocess.PIPE),
                subprocess.Popen(['gpspipe', '-r', silvus_ip2], stdout=subprocess.PIPE),
                subprocess.Popen(['gpspipe', '-r', silvus_ip3], stdout=subprocess.PIPE),]

    while True:

        ready, _, _ = select.select([gpspipe.stdout for gpspipe in gpspipes], [], [], timeout)

        for pipe in ready:
            for gpspipe in gpspipes:
                if pipe == gpspipe.stdout:
                    output = gpspipe.stdout.readline().decode()
                    if '$GPGGA' in output:
                        print(output)


def gpsListen(silvus_ip):
    
    while True:
        process1 = gpspipe(silvus_ip)

        while True:
            gpslog(process1)
            
            status = ping(silvus_ip)
            
            if not status:
                break


def GPSlog():
    IPs = ['172.20.81.233', '172.20.125.84', '172.20.153.102']


    # GPSpipe command to run
    gpspipe_cmd = ['gpspipe', '-r', '172.20.81.233:2947']

    timeout = 1

    # Start gpspipe
    gpspipe_process = subprocess.Popen(gpspipe_cmd, stdout=subprocess.PIPE)

    while True:
        # Check network connectivity
        connected = False
        for ip in IPs:
            try:
                s = socket.create_connection((ip, int(PORT[1:]), timeout))
                process = subprocess.Popen(['gpspipe', '-r', f"{ip}:2947"], stdout=subprocess.PIPE, stdin=s)
                print(f"Connected to {ip}")
                while True:
                    output = process.stdout.readline().decode().strip()
                    if output == '' and process.poll() is not None:
                        break
                    if '$GPGGA' in output:
                        print(f"{ip} GPS data: {output}")
                if process.poll() is not None:
                    print(f"Connection to {ip} lost. Retrying...")
            except:
                pass

        # Restart gpspipe if network connection is reestablished
        if connected and gpspipe_process.poll() is not None:
            gpspipe_process = subprocess.Popen(gpspipe_cmd, stdout=subprocess.PIPE)

        # Stop gpspipe if network connection is lost
        if not connected and gpspipe_process.poll() is None:
            gpspipe_process.kill()

        # Read GPS data from gpspipe
        output = gpspipe_process.stdout.readline().decode()
        if output == '' and gpspipe_process.poll() is not None:
            # If gpspipe has stopped outputting data, it may have crashed, so restart it
            gpspipe_process = subprocess.Popen(gpspipe_cmd, stdout=subprocess.PIPE)
        elif '$GPGGA' in output:
            # Process GPS data here
            print(f"{ip} GPS data: {output}")

        # Sleep for a short period to avoid hogging CPU resources
        time.sleep(0.1)

def ping(host):
    """
    Returns True if the specified host is reachable, False otherwise.
    """

    result = subprocess.run(['fping', '-Q', '100000', '-c1', '-t500', host], stdout = subprocess.DEVNULL)

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

    gpsListen(silvus_ip2)

    # wireshark
    # switch to UDP instead of TCP
    # broadcast?
    # nmap
