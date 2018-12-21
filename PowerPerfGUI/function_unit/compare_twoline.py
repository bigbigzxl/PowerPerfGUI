Int8_NCNN       = []
Int8_Venus      = []

COMPARE_WHAT = "CPU_CYCLES"

with open("NCNNdata_32bit.txt", "rb") as f:
    for line in f:
        if COMPARE_WHAT in line:
            value = float(line.split(",")[-1].replace(" ", "").split("=")[-1])
            Int8_NCNN.append(value)

with open("Venusdata_32bit.txt", "rb") as f:
    for line in f:
        if COMPARE_WHAT in line:
            value = float(line.split(",")[-1].replace(" ", "").split("=")[-1])
            Int8_Venus.append(value)


print "Int8NCNN     : %d"%len(Int8_NCNN)
print "Int8Venus    : %d"%len(Int8_Venus)



import matplotlib.pyplot as plt

# plt.figure(figsize=(8, 6), dpi=80)

plt.plot(Int8_NCNN , "--o", label="NCNN Int8")
plt.plot(Int8_Venus, "--o", label="new Int8")
if len(Int8_NCNN) == len(Int8_Venus):
    for ratio in list(map(lambda x: float(x[0]-x[1]) / x[0], zip(Int8_NCNN, Int8_Venus))):
        print ( "%.2f%%"%(ratio*100.0))

plt.legend()
plt.xlabel("Layer size Index(0~16)")
plt.ylabel("%s Value"%COMPARE_WHAT)
plt.title("compare %s"%COMPARE_WHAT)
plt.grid(True)
plt.show()