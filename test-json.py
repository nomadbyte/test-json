#!/usr/bin/env python3

import json
import ctypes
import os
import sys

import math
import struct

PI = math.pi


cm_from_refl = [\
{"refl":0,"front":50,"back":50}, \
{"refl":1,"front":50,"back":50}, \
{"refl":2,"front":50,"back":50}, \
{"refl":3,"front":50,"back":50}, \
{"refl":4,"front":50,"back":50}, \
{"refl":5,"front":50,"back":50}, \
{"refl":6,"front":50,"back":50}, \
{"refl":7,"front":50,"back":50}, \
{"refl":8,"front":50,"back":50}, \
{"refl":9,"front":50,"back":50}, \
{"refl":10,"front":50,"back":50}, \
{"refl":11,"front":30,"back":50}, \
{"refl":12,"front":29,"back":50}, \
{"refl":13,"front":28,"back":50}, \
{"refl":14,"front":27,"back":50}, \
{"refl":15,"front":26,"back":38.75}, \
{"refl":16,"front":25,"back":27.5}, \
{"refl":17,"front":23.75,"back":26.6667}, \
{"refl":18,"front":22.5,"back":25.8333}, \
{"refl":19,"front":21.9444,"back":25}, \
{"refl":20,"front":21.3889,"back":24.375}, \
{"refl":21,"front":20.8333,"back":23.75}, \
{"refl":22,"front":20.2778,"back":23.125}, \
{"refl":23,"front":19.6429,"back":22.5}, \
{"refl":24,"front":18.9286,"back":22.0833}, \
{"refl":25,"front":18.2143,"back":21.6667}, \
{"refl":26,"front":17.5,"back":21.25}, \
{"refl":27,"front":17.1429,"back":20.8333}, \
{"refl":28,"front":16.7857,"back":20.4167}, \
{"refl":29,"front":16.4286,"back":20}, \
{"refl":30,"front":16.0714,"back":19.1667}, \
{"refl":31,"front":15.7143,"back":18.3333}, \
{"refl":32,"front":15.3571,"back":17.5}, \
{"refl":33,"front":15,"back":17.2917}, \
{"refl":34,"front":14.8214,"back":17.0833}, \
{"refl":35,"front":14.6429,"back":16.875}, \
{"refl":36,"front":14.4643,"back":16.6667}, \
{"refl":37,"front":14.2857,"back":16.4583}, \
{"refl":38,"front":14.1071,"back":16.25}, \
{"refl":39,"front":13.9286,"back":16.0417}, \
{"refl":40,"front":13.75,"back":15.8333}, \
{"refl":41,"front":13.5714,"back":15.625}, \
{"refl":42,"front":13.3929,"back":15.4167}, \
{"refl":43,"front":13.2143,"back":15.2083}, \
{"refl":44,"front":13.0357,"back":15}, \
{"refl":45,"front":12.8571,"back":14.881}, \
{"refl":46,"front":12.6786,"back":14.7619}, \
{"refl":47,"front":12.5,"back":14.6429}, \
{"refl":48,"front":12.3958,"back":14.5238}, \
{"refl":49,"front":12.2917,"back":14.4048}, \
{"refl":50,"front":12.1875,"back":14.2857}, \
{"refl":51,"front":12.0833,"back":14.1667}, \
{"refl":52,"front":11.9792,"back":14.0476}, \
{"refl":53,"front":11.875,"back":13.9286}, \
{"refl":54,"front":11.7708,"back":13.8095}, \
{"refl":55,"front":11.6667,"back":13.6905}, \
{"refl":56,"front":11.5625,"back":13.5714}, \
{"refl":57,"front":11.4583,"back":13.4524}, \
{"refl":58,"front":11.3542,"back":13.3333}, \
{"refl":59,"front":11.25,"back":13.2143}, \
{"refl":60,"front":11.1458,"back":13.0952}, \
{"refl":61,"front":11.0417,"back":12.9762}, \
{"refl":62,"front":10.9375,"back":12.8571}, \
{"refl":63,"front":10.8333,"back":12.7381}, \
{"refl":64,"front":10.7292,"back":12.619}, \
{"refl":65,"front":10.625,"back":12.5}, \
{"refl":66,"front":10.5208,"back":12.4286}, \
{"refl":67,"front":10.4167,"back":12.3571}, \
{"refl":68,"front":10.3125,"back":12.2857}, \
{"refl":69,"front":10.2083,"back":12.2143}, \
{"refl":70,"front":10.1042,"back":12.1429}, \
{"refl":71,"front":10,"back":12.0714}, \
{"refl":72,"front":9.94318,"back":12}, \
{"refl":73,"front":9.88636,"back":11.9286}, \
{"refl":74,"front":9.82955,"back":11.8571}, \
{"refl":75,"front":9.77273,"back":11.7857}, \
{"refl":76,"front":9.71591,"back":11.7143}, \
{"refl":77,"front":9.65909,"back":11.6429}, \
{"refl":78,"front":9.60227,"back":11.5714}, \
{"refl":79,"front":9.54545,"back":11.5}, \
{"refl":80,"front":9.48864,"back":11.4286}, \
{"refl":81,"front":9.43182,"back":11.3571}, \
{"refl":82,"front":9.375,"back":11.2857}, \
{"refl":83,"front":9.31818,"back":11.2143}, \
{"refl":84,"front":9.26136,"back":11.1429}, \
{"refl":85,"front":9.20455,"back":11.0714}, \
{"refl":86,"front":9.14773,"back":11}, \
{"refl":87,"front":9.09091,"back":10.9286}, \
{"refl":88,"front":9.03409,"back":10.8571}, \
{"refl":89,"front":8.97727,"back":10.7857}, \
{"refl":90,"front":8.92045,"back":10.7143}, \
{"refl":91,"front":8.86364,"back":10.6429}, \
{"refl":92,"front":8.80682,"back":10.5714}, \
{"refl":93,"front":8.75,"back":10.5}, \
{"refl":94,"front":8.69318,"back":10.4286}, \
{"refl":95,"front":8.63636,"back":10.3571}, \
{"refl":96,"front":8.57955,"back":10.2857}, \
{"refl":97,"front":8.52273,"back":10.2143}, \
{"refl":98,"front":8.46591,"back":10.1429}, \
{"refl":99,"front":8.40909,"back":10.0714}, \
{"refl":100,"front":8.35227,"back":10}, \
{"refl":101,"front":8.29545,"back":9.96711}, \
{"refl":102,"front":8.23864,"back":9.93421}, \
{"refl":103,"front":8.18182,"back":9.90132}, \
{"refl":104,"front":8.125,"back":9.86842}, \
{"refl":105,"front":8.06818,"back":9.83553}, \
{"refl":106,"front":8.01136,"back":9.80263}, \
{"refl":107,"front":7.95455,"back":9.76974}, \
{"refl":108,"front":7.89773,"back":9.73684}, \
{"refl":109,"front":7.84091,"back":9.70395}, \
{"refl":110,"front":7.78409,"back":9.67105}, \
{"refl":111,"front":7.72727,"back":9.63816}, \
{"refl":112,"front":7.67045,"back":9.60526}, \
{"refl":113,"front":7.61364,"back":9.57237}, \
{"refl":114,"front":7.55682,"back":9.53947}, \
{"refl":115,"front":7.5,"back":9.50658}, \
{"refl":116,"front":7.47585,"back":9.47368}, \
{"refl":117,"front":7.45169,"back":9.44079}, \
{"refl":118,"front":7.42754,"back":9.40789}, \
{"refl":119,"front":7.40338,"back":9.375}, \
{"refl":120,"front":7.37923,"back":9.34211}, \
{"refl":121,"front":7.35507,"back":9.30921}, \
{"refl":122,"front":7.33092,"back":9.27632}, \
{"refl":123,"front":7.30676,"back":9.24342}, \
{"refl":124,"front":7.28261,"back":9.21053}, \
{"refl":125,"front":7.25845,"back":9.17763}, \
{"refl":126,"front":7.2343,"back":9.14474}, \
{"refl":127,"front":7.21014,"back":9.11184}, \
{"refl":128,"front":7.18599,"back":9.07895}, \
{"refl":129,"front":7.16184,"back":9.04605}, \
{"refl":130,"front":7.13768,"back":9.01316}, \
{"refl":131,"front":7.11353,"back":8.98026}, \
{"refl":132,"front":7.08937,"back":8.94737}, \
{"refl":133,"front":7.06522,"back":8.91447}, \
{"refl":134,"front":7.04106,"back":8.88158}, \
{"refl":135,"front":7.01691,"back":8.84868}, \
{"refl":136,"front":6.99275,"back":8.81579}, \
{"refl":137,"front":6.9686,"back":8.78289}, \
{"refl":138,"front":6.94444,"back":8.75}, \
{"refl":139,"front":6.92029,"back":8.71711}, \
{"refl":140,"front":6.89614,"back":8.68421}, \
{"refl":141,"front":6.87198,"back":8.65132}, \
{"refl":142,"front":6.84783,"back":8.61842}, \
{"refl":143,"front":6.82367,"back":8.58553}, \
{"refl":144,"front":6.79952,"back":8.55263}, \
{"refl":145,"front":6.77536,"back":8.51974}, \
{"refl":146,"front":6.75121,"back":8.48684}, \
{"refl":147,"front":6.72705,"back":8.45395}, \
{"refl":148,"front":6.7029,"back":8.42105}, \
{"refl":149,"front":6.67874,"back":8.38816}, \
{"refl":150,"front":6.65459,"back":8.35526}, \
{"refl":151,"front":6.63043,"back":8.32237}, \
{"refl":152,"front":6.60628,"back":8.28947}, \
{"refl":153,"front":6.58213,"back":8.25658}, \
{"refl":154,"front":6.55797,"back":8.22368}, \
{"refl":155,"front":6.53382,"back":8.19079}, \
{"refl":156,"front":6.50966,"back":8.15789}, \
{"refl":157,"front":6.48551,"back":8.125}, \
{"refl":158,"front":6.46135,"back":8.09211}, \
{"refl":159,"front":6.4372,"back":8.05921}, \
{"refl":160,"front":6.41304,"back":8.02632}, \
{"refl":161,"front":6.38889,"back":7.99342}, \
{"refl":162,"front":6.36473,"back":7.96053}, \
{"refl":163,"front":6.34058,"back":7.92763}, \
{"refl":164,"front":6.31643,"back":7.89474}, \
{"refl":165,"front":6.29227,"back":7.86184}, \
{"refl":166,"front":6.26812,"back":7.82895}, \
{"refl":167,"front":6.24396,"back":7.79605}, \
{"refl":168,"front":6.21981,"back":7.76316}, \
{"refl":169,"front":6.19565,"back":7.73026}, \
{"refl":170,"front":6.1715,"back":7.69737}, \
{"refl":171,"front":6.14734,"back":7.66447}, \
{"refl":172,"front":6.12319,"back":7.63158}, \
{"refl":173,"front":6.09903,"back":7.59868}, \
{"refl":174,"front":6.07488,"back":7.56579}, \
{"refl":175,"front":6.05072,"back":7.53289}, \
{"refl":176,"front":6.02657,"back":7.5}, \
{"refl":177,"front":6.00242,"back":7.46835}, \
{"refl":178,"front":5.97826,"back":7.43671}, \
{"refl":179,"front":5.95411,"back":7.40506}, \
{"refl":180,"front":5.92995,"back":7.37342}, \
{"refl":181,"front":5.9058,"back":7.34177}, \
{"refl":182,"front":5.88164,"back":7.31013}, \
{"refl":183,"front":5.85749,"back":7.27848}, \
{"refl":184,"front":5.83333,"back":7.24684}, \
{"refl":185,"front":5.80918,"back":7.21519}, \
{"refl":186,"front":5.78502,"back":7.18354}, \
{"refl":187,"front":5.76087,"back":7.1519}, \
{"refl":188,"front":5.73671,"back":7.12025}, \
{"refl":189,"front":5.71256,"back":7.08861}, \
{"refl":190,"front":5.68841,"back":7.05696}, \
{"refl":191,"front":5.66425,"back":7.02532}, \
{"refl":192,"front":5.6401,"back":6.99367}, \
{"refl":193,"front":5.61594,"back":6.96203}, \
{"refl":194,"front":5.59179,"back":6.93038}, \
{"refl":195,"front":5.56763,"back":6.89873}, \
{"refl":196,"front":5.54348,"back":6.86709}, \
{"refl":197,"front":5.51932,"back":6.83544}, \
{"refl":198,"front":5.49517,"back":6.8038}, \
{"refl":199,"front":5.47101,"back":6.77215}, \
{"refl":200,"front":5.44686,"back":6.74051}, \
{"refl":201,"front":5.42271,"back":6.70886}, \
{"refl":202,"front":5.39855,"back":6.67722}, \
{"refl":203,"front":5.3744,"back":6.64557}, \
{"refl":204,"front":5.35024,"back":6.61392}, \
{"refl":205,"front":5.32609,"back":6.58228}, \
{"refl":206,"front":5.30193,"back":6.55063}, \
{"refl":207,"front":5.27778,"back":6.51899}, \
{"refl":208,"front":5.25362,"back":6.48734}, \
{"refl":209,"front":5.22947,"back":6.4557}, \
{"refl":210,"front":5.20531,"back":6.42405}, \
{"refl":211,"front":5.18116,"back":6.39241}, \
{"refl":212,"front":5.157,"back":6.36076}, \
{"refl":213,"front":5.13285,"back":6.32911}, \
{"refl":214,"front":5.1087,"back":6.29747}, \
{"refl":215,"front":5.08454,"back":6.26582}, \
{"refl":216,"front":5.06039,"back":6.23418}, \
{"refl":217,"front":5.03623,"back":6.20253}, \
{"refl":218,"front":5.01208,"back":6.17089}, \
{"refl":219,"front":4.96575,"back":6.13924}, \
{"refl":220,"front":4.89726,"back":6.10759}, \
{"refl":221,"front":4.82877,"back":6.07595}, \
{"refl":222,"front":4.76027,"back":6.0443}, \
{"refl":223,"front":4.69178,"back":6.01266}, \
{"refl":224,"front":4.62329,"back":5.98101}, \
{"refl":225,"front":4.55479,"back":5.94937}, \
{"refl":226,"front":4.4863,"back":5.91772}, \
{"refl":227,"front":4.41781,"back":5.88608}, \
{"refl":228,"front":4.34932,"back":5.85443}, \
{"refl":229,"front":4.28082,"back":5.82278}, \
{"refl":230,"front":4.21233,"back":5.79114}, \
{"refl":231,"front":4.14384,"back":5.75949}, \
{"refl":232,"front":4.07534,"back":5.72785}, \
{"refl":233,"front":4.00685,"back":5.6962}, \
{"refl":234,"front":3.93836,"back":5.66456}, \
{"refl":235,"front":3.86986,"back":5.63291}, \
{"refl":236,"front":3.80137,"back":5.60127}, \
{"refl":237,"front":3.73288,"back":5.56962}, \
{"refl":238,"front":3.66438,"back":5.53797}, \
{"refl":239,"front":3.59589,"back":5.50633}, \
{"refl":240,"front":3.5274,"back":5.47468}, \
{"refl":241,"front":3.4589,"back":5.44304}, \
{"refl":242,"front":3.39041,"back":5.41139}, \
{"refl":243,"front":3.32192,"back":5.37975}, \
{"refl":244,"front":3.25342,"back":5.3481}, \
{"refl":245,"front":3.18493,"back":5.31646}, \
{"refl":246,"front":3.11644,"back":5.28481}, \
{"refl":247,"front":3.04795,"back":5.25316}, \
{"refl":248,"front":2.97945,"back":5.22152}, \
{"refl":249,"front":2.91096,"back":5.18987}, \
{"refl":250,"front":2.84247,"back":5.15823}, \
{"refl":251,"front":2.77397,"back":5.12658}, \
{"refl":252,"front":2.70548,"back":5.09494}, \
{"refl":253,"front":2.63699,"back":5.06329}, \
{"refl":254,"front":2.56849,"back":5.03165}, \
{"refl":255,"front":2.5,"back":5} \
]

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


class TestSensor(object):
    @staticmethod
    def string_into_c_byte_array(str, cba):
        n = 0
        for c in str:
            cba[n] = ord(c)
            n += 1

    class two_packet_wrappers(ctypes.Structure):
        _fields_ = [
            ('packet1_bytes_num', ctypes.c_ubyte),
            ('packet1_bytes'    , ctypes.c_ubyte * 20),
            ('packet2_bytes_num', ctypes.c_ubyte),
            ('packet2_bytes'    , ctypes.c_ubyte * 20),
        ]


    def __init__(self):
        self._load_lib()


    def _load_lib(self):
        lib_path = os.path.join(_ROOT_DIR, _LIB_FILE)
        self._lib = ctypes.cdll.LoadLibrary(lib_path)
        self._lib.packets2Json.restype  = (ctypes.c_char_p)


    def get_json(self, sensor1_data, sensor2_data):
        sensor_packet_1 = sensor1_data
        sensor_packet_2 = sensor2_data

        pw = self.two_packet_wrappers()
        #self.string_into_c_byte_array(sensor_packet_1, pw.packet1_bytes)
        for i in range(len(sensor_packet_1)) : pw.packet1_bytes[i] = sensor_packet_1[i]
        pw.packet1_bytes_num = len(sensor_packet_1)
        pw.packet2_bytes_num = 0

        if sensor_packet_2 is not None:
            #self.string_into_c_byte_array(sensor_packet_2, pw.packet2_bytes)
            for i in range(len(sensor_packet_2)) : pw.packet2_bytes[i] = sensor_packet_2[i]
            pw.packet2_bytes_num = len(sensor_packet_2)

        json = self._lib.packets2Json(pw)
        return json


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


robot_type = 1003 ## TEST:1003:cue, otherwise can get it from ??serial number
clap_info = 0

def get_current_robot_type() :
    global robot_type
    return robot_type


def parse_sensor0_packet(packet0, packet1=None):
    global clap_info

    p = packet0
    assert(len(p) == 20)
    res = {}
    res["tm"] = 0
    b = p[1] | (p[0] & 0x0f) << 8
    res["tm"] = b

    res["2003"] = {}
    d = res["2003"]
    b = p[2] | (p[4] & 0xf0) << 4
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)  # 12bit, signed
    d["x"] = b/2047. * 2   ## resolution: 2/2047.:0.0009770395701025891, 2047.:0x0fff/2.=2047.5 (abs max, so the val gets normalized by max and doubled)
    b = p[3] | (p[4] & 0x0f) << 8
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)  # 12bit, signed
    d["y"] = b/2047. * 2
    b = p[6] | (p[5] & 0xf0) << 4
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)  # 12bit, signed
    d["z"] = b/2047. * 2

    res["5101"] = {}
    d = res["5101"]
    d["data"] = [ b for b in p ]

    res["1000"] = {}
    d = res["1000"]
    d["s"] = int(p[8] & 0x10 != 0)
    res["1001"] = {}
    d = res["1001"]
    d["s"] = int(p[8] & 0x20 != 0)
    res["1002"] = {}
    d = res["1002"]
    d["s"] = int(p[8] & 0x40 != 0)
    res["1003"] = {}
    d = res["1003"]
    d["s"] = int(p[8] & 0x80 != 0)

    has_mic_event = (p[7] != 0)  ## amp, amplitude
    mictconf = 0
    mictdir_deg = 0

    clap_flag = (p[11] & 0b0001)
    has_clap_info = False
    sparse_clap_changed = False
    #print("DBG|p[7]:{:02x} p[9]:{:02x} p[10]:{:02x} p[11]:{:02x}".format(p[7], p[9], p[10], p[11]), "clap_flag:", clap_flag)

    if (p[19] < 0x80) :
        for ofs in range(0, 5, 4) : # first run: 0, second run: -4 
            evt = p[19 - ofs]   # first-pass (p[19], process p[16], ...), second-pass (p[19-4], p[16-4], ...)

            if evt in [0,1,4] :
                pass

            elif evt == 2 :  ## 3006 battery status (p[16,17,18], robotType)
                res["3006"] = {}
                d = res["3006"]
                if get_current_robot_type() == 1003 :  ## cue
                    b = (p[16 - ofs] & 0b11)
                    d["chg"] = int(b == 1 or b == 2)

                    b = (p[16 - ofs] & 0b11100) >> 2  ## 3bit
                    if b == 1 :   d["level"] = 1
                    elif b == 2 : d["level"] = 10
                    elif b == 3 : d["level"] = 20
                    else :        d["level"] = 9999
                else:
                    d["chg"] = int(p[16 - ofs] >= 0x80)  ## 0x80:0b10000000

                    b = p[18 - ofs] >> 5
                    d["level"] = b

                b = p[17 - ofs] | (p[18 - ofs] & 0x1f) << 8  # 13bit
                d["volt"] = b


            elif evt == 5 :  ## 3007 beacon (p[16,17,18])
                res["3007"] = {}
                d = res["3007"]
                b = (p[18 - ofs] | (p[16 - ofs] & 0x0f) << 8)
                d["dataL"] = b
                b = (p[17 - ofs] | (p[16 - ofs] & 0xf0) << 4)
                d["dataR"] = b


            elif evt == 6 :  ## ?? clap
                has_clap_info = True
                #if ofs != 4 and p[19] != 0 : continue
                #if p[19] == 2 : print("DBG|3005:clap ofs:", ofs, "p[19]", p[19], "p[7]:", p[7], "3006:", res["3006"])
                b = (p[16 - ofs] & 0x0f)
                sparse_clap_changed = (clap_info < 0x80 and b != clap_info)
                print("DBG|clap_info:", b, "sparse_clap_changed:", sparse_clap_changed, "ofs:", ofs)
                clap_info = b


            elif evt == 8 :  ## 3005 mic event (p[16,17,18])
                #if p[19] != 0 : continue
                mictconf_a = (p[16 - ofs] & 0xf0) >> 4
                mictconf_b = min(max(0, (p[16 - ofs] & 0x0f) - 3.0), 3.0) / 3.0
                if get_current_robot_type() == 1001:  # dash
                    mictconf_b = mictconf_b * min(p[17 - ofs] & 0x0f, 15) / 15.  ## ?? decrease the confidence
                mictconf = int(min(mictconf_a, 5) / 5. * mictconf_b * 255) & 0xff

                print("DBG|mictconf a:", mictconf_a, "b:", mictconf_b, "mictconf:", mictconf)
                if not ((p[18 - ofs] & 0b100000) == 0 and mictconf > 10) :
                    mictconf = 0
                    mictdir_deg = 0
                else:
                    mictdir_deg = int(( (p[17 - ofs] & 0xf0) >> 4 | (p[18 - ofs] << 4) & 0x01f0  )  * 360 * 1/512.)
                    mictdir_deg = (mictdir_deg - 360 if mictdir_deg > 180 else mictdir_deg)
                    print("DBG|mictdir mictdir_deg:", mictdir_deg)
                #print("DBG|3005 ofs:", ofs, "p[19]", p[19], "p[7]:", p[7], "3006:", res["3006"])
                pass

            else :
                print("E|Short sensor event - unrecognized event: {}".format(evt), file=sys.stderr)

    else :
        evt = p[19]
        if evt == 0x81 :   ## 3009 beacon_v2 (p[12,13,14,15,16,17,18])
            res["3009"] = {}
            d = res["3009"]
            rt = p[12] & 0b0111
            if rt == 0 :
                d["rbtType"] = 1001  ## dash
            elif rt == 1 :
                d["rbtType"] = 1002  ## dot
            elif rt == 2 :
                d["rbtType"] = 1003  ## cue
            else :
                d["rbtType"] = 1000  ## unhandled
                print("E|Beacon received from an unhandled robot type: {}".format(rt), file=sys.stderr)

            d["rbtID"] = (p[12] & 0b11111000) >> 3 | (p[13] & 0b11) << 5

            dt = (p[13] & 0b00001100) >> 2
            d["dataType"] = b
            if dt == 0 :
                d["dataLnBits"] = 4
            elif dt == 1 :
                d["dataLnBits"] = 12
            else :
                d["dataLnBits"] = 30
                print("E|Beacon received with data of unhandled type: {}".format(dt), file=sys.stderr)

            b = (p[14] << 4 | p[13] >> 4 | p[15] << 12 | p[16] << 20 ) & 0xf00000  ## 0xf00000:0b111100000000000000000000
            d["data"] = b

            rcvrs = [0, 0, 0, 0, 0]
            rcvrs[0] = (p[17] & 0b00001110) >> 1
            rcvrs[1] = (p[17] & 0b01110000) >> 4
            rcvrs[2] = (p[17] & 0b10000000) >> 7 | (p[18] & 0b0011) << 1
            rcvrs[3] = (p[18] & 0b00011100) >> 2
            rcvrs[4] = (p[18] & 0b11100000) >> 5
            d["rcvrs"] = rcvrs


        elif evt == 0xff :  ## 9000 ping (p[12,13,14,15,16,17])
            res["9000"] = {}
            d = res["9000"]
            d["pingID"] = p[12] | (p[13] << 8)
            d["pingCount"] = p[14] | (p[15] << 8) | (p[16] << 16) | (p[17] << 24)

        else:
            print("E|Long sensor event - unrecognized event: {}".format(evt), file=sys.stderr)


    res["3005"] = {}
    d = res["3005"]
    d["amp"] = p[7] / 255.
    mictdir = mictdir_deg / 180. * PI  ## in radians for some reason
    if d["amp"] != 0.0 and mictconf > 10 :
        d["mictconf"] = mictconf
        d["mictdir"] = mictdir

    if has_clap_info or clap_flag != 1 :
        if clap_flag == 1 and not sparse_clap_changed :
            print("W|Clap flag set but sparse clap unchanged: likely packet missed.")
        elif clap_flag != 1 and sparse_clap_changed :
            print("W|Clap flag not set and sparse clap changed: packet(s) missed!")
    else:
        print("W|Unexpected: clap flag set but no sparse clap event.")
    d["clap"] = int((has_clap_info and sparse_clap_changed) or clap_flag == 1)


    res["4001"] = {}
    d = res["4001"]
    d["flag"] = int(p[11] & 0x04 != 0)
    res["4002"] = {}
    d = res["4002"]
    d["flag"] = int(p[11] & 0x08 != 0)
    res["4003"] = {}
    d = res["4003"]
    d["flag"] = int(p[11] & 0x02 != 0)
    res["4006"] = {}
    d = res["4006"]
    d["flag"] = int(p[11] & 0x40 != 0)

    x_flag = int(p[11] & 0x01 != 0)    ## ?? some unknown flag
    #if x_flag :
    #    res["????"] = {} ; res["????"]["x_flag"] = x_flag

    return res

   
def get_cm_from_refl(refl, dir):
    if dir not in ["front", "back"]: raise ValueError("Direction should be 'front' or 'back'")
    return cm_from_refl[refl][dir]


def parse_sensor1_packet(packet0, packet1):
    p = packet1
    assert(len(p) == 20)
    res = {}
    res["5102"] = {}
    d = res["5102"]
    d["data"] = [ b for b in p ]

    res["2004"] = {}
    d = res["2004"]
    b = p[5] | ((p[4] & 0x0f) << 8)
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)
    d["r"] = b/2047.*500/180*PI
    b = p[3] | ((p[4] & 0xf0) << 4)
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)
    d["p"] = b/2047.*500/180*PI
    b = p[2] | ((p[0] & 0x0f) << 8)
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)
    d["y"] = b/2047.*500/180*PI
    #print('DBG|s1:2004:{{"r":{:.6g},"p":{:.6g},"y":{:.6g}}}'.format(d["r"],d["p"],d["y"]))

    res["3000"] = {}
    d = res["3000"]
    refl = p[7]
    cm = get_cm_from_refl(refl,"front")
    d["cm"] = cm
    d["refl"] = refl

    res["3001"] = {}
    d = res["3001"]
    refl = p[6]
    cm = get_cm_from_refl(refl,"front")
    d["cm"] = cm
    d["refl"] = refl

    res["3002"] = {}
    d = res["3002"]
    refl = p[8]
    cm = get_cm_from_refl(refl,"back")
    d["cm"] = cm
    d["refl"] = refl

    res["3003"] = {}
    d = res["3003"]
    b = p[14] | (p[15] << 8)
    b = (b - 0x010000 if b >= (0x010000 >> 1) else b)
    d["cm"] = b/1200. * PI * 7.85

    res["3004"] = {}
    d = res["3004"]
    b = p[16] | (p[17] << 8)
    b = (b - 0x010000 if b >= (0x010000 >> 1) else b)
    d["cm"] = b/1200. * PI * 7.85

    res["2000"] = {}
    d = res["2000"]
    b = (p[19] | (p[18] << 8)) & 0x01ff  ## 9bit
    b = (b - 0x0200 if b >= (0x0200 >> 1) else b)
    d["degree"] = b/100./PI *180

    res["2001"] = {}
    d = res["2001"]
    b = (p[18] >> 1)  ## 7bit
    b = (b - 0x80 if b >= (0x80 >> 1) else b)
    d["degree"] = -b/100./PI *180

    res["2002"] = {}
    d = res["2002"]
    b = p[10] | ((p[9] & 0xf0) << 4)
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)
    d["x"] = b/10.
    b = p[11] | ((p[9] & 0x0f) << 8)
    b = (b - 0x1000 if b >= (0x1000 >> 1) else b)
    d["y"] = b/10.
    b = p[12] | (p[13] << 8)
    b = (b - 0x010000 if b >= (0x010000 >> 1) else b)
    d["degree"] = b/1000./PI *180

    if packet0:
        p0 = packet0
        ofs = 4 if p0[19] != 1 else 0
        if p0[19 - ofs] == 1 :
            d["watermark"] = p0[16 - ofs]

    return res


def parse_sensor_data(packet0, packet1):
    d0 = parse_sensor0_packet(packet0, packet1) if packet0 else {}
    d1 = parse_sensor1_packet(packet0, packet1) if packet1 else {}
    d = {**d0, **d1}
    return d


def match_sensor_data(d1, d2, full=False):
    matched = False
    for k in d1 :
        kd1 = d1[k]
        kd2 = d2[k]
        if not type(kd1) == dict:
            if not kd1 == kd2:
                print("DBG|sensor: not matched:", k)
                return matched
            continue

        for kv in kd1 :
            if type(kd1[kv]) == list :
                for i in range(len(kd1[kv])) :
                    eps = math.pow(10,-5 + (0 if kd1[kv][i] == 0 else math.log(abs(kd1[kv][i]), 10)))
                    if not abs(float(kd1[kv][i]) - float(kd2[kv][i])) < eps:
                        print("DBG|sensor: not matched:", k)
                        return matched
            else:
                eps = math.pow(10,-5 + (0 if kd1[kv] == 0 else math.log(abs(kd1[kv]), 10)))
                #print("v:{}, eps: {:.0e}".format(kd1[kv], eps))
                if not abs(float(kd1[kv]) - float(kd2[kv])) < eps :
                    print("DBG|sensor: not matched:", k, kv, kd1[kv], "expected:", kd2[kv])
                    return matched

    if full :
        for k in d2 :
            if not k in d1.keys():
                print("DBG|sensor: missing key:", k)
                return matched

            if not type(d2[k]) == dict : continue
            for kv in d2[k] :
                if not type(d2[k]) == dict : continue
                if kv in d1[k].keys() : continue
                print("DBG|sensor: missing key:", kv)
                return matched

    matched = True
    return matched

def test_sensor():
    ts = TestSensor()
    #data = [ b"\x10\x88\x00\xff\xff\xff\x08\x02K\x00\x00\x00\x00\x00\x00\x00\x01\x00\x04\x00", None ]
    #data = [ b'\xefY\xff\x00\x00\x00\x08\x02K\x00\x00\x00\x00\x00\x00\x00\x01\x00\x06\x00', None ]
    #data = [ b'p\x00\xc6\xdd\xef\x10E\x01\x00\x00\x00$\x10\xa7\x16\x08\x08\x1f\xaa\x05', None ]
    #data = [ b'\x10\x00\x02\xe1\x0f@\x0e\x01\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00', \
    #         b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]

    #data = [ b'\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', \
    #         b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]
    #data = [ b'\x10\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff', \
    #         b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]
    #data = [ b'\x10\x00\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29', \
    #         b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]
    data = [ b'\x10\x00\xff\xff\xff\xff\xff\xff\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', \
             b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]

    #data = [ b'\xc0\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x08\x75\xc8\x96\x08\x00\x00\x00\x00', \
    #
    data = [ b'\xc0\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x86\xff\x00\x00\x00\x34\x56\x81', \
             b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]

    ## 3006:
    #data = [ b'\x90\x00\x26\x8f\x0f\x40\x07\x01\x00\x00\x00\x30\x00\x00\x00\x00\x08\xef\x0d\x02', \
    #         b'\x90\x13\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\xe1\x0d\x00\x00\xfe\xff\x06\x00' ]

    # 3005:clap
    data = [ bytearray([192, 0, 59, 140, 15, 48, 214, 4, 0, 0, 0, 49, 2, 0, 0, 6, 0, 0, 0, 0]), None ]
    data = [ bytearray([0, 0, 39, 133, 15, 64, 16, 1, 0, 0, 0, 48, 1, 0, 0, 6, 0, 0, 0, 0]), \
             bytearray([0, 61, 0, 5, 15, 254, 255, 255, 255, 0, 0, 0, 25, 2, 0, 0, 254, 255, 4, 0]) ]
    data = [ bytearray([208, 0, 252, 244, 255, 64, 13, 43, 0, 0, 0, 49, 13, 0, 0, 6, 0, 0, 0, 0]), None ]

    data = [ b'\x10\x00\xeeN\xff0\xfb\x01\x00\x00\x000d\xe2\xe1\x08\x04\xdd\r\x02', None]

    #data = [ b'\x80\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x30\xf6\xf1\x4e\x08\x00\x00\x00\x00', \
    #         b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]

    #data = [ b'\x10\x00\x02\xe1\x0f@\x0e\x01\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00', \
    #         b'\x10\x00\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29' ]
    #data = [ b'\x10\x00\x02\xe1\x0f@\x0e\x01\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00', \
    #         b'\x10\x00\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9' ]
    #data = [ b'\x10\x00\x02\xe1\x0f@\x0e\x01\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00', \
    #         b'\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' ]

    # watermark packet0:[... 01] ==> 2002:watermark:255, packet0:[... ff ... 01]
    #data = [ bytearray.fromhex("10 00 19 89 0f 40 05 00 00 00 00 30 00 00 00 00 ff 00 00 01")[:], \
    #         bytearray.fromhex("10 9b 00 ff f0 00 ff ff ff 00 00 00 00 00 00 00 fe ff 04 00")[:] ]

    packets = [ bytearray(data[0]), bytearray(data[1]) if data[1] is not None else None ]

    jstr = ts.get_json(packets[0], packets[1])
    print("[{}, {}]:{}".format( \
      hexstr(packets[0]), \
      (hexstr(packets[1]) if packets[1] is not None else None), \
      jstr \
    ))

    #jstr = '{"tm":0,"2003":{"x":0.00195408,"y":-0.0302882,"z":1.01417},"5101":{"data":[16,0,2,225,15,64,14,1,0,0,0,48,0,0,0,0,0,0,0,0]},"1000":{"s":0},"1001":{"s":0},"1002":{"s":0},"1003":{"s":0},"3005":{"amp":0.00392157,"mictconf":0,"mictdir":0,"clap":0},"4001":{"flag":0},"4002":{"flag":0},"4003":{"flag":0},"4006":{"flag":0},"5102":{"data":[16,0,18,19,20,21,22,23,24,25,32,33,34,35,36,37,38,39,40,41]},"2004":{"r":4.45498,"p":1.17236,"y":0.0767365},"3000":{"cm":19.6429,"refl":23},"3001":{"cm":20.2778,"refl":22},"3002":{"cm":22.0833,"refl":24},"3003":{"cm":195.401},"3004":{"cm":205.965},"2000":{"degree":23.4913},"2001":{"degree":-11.4592},"2002":{"x":28.8,"y":-175.9,"degree":515.318}}'
    #jstr = '{"tm":0,"2003":{"x":0.00195408,"y":-0.0302882,"z":1.01417},"5101":{"data":[16,0,2,225,15,64,14,1,0,0,0,48,0,0,0,0,0,0,0,0]},"1000":{"s":0},"1001":{"s":0},"1002":{"s":0},"1003":{"s":0},"3005":{"amp":0.00392157,"mictconf":0,"mictdir":0,"clap":0},"4001":{"flag":0},"4002":{"flag":0},"4003":{"flag":0},"4006":{"flag":0},"5102":{"data":[16,0,242,243,244,245,246,247,248,249,240,241,242,243,244,245,246,247,248,249]},"2004":{"r":5.40992,"p":-0.0554208,"y":1.03168},"3000":{"cm":3.04795,"refl":247},"3001":{"cm":3.11644,"refl":246},"3002":{"cm":5.22152,"refl":248},"3003":{"cm":-52.8578},"3004":{"cm":-42.2945},"2000":{"degree":142.666},"2001":{"degree":2.29183},"2002":{"x":-1.6,"y":-155.1,"degree":-176.815}}'
    #jstr = '{"tm":0,"2003":{"x":0.00195408,"y":-0.0302882,"z":1.01417},"5101":{"data":[16,0,2,225,15,64,14,1,0,0,0,48,0,0,0,0,0,0,0,0]},"1000":{"s":0},"1001":{"s":0},"1002":{"s":0},"1003":{"s":0},"3005":{"amp":0.00392157,"mictconf":0,"mictdir":0,"clap":0},"4001":{"flag":0},"4002":{"flag":0},"4003":{"flag":0},"4006":{"flag":0},"5102":{"data":[16,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255]},"2004":{"r":-0.00426314,"p":-0.00426314,"y":1.0871},"3000":{"cm":2.5,"refl":255},"3001":{"cm":2.5,"refl":255},"3002":{"cm":5,"refl":255},"3003":{"cm":-0.0205513},"3004":{"cm":-0.0205513},"2000":{"degree":-0.572958},"2001":{"degree":0.572958},"2002":{"x":-0.1,"y":-0.1,"degree":-0.0572958}}'

#13410:[f0 00 18 88 0f 40 01 01 00 00 00 30 fa 36 d7 08 00 00 00 00]:[f0 89 00 01 0f ff ff ff ff 00 00 00 19 02 00 00 fe ff 04 00]:{'tm': 0, '2003': {'x': 0.0234489, 'y': -0.117245, 'z': 1.00147}, '5101': {'data': [240, 0, 24, 136, 15, 64, 1, 1, 0, 0, 0, 48, 250, 54, 215, 8, 0, 0, 0, 0]}, '1000': {'s': 0}, '1001': {'s': 0}, '1002': {'s': 0}, '1003': {'s': 0}, '3005': {'amp': 0.00392157, 'mictconf': 102, 'mictdir': -1.74533, 'clap': 0}, '4001': {'flag': 0}, '4002': {'flag': 0}, '4003': {'flag': 0}, '4006': {'flag': 0}, '5102': {'data': [240, 137, 0, 1, 15, 255, 255, 255, 255, 0, 0, 0, 25, 2, 0, 0, 254, 255, 4, 0]}, '2004': {'r': -0.00426314, 'p': 0.00426314, 'y': 0}, '3000': {'cm': 2.5, 'refl': 255}, '3001': {'cm': 2.5, 'refl': 255}, '3002': {'cm': 5, 'refl': 255}, '3003': {'cm': 0}, '3004': {'cm': -0.0411025}, '2000': {'degree': 0}, '2001': {'degree': -1.14592}, '2002': {'x': 0, 'y': 0, 'degree': 30.7678}}


    data = [ bytearray([16,0,2,225,15,64,14,1,0,0,0,48,0,0,0,0,0,0,0,0]), None ]  # "2003":{"x":0.00195408,"y":-0.0302882,"z":1.01417}
    data = [ bytearray([144, 0, 38, 143, 15, 64, 7, 1, 0, 0, 0, 48, 0, 0, 0, 0, 8, 239, 13, 2]), None ]  # 1003:"3006":{"chg":True,"level":10,"volt":, 1001:"3006":{"chg":0,"level":0,"volt":3567}
    data = [ bytearray([112, 0, 198, 221, 239, 16, 69, 1, 0, 0, 0, 36, 16, 167, 22, 8, 8, 31, 170, 5]), None ]  # "3007":{"dataL":2218,"dataR":31}
    data = [ bytearray([192,0,0,0,0,0,0,255,0,0,0,35,134,201,150,8,0,0,0,0]), None ]  # "3005":{"amp":1,"mictconf":153,"mictdir":-1.8326,"clap":1}, "unexpected: clap flag set but no sparse clap event."
    #data = [ bytearray([192,0,0,0,0,0,0,255,0,0,0,0,133,255,0,0,255,255,255,255]), None ]  # "9000":{"pingID":65413,"pingCount":4294901760}
    #data = [ bytearray([192,0,0,0,0,0,0,255,0,0,0,0,134,255,0,0,0,52,86,129]), None ]  # "3009":{"rbtType":1000,"rbtID":112,"dataType":3,"dataLnBits":30,"data":15,"rcvrs":[2,3,4,5,2]}, error: unhandled robot type, data_type
    #data = [ b'\x10\x00\xeeN\xff0\xfb\x01\x00\x00\x000d\xe2\xe1\x08\x04\xdd\r\x02', None]
    data = [ bytearray([240, 0, 24, 136, 15, 64, 1, 1, 0, 0, 0, 48, 250, 54, 215, 8, 0, 0, 0, 0]), bytearray([240, 137, 0, 1, 15, 255, 255, 255, 255, 0, 0, 0, 25, 2, 0, 0, 254, 255, 4, 0]) ] ##  '3005': {'amp': 0.00392157, 'mictconf': 102, 'mictdir': -1.74533, 'clap': 0}
    packets = [ bytearray(data[0]), bytearray(data[1]) if data[1] is not None else None ]
    if packets[0] :
        s0_data = parse_sensor0_packet(packets[0], packets[1])
        print("DBG|s0:", s0_data)
    #
    #    if not match_sensor0_data(s0_data, json.loads(jstr)):
    #        print("DBG|s0: not matched")

    if packets[1] :
        s1_data = parse_sensor1_packet(packets[0], packets[1])
        print("DBG|s1:", s1_data)
    #
    #    if not match_sensor1_data(s1_data, json.loads(jstr)):
    #        print("DBG|s1: not matched")

def test_sensor_refl_cm():
    ts = TestSensor()
    data = [ b'\x10\x00\x02\xe1\x0f@\x0e\x01\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00', \
             b'\x10\x00\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xf0\xf1\xf2\xf3\xf4\xf5\xf6\x17\xf8\xf9' ]

    packets = [ bytearray(data[0]), bytearray(data[1]) if data[1] is not None  else None ]

    for i in range(256):
        packets[1][6] = i
        packets[1][8] = i

        jstr = ts.get_json(packets[0], packets[1])
        print("[{}, {}]:{}".format( \
          hexstr(packets[0]), \
          (hexstr(packets[1]) if packets[1] is not None else None), \
          jstr \
        ))
        d = json.loads(jstr)
        print("DBG|0x{:02x},{},{},{}".format(i, d['3001']['refl'], d['3001']['cm'], d['3002']['cm']))


def test_sensor_byte(s, n):
    ts = TestSensor()
    data = [ b'\xc0\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x85\xff\x00\x04\x00\x00\x00\x00', \
             b'\x10]\x00\xff\xf0\x00\x08\x02\x03\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00' ]

    packets = [ bytearray(data[0]), bytearray(data[1]) if data[1] is not None  else None ]

    for i in range(256):
        packets[s][n] = i

        jstr = ts.get_json(packets[0], packets[1])
        print("[{}, {}]:{}".format( \
          hexstr(packets[0]), \
          (hexstr(packets[1]) if packets[1] is not None else None), \
          jstr \
        ))
        #d = json.loads(jstr)


def test_sensor_data(fname):
    with open(fname, "r") as f:
        ln = 0
        ln1 = 0 ; ln2 = 0
        packets = [None, None]
        for line in f :
            ln += 1
            line = line.replace("\r","").replace("\n","")
            flds = line.split("|")
            sid = int(flds[0], 16)  ## sensor handle num
            p = bytearray.fromhex(flds[1])
            if sid == 0x17 :
                ln1 = ln
                packets[0] = p[:]
                packets[1] = None
                print("b15:{:02x}, b19:{:02x}".format(packets[0][15], packets[0][19]))
                s0 = parse_sensor0_packet(packets[0], packets[1])
                print("{}:{}".format(ln1, s0))
            elif sid == 0x1a :
                ln2 = ln
                packets[1] = p[:]
                if packets[0] and packets[0][0] == (packets[1][0] & 0xf0) : ## matching seq
                     #print("DBG|{}:[{:02x} {:02x}]:[{:02x} {:02x}]".format(ln1, packets[0][0], packets[0][1], packets[1][0], packets[1][1]))
                     s0 = parse_sensor0_packet(packets[0], packets[1])
                     print("{}:{}".format(ln2, s0))
                     s1 = parse_sensor1_packet(packets[0], packets[1])
                     print("{}:{}".format(ln2, s1))
                     continue
                ## out-of-seq packet1, process packets separately
                print("W|Out of seq ln1:{}, ln2:{}".format(ln1, ln2), file=sys.stderr)
                if packets[0] :
                     pass
                if packets[1] :
                     pass

def test_sensor_out_json(fname):
    with open(fname, "r") as f:
        ln = 0
        packets = [None, None]
        for line in f :
            ln += 1
            line = line.replace("\r","").replace("\n","")
            data = json.loads(line)
            packets[0] = data["5101"]["data"][:]
            packets[1] = data["5102"]["data"][:]
            #print("DBG|{}:[{:02x} {:02x}]:[{:02x} {:02x}]".format(ln1, packets[0][0], packets[0][1], packets[1][0], packets[1][1]))
            if packets[0][15] == 0x06: print("DBG|input:3005:", data["3005"], "5101:", data["5101"])
            s = parse_sensor_data(packets[0], packets[1])
            print("{}:{}".format(ln, s))

            if not match_sensor_data(s, data, full=True):
                print("DBG|s: not matched")
            continue


if __name__ == '__main__' :
    #parse_vals('sens.vals')
    #test_cmd()
    #test_cmd_range()
    #test_sensor()
    #test_sensor_byte(0, 15)
    #test_sensor_refl_cm()
    test_sensor_data(sys.argv[1])
    #test_sensor_out_json(sys.argv[1])

