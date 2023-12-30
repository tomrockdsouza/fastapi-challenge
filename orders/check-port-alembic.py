import socket
import os
from time import sleep
from subprocess import check_call
import logging

check_call(["pip","freeze"])

def is_port_open(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Set a timeout (in seconds) for the connection attempt
            s.connect((host, port))
        return True
    except (ConnectionRefusedError, TimeoutError):
        return False


if __name__ == '__main__':
    retries = 3
    for i in range(retries):
        host, port = os.environ["POSTGRES_HOST"], int(os.environ["POSTGRES_PORT"])
        if is_port_open(host, port):
            check_call(["alembic", "upgrade", "head"])
            print()
            break
        elif i < (retries - 1):
            logging.info('Database not ready waiting for 10 seconds')
            sleep(10)
        else:
            raise Exception("Alembic could not connect to database")
