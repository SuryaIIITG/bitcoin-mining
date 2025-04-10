from ctypes import cdll, c_ubyte, c_uint32, POINTER
from codecs import decode
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from pprint import pprint
import sys

user = "djkabutar"
password = "Devang110402"
host = "192.168.29.12"
http_port = "8332"

askrate = 5
flag = 1

from time import ctime, sleep, time
from json import loads, dumps
from serial import Serial
from threading import Thread, Event
from queue import Queue
from base64 import b64encode
from urllib.parse import unquote
import binascii, struct

def stats(count, starttime):
    mhshare = 4294.967296
    s = sum(count)
    tdelta = time() - starttime
    rate = (s * mhshare) / tdelta if tdelta > 0 else 0
    stddev = rate / (s**0.5) if s > 0 else 0
    return "[%i accepted, %i failed, %.2f +/- %.2f Mhash/s]" % (count[0], count[1], rate, stddev)

class GetWork():
    def __init__(self):
        self.rpc_connection = AuthServiceProxy("http://{}:{}@{}:{}".format(user, password, host, http_port))
    
    def getwork(self, *args):
        if not args:
            job = self.rpc_connection.batch_([["getwork"]])
        else:
            job = self.rpc_connection.batch_([["getwork", args, user]])
        return job[0]

class Reader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        ser.read(1000)

    def run(self):
        global flag
        while True:
            nonce = ser.read(4)
            if len(nonce) == 4:
                flag = 0
                submitter = Submitter(writer.block, nonce)
                submitter.start()
                golden.set()

class Writer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.block = "0" * 256
        self.midstate = "0" * 64
        self.daemon = True

    def run(self):
        global flag
        while True:
            work = bitcoin.getwork()
            self.block = work['data']
            self.midstate = work['midstate']
            flag = 1
            rdata2 = decode(self.block[95:63:-1], 'hex')
            rmid = decode(self.midstate[::-1], 'hex')
            payload = rmid + rdata2
            print(binascii.hexlify(payload[::-1]))
            ser.write(payload[::-1])
            result = golden.wait(askrate)
            if result:
                golden.clear()

class Submitter(Thread):
    def __init__(self, block, nonce):
        Thread.__init__(self)
        self.block = block
        self.nonce = nonce

    def run(self):
        print("Block found on " + ctime())
        hrnonce = int(binascii.hexlify(self.nonce), 16)
        print(hex(hrnonce)[2:])
        data = self.block[:152] + hex(hrnonce)[2:] + self.block[160:]
        try:
            result = bitcoin.getwork(data)
            print("Upstream result: " + str(result))
        except Exception as e:
            print("RPC send error:", e)
            result = False
        results_queue.put(result)

class Display_stats(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = [0, 0]
        self.starttime = time()
        self.daemon = True
        print("Miner started on " + ctime())

    def run(self):
        while True:
            result = results_queue.get()
            if result:
                self.count[0] += 1
            else:
                self.count[1] += 1
            print(stats(self.count, self.starttime))
            results_queue.task_done()

golden = Event()
bitcoin = GetWork()
results_queue = Queue()

def print_usage():
    print("Usage: ./" + str(sys.argv[0]) + " <PORT>")

if len(sys.argv) != 2:
    print_usage()
    exit()

serial_port = sys.argv[1]
ser = Serial(serial_port, 2000000, timeout=askrate)
reader = Reader()
writer = Writer()
disp = Display_stats()
reader.start()
writer.start()
disp.start()

try:
    while True:
        sleep(10000)
except KeyboardInterrupt:
    print("Terminated")
