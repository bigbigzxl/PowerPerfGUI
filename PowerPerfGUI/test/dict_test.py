# coding=utf-8
event_dicts = {
    "CPU CYCLES":{
         "Line_X": [],
         "Line_Y": [],
    },
    "INSTRUCTIONS":{
        "Line_X": [],
        "Line_Y": [],
    }
    }

# print event_dicts
name = "INSTRUCTIONS"

# ditc.get()有就返回，没有就返回None

event_dicts["zxl"] = {"Line_X":[1,2,3],
                      "Line_Y":[4,5,6],
                      }
# print event_dicts.get("zxl0")
# print event_dicts
a = ["zxl2", "oas", "zxl1"]


# if "zxl1" in a:
#     print "1111111111"
#
# print a.pop(0), a