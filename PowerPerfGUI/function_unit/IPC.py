
import matplotlib.pyplot as plt


def draw_one_line(path):
    I = []
    C = []
    IPC = []
    with open(path, "rb") as f:
        for line in f:
            if "CPU_CYCLES" in line:
                value = float(line.split(",")[-1].replace(" ", "").split("=")[-1])
                C.append(value)

            if "INST_RETIRED" in line:
                value = float(line.split(",")[-1].replace(" ", "").split("=")[-1])
                I.append(value)

    print "cycles         : %d"%len(C)
    print "Instruction    : %d"%len(I)

    # plt.plot(I, "--o" , label="Instruction", alpha=0.3)
    # plt.plot(C, "--o" , label="cycles", alpha=0.3)

    if len(I) == len(C):
        IPC = list(map(lambda x: x[0] / x[1], zip(I, C)))
        plt.plot(IPC, "--o" , label=path.split(".")[0], alpha=0.9)



draw_one_line("NCNNdata_32bit.txt")
draw_one_line("Venusdata_32bit.txt")


plt.legend()
plt.title("For selected sizes")
plt.show()