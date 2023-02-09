import subprocess
import time
import select

PORT = ':2947'

def gpsListen(silvus_ip):
    timeout = 0.5

    silvus_ip = silvus_ip + PORT

    while True:
        process = subprocess.Popen(
            ['gpspipe', '-r', silvus_ip], stdout=subprocess.PIPE)
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

    gpsListen(silvus_ip1)
    gpsListen(silvus_ip2)