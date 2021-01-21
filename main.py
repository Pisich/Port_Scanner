from colorama import init, Fore
from socket import *
from threading import Thread, Lock
from queue import Queue

init()

N_THREADS=200

q = Queue()
printer = Lock()

def scan_port(port):
  """Used to check if a port in the host is open or not"""
  try:
    s = socket()
    s.connect((host, port))
  except:
    with printer:
      print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
  else:
    with printer:
      print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
  finally:
    s.close()

def scan_thread():
  global q
  while True:
    worker = q.get()
    port_scan(worker)
    q.task_done()

def main(host, ports):
  global q
  for t in range(N_THREADS):
    t = Thread(target=scan_thread, daemon=True)
    t.start()
  for worker in ports:
    q.put(worker)
  q.join()