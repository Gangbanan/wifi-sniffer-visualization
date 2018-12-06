import sys
import os
import logging
import traceback
import random
import time
import datetime
import multiprocessing
import Queue
import sqlite3
import pcapy
import dpkt
sys.path.append('../')
from setting import PROJECT_DIR
sys.path.append(PROJECT_DIR)

# mac
# interface = 'en0'
# monitor_enable  = 'tcpdump -i en0 -Ic1 -py IEEE802_11'
# monitor_disable = 'tcpdump -i en0 -Ic1'
# change_channel  = 'airport en0 channel {}'

# linux
interface = 'wlp2s0'
monitor_enable  = ''
monitor_disable = ''
change_channel  = 'iw dev wlp2s0 set channel %s'

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] # 2.4GHz only

queue = multiprocessing.Queue()

from backend.db import dbconn
conn = dbconn.getDBConn()

def start():
    logging.basicConfig(filename='wifispy.log', format='%(levelname)s:%(message)s', level=logging.INFO)
    os.system(monitor_enable)
    print("Monitor Mode Open.")
    stop_rotating = rotator(channels, change_channel)
    stop_writing  = writer()
    try: sniff(interface)
    except KeyboardInterrupt: sys.exit()
    finally:
        stop_writing.set()
        stop_rotating.set()
        os.system(monitor_disable)

def rotator(channels, change_channel):
    def rotate(stop):
        while not stop.is_set():
            try:
                channel = str(random.choice(channels))
                logging.info('Changing to channel ' + channel)
                os.system(change_channel % channel)
                time.sleep(1) # seconds
            except KeyboardInterrupt: pass
    stop = multiprocessing.Event()
    multiprocessing.Process(target=rotate, args=[stop]).start()
    print("Rotating")
    return stop

def writer():
    db = sqlite3.connect('wifispy.sqlite3')
    def write(stop):
        while not stop.is_set():
            try:
                logging.info('Writing...')
                for _ in range(0, queue.qsize()):
                    item = queue.get_nowait()
                    INSERT_TEMPLATE = """insert into sniff values('{mac}', {time});"""
                    dbconn.executeSelect(conn, INSERT_TEMPLATE.format(**item))
                time.sleep(1) # seconds
            except Queue.Empty: pass
            except KeyboardInterrupt: pass
    create =  'CREATE TABLE IF NOT EXISTS public.sniff (mac character(17), "time" double precision);'
    dbconn.executeSelect(conn, create)
    stop = multiprocessing.Event()
    multiprocessing.Process(target=write, args=[stop]).start()
    print("DB create successfully.")
    return stop

def to_address(address): # decode a MAC or BSSID address
    return ':'.join('%02x' % ord(b) for b in address)

def sniff(interface):
    max_packet_size = 25500 # bytes
    promiscuous = 1 # boolean masquerading as an int
    timeout = 100 # milliseconds
    packets = pcapy.open_live(interface, max_packet_size, promiscuous, timeout)
    packets.setfilter('') # bpf syntax (empty string = everything)
    (header, data) = packets.next()
    while header:
        timestamp = datetime.datetime.now().isoformat()
        try:
            packet = dpkt.radiotap.Radiotap(data)
            frame = packet.data
            if not hasattr(frame, "type"):
                print("frame has no type")
                (header, data) = packets.next()
                continue
            else:
                print("frame has type")
            # packet_signal = -(256 - packet.ant_sig.db) # dBm
            packet_signal = 0
            if frame.type == dpkt.ieee80211.MGMT_TYPE:
                record = {'mac':to_address(frame.mgmt.src), "time": time.time()}
                queue.put(record)
                record = {'mac':to_address(frame.mgmt.dst), "time": time.time()}
                queue.put(record)
                record = {'mac':to_address(frame.mgmt.bssid), "time": time.time()}
                queue.put(record)

            elif frame.type == dpkt.ieee80211.DATA_TYPE:
                record = {'mac':to_address(frame.data_frame.src), "time": time.time()}
                queue.put(record)
                record = {'mac':to_address(frame.data_frame.dst), "time": time.time()}
                queue.put(record)
                record = {'mac':to_address(frame.data_frame.bssid), "time": time.time()}
                queue.put(record)
        except Exception as e:
            logging.error(traceback.format_exc())
        (header, data) = packets.next()

start()
