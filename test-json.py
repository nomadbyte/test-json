#!/usr/bin/env python3

import json
import ctypes
import os
import sys


_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if sys.platform in ["linux", "linux2"]:
  _LIB_FILE = "lib/linux/libTestJson.so"
elif sys.platform == "darwin":
  _LIB_FILE = "lib/osx/libTestJson.dylib"
else:
  raise NotImplementedError("Not implemented on '{}' platform".format(sys.platform))



class two_packet_wrappers(ctypes.Structure):
    _fields_ = [
        ('packet1_bytes_num', ctypes.c_ubyte),
        ('packet1_bytes'    , ctypes.c_ubyte * 20),
        ('packet2_bytes_num', ctypes.c_ubyte),
        ('packet2_bytes'    , ctypes.c_ubyte * 20),
    ]

def cp_data_into_c_byte_array(dst, src):
    n = 0
    for c in src:
        dst[n] = ord(c)
        n += 1


def string_into_c_byte_array(str, cba):
    n = 0
    for c in str:
        cba[n] = ord(c)
        n += 1


def hexstr(bytes):
    return " ".join("{:02x}".format(b) for b in bytes)


class TestJson(object):

    def __init__(self):
        self._load_lib()
        self._p1 = None
        self._p2 = None
        self._expect_packet_2 = False;


    @property
    def expect_packet_2(self):
        return self._expect_packet_2


    def _load_lib(self):
        lib_path = os.path.join(_ROOT_DIR, _LIB_FILE)
        self._lib = ctypes.cdll.LoadLibrary(lib_path)
        self._lib.packets2Json.restype  = (ctypes.c_char_p)


    class two_packet_wrappers(ctypes.Structure):
        _fields_ = [
            ('packet1_bytes_num', ctypes.c_ubyte),
            ('packet1_bytes'    , ctypes.c_ubyte * 20),
            ('packet2_bytes_num', ctypes.c_ubyte),
            ('packet2_bytes'    , ctypes.c_ubyte * 20),
        ]


    def get_packets(self, dict):
        packets = []

        if (len(dict) == 0):
            return

        json_str = json.dumps(dict, ensure_ascii=True)

        pw = self.two_packet_wrappers()

        self._lib.json2Packets(json_str.encode('ascii'), ctypes.byref(pw))

        if (pw.packet1_bytes_num > 0):
            p = bytearray(pw.packet1_bytes_num)
            #print("bytes_num:", pw.packet1_bytes_num)
            for i in range(pw.packet1_bytes_num):
               #print("bytes[{}]:".format(i), pw.packet1_bytes[i])
               p[i] = pw.packet1_bytes[i]  ## or & 0xff to convert negative vals
            packets.append(p)

        if (pw.packet2_bytes_num > 0):
            p = bytearray(pw.packet2_bytes_num)
            for i in range(pw.packet2_bytes_num):
               p[i] = pw.packet2_bytes[i] ## or & 0xff to convert negative vals
            packets.append(p)

        return packets


    def get_json0(self, data):
        self._p1 = data
        if not self.expect_packet_2:
            p1 = self._p1
            pw = self.two_packet_wrappers()
            for i in range(len(p1)) : pw.packet1_bytes[i] = p1[i]
            pw.packet1_bytes_num = len(p1)
            pw.packet2_bytes_num =      0
            json_string = self._lib.packets2Json(pw)
            self._p1 = None
            return json_string


    def get_json1(self, data):
        self._p2 = data
        if self._p1 is not None:
            p1 = self._p1
            p2 = self._p2
            pw = two_packet_wrappers()
            for i in range(len(p1)) : pw.packet1_bytes[i] = p1[i]
            pw.packet1_bytes_num = len(p1)
            for i in range(len(p2)) : pw.packet2_bytes[i] = p2[i]
            pw.packet2_bytes_num = len(p2)
            json_string = self._lib.packets2Json(pw)
            self._p1 = None
            self._p2 = None
            return json_string



def parse_vals(filename):
    vals = list()
    with open(filename,"rt") as f: vals = list(f.read().splitlines())

    tj = TestJson()

    tj._expect_packet_2 = True

    for i in range(0, len(vals), 2) :
        if i+1 == len(vals) : break

        pstr = vals[i]
        pstr2 = vals[i+1]
        data = bytearray.fromhex(pstr)
        data2 = bytearray.fromhex(pstr2)

        if data[0] != data2[0] : continue  ## not matching index

        json_string = tj.get_json0(data)
        json_string = tj.get_json1(data2)

        d = json.loads(json_string)
        print("{}:[{}]:[{}]:{}".format(i, pstr, pstr2, d))


def run_test():
    tj = TestJson()

    tj._expect_packet_2 = False

    pstr = "30 00 97 ed 01 30 5d 00 00 00 00 24 00 0d 70 08 ff 00 00 01"
    data = bytearray.fromhex(pstr)
    json_string = tj.get_json0(data)
    d = json.loads(json_string)
    print("[{}]:{}".format(pstr, d))

    pstr = "70 00 c6 dd ef 10 45 01 00 00 00 24 10 a7 16 08 00 00 00 00"
    data = bytearray.fromhex(pstr)
    json_string = tj.get_json0(data)
    d = json.loads(json_string)
    print("[{}]:{}".format(pstr, d))


    pstr = "70 00 c6 dd ef 10 45 01 00 00 00 24 10 a7 16 08 08 1f 0e 02"
    data = bytearray.fromhex(pstr)
    json_string = tj.get_json0(data)
    d = json.loads(json_string)
    print("[{}]:{}".format(pstr, d))


    pstr = "70 00 c6 dd ef 10 45 01 00 00 00 24 10 a7 16 08 08 1f aa 05"
    data = bytearray.fromhex(pstr)
    json_string = tj.get_json0(data)
    d = json.loads(json_string)
    print("[{}]:{}".format(pstr, d))

    tj._expect_packet_2 = True

    pstr = "10 00 02 e1 0f 40 0e 01 00 00 00 30 00 00 00 00 00 00 00 00"
    data = bytearray.fromhex(pstr)
    json_string = tj.get_json0(data)
    if not tj._expect_packet_2 :
      d = json.loads(json_string)
      print("[{}]:{}".format(pstr, d))


    pstr = "10 5d 00 ff f0 00 09 01 04 00 00 00 00 00 00 00 fe ff 10 00"
    data = bytearray.fromhex(pstr)
    json_string = tj.get_json1(data)
    d = json.loads(json_string)
    print("[{}]:{}".format(pstr, d))


    jstr = '{"106":{"brightness":0.3137}}'
    d = json.loads(jstr)
    packets = tj.get_packets(d)
    if len(packets):
      for i, p in enumerate(packets):
        print("{}:{}:[{}]".format(jstr, i, hexstr(p)))


def test_cmd():
    tj = TestJson()

    tj._expect_packet_2 = False

    #jstr = '{"1":{"pwr":6}}'
    #jstr = '{"106":{"brightness":0.3137254901960784}}'
    #jstr = '{"108":{"1":0.3137254901960784,"2":0.5,"3":1}}'
    #jstr = '{"213":{"prcnt":-30}}'
    #jstr = '{"208":{"angular_deg_s":30}}'
    #jstr = '{"211":{"left_cm_s":1.5,"right_cm_s":-1.5}}'
    #jstr = '{"204":{"linear_cm_s":10,"angular_cm_s":4.5}}'
    #jstr = '{"204":{"linear_cm_s":-151}}'
    #jstr = '{"204":{"angular_deg_s":60.5}}'
    #jstr = '{"204":{"linear_cm_s":1,"linear_acc_cm_s_s":0.5}}'
    #jstr = '{"204":{"linear_cm_s":1,"pose":true}}'
    #jstr = '{"205":{"x":25,"y":0,"degree":0,"time":1.25,"dir":2,"mode":6,"wrap_theta":0,"ease":true}}'
    #jstr = '{"205":{"x":-15,"y":-25,"degree":-35,"time":2.50,"dir":2,"mode":5,"wrap_theta":1,"ease":true}}'
    #jstr = '{"205":{"x":-15,"y":-25,"degree":-35,"time":2.50,"dir":2,"mode":3,"wrap_theta":1,"ease":true}}'
    #jstr = '{"205":{"x":-15,"y":-25,"degree":-25,"time":2.50,"dir":2,"mode":4,"wrap_theta":1,"ease":true}}'
    #jstr = '{"5000":{}}'
    #jstr = '{"9000":{"pingID":65535}}'
    #jstr = '{"304":{"type":4,"perc1":2,"perc2":4,"duration":100,"tone1":{"type":3,"freq":300,"phase":30},"tone2":{"type":2,"freq":400},"tone4":{"freq":600}}}'
    #jstr = '{"304":{"type":3,"duration":1000,"tone1":{"type":3,"freq":300,"phase":30}}}'
    #jstr = '{"304":{"tone1":{"type":3,"freq":300},"tone2":{"type":4,"freq":400},"tone3":{"type":3,"freq":500},"tone4":{"type":4,"freq":600},"perc2":-50}}'
    #jstr = '{"304":{"type":3,"tone1":{"freq":300},"tone2":{"freq":400},"tone3":{"freq":500},"tone4":{"freq":600}}}'
    #jstr = '{"300":{"file":"STOPSOUND"}}'
    #jstr = '{"302":{"event_tag":"AK_Mission_Success_1"}}'
    #jstr = '{"410":{"LEDs":[105],"message":20}}'
    #jstr = '{"100":{"animation":2,"brightness":5}}'
    #jstr = '{"100":{"brightness":5}}'
    #jstr = '{"100":{"brightness":[5,10,20,30]}}'
    #jstr = '{"100":{"brightness":[10,20,30,40],"index":[true,true,false,true,true,true,true,true,true,true,true,true]}}'
    #jstr = '{"100":{"animation":1,"index":[true,true,false,true,true,true,true,true,true,true,true,true],"brightness":5}}'
    #jstr = '{"104":{"r":0.5,"b":0.5,"g":0.5}}'
    #jstr = '{"450":{"id":1,"weight":2,"params":{"amp_deg":30,"amp_cm_s":40,"anim":50,"bkup":60,"avg_deg":70,"prd_s":80,"rpt":90,"max_scl":100,"sidelen_cm":8,"sidetm_s":13,"turntm_s":17}}}'
    #jstr = '{"450":{"id":0,"amp_deg":1,"anim":1,"bkup":1,"avg_deg":1,"prd_s":1,"rpt":1,"max_scl":1,"sidetm_s":1,"turntm_s":1}}'
    #jstr = '{"450":{"id":65535}}'
    #jstr = '{"6001":{}}'
    #jstr = '{"5000":{"name":"New name","pvolume":70}}'
    #jstr = '{"5000":{"pvolume":0.4,"peyebright":0.5}}'
    #jstr = '{"5000":{"anim":3,"color":4}}'
    jstr = '{"5000":{"avatar":3,"entr":"111111111111111111","s":true}}'
    d = json.loads(jstr)
    packets = tj.get_packets(d)
    if len(packets):
        for i, p in enumerate(packets):
            print("{}:{}:[{}]".format(jstr, i, hexstr(p)))

def test_cmd_range():
    tj = TestJson()

    tj._expect_packet_2 = False

    for i in range(100,500):
        jstr = '{"' + "{}".format(i) + '":{}}'
        d = json.loads(jstr)
        packets = tj.get_packets(d)
        if len(packets):
            for i, p in enumerate(packets):
                print("{}:{}:[{}]".format(jstr, i, hexstr(p)))




if __name__ == '__main__' :
    #parse_vals('sens.vals')
    test_cmd()
    #test_cmd_range()
