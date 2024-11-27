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
        ('packet1_bytes_num', ctypes.c_byte),
        ('packet1_bytes'    , ctypes.c_byte * 20),
        ('packet2_bytes_num', ctypes.c_byte),
        ('packet2_bytes'    , ctypes.c_byte * 20),
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
            ('packet1_bytes_num', ctypes.c_byte),
            ('packet1_bytes'    , ctypes.c_byte * 20),
            ('packet2_bytes_num', ctypes.c_byte),
            ('packet2_bytes'    , ctypes.c_byte * 20),
        ]



    def get_json0(self, data):
        self._p1 = data
        if not self.expect_packet_2:
            p1 = self._p1
            pw = two_packet_wrappers()
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


if __name__ == '__main__' :
    run_test()
