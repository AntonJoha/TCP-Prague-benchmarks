from typing import List, Dict
import matplotlib.pyplot as plt
from enum import Enum

class PlotType(Enum):
    Transfer="transfer"
    Bandwidth="throughput"
    Write="write"
    Err="err"
    Rtry="rtry"
    Cwnd="cwnd"
    RTT="rtt"
    Var="var"
    NetPwr="netpwr"


def mega_scaler(y):
    return [i/10**6 for i in y]

def _remove_dup(s: str) -> str:
    to_return = ""
    for i in s:
        if i == "," and to_return[-1] == ",":
            continue
        to_return += i
    return to_return

def _handle_line(i: str) -> Dict[str, any]:
    i = _remove_dup(i.strip("\n").replace(" ", ","))
    values = i.split(",")
    res = {}
    #[,1],1.1000-1.2000,sec,156524,Bytes,1565224,Bytes/sec,2/0,0,35K/31397(701),us,49.85
    #Remove the ID
    values = values[2:]
    #Get time
    res["time"] = float(values[0].split("-")[1])
    values = values[2:]
    # Get total transfer
    res["transfer"] = float(values[0])
    values = values[2:]
    res["throughput"] = float(values[0])
    values = values[2:]
    res["write"] = float(values[0].split("/")[0])
    res["err"] = float(values[0].split("/")[1])
    values = values[1:]
    res["rtry"] = float(values[0])
    values = values[1:]
    
    # A mouthfull, splitting 35K/31397(701)
    try:
        res["cwnd"] = float(values[0].split("/")[0].strip("K"))
    except:
        print(":)")
    res["rtt"] = float(values[0].split("/")[1].split("(")[0])
    res["variance"] = float(values[0].split("/")[1].split("(")[1].split(")")[0])
    values = values[2:]
    res["NetPwr"] = float(values[0])
    return res

def _make_dict(filename) -> List[Dict[str, float]]:
    measurements = []
    lines =  []
    with open(filename, "r") as f:
        lines = f.readlines()

    while "NetPwr" not in lines[0]:
        lines = lines[1:]
    lines = lines[1:]
    for i in lines:
        measurements.append(_handle_line(i))

    return measurements[:-1]

def _get_last(filename) -> List[Dict[str,float]]:
    measurements = []
    lines =  []
    with open(filename, "r") as f:
        lines = f.readlines()

    while "NetPwr" not in lines[0]:
        lines = lines[1:]
    lines = lines[1:]
    for i in lines:
        measurements.append(_handle_line(i))

    return measurements[-1]



def _get_column(entries, key):
    to_return = []
    for i in entries:
        to_return.append(i[key])
    return to_return


def iperf_plot(filename: str, title: str= None, outfile:str = None, param=PlotType.Bandwidth, ylabel="Throughput Bps", scaler=None) -> None:



    if title is None:
        print("No title set, using filename...")
        title = filename
    if outfile is None:
        outfile = "%s_plot.png" % filename

    d = _make_dict(filename)


    y = _get_column(d, param.value)
    if scaler is not None:
        y = scaler(y)


    x = _get_column(d, "time")
    fig, ax = plt.subplots()
    ax.set(xlabel="Time (s)", ylabel=ylabel, title=title)
    ax.plot(x, y)

    fig.savefig(outfile)
    plt.close()

def histogram(filenames, param=PlotType.Bandwidth, outfile="test.png",ylabel="Bandwidth (bps)",  xlabel="Flows per burst"):
    x = []
    y = []
    for i in filenames:
        x.append(i[1])
        y.append(_get_last(i[0])[param.value])

    fig, ax = plt.subplots()
    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.plot(x, y)

    fig.savefig(outfile)
    plt.close()


