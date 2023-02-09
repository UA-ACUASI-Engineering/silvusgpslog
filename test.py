import subprocess
import time
import select

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
    timeout = 0.5

    silvus_ip = silvus_ip + PORT

    while True:
        process = subprocess.Popen(['gpspipe', '-r', silvus_ip], stdout=subprocess.PIPE)
        while True:
            ready, _, _ = select.select([process.stdout], [], [], timeout)

            if ready:
                output = process.stdout.readline().decode()
                if output == '' and process.poll() is None:
                    break
                if '$GPGGA' in output:
                    with open('output.txt', 'a') as file:
                        file.write(output)

        if process.poll() is not None:
            process.terminate()
            print("No data received, restarting gpspipe")
        time.sleep(0.1)


if __name__ =="__main__":
    silvus_ip1 = '172.20.81.233'
    silvus_ip2 = '172.20.125.84'
    silvus_ip3 = '172.20.153.102'

    multGPSListen(silvus_ip1, silvus_ip2, silvus_ip3)

    #gpsListen(silvus_ip1)
    #gpsListen(silvus_ip2)