from run_experiment import *
import plotperf
import numpy as np

params = get_dualpi2_params()


def varying_target_test(low=0, high=100):
    params = get_dualpi2_params()

    for i in range(high):
        params["target"] = str(i) + "ms"
        params["limit"] = "10000000"
        outfile = "result/%s" % params["target"]
        run_experiment(params, outfile=outfile, iperf_time=20, num_flows=0)
        plotperf.iperf_plot(outfile,
                            title=params["target"],
                            outfile="%s_bandwidth.png" % outfile,
                            param=plotperf.PlotType.Bandwidth,
                            scaler=plotperf.mega_scaler)
        plotperf.iperf_plot(outfile,
                            title=params["target"],
                            outfile="%s_rtt.png" % outfile, 
                            param=plotperf.PlotType.RTT)



def varying_alfa_test(low=0, high=1, step=0.01):
    params = get_dualpi2_params()

    for i in np.arange(low,high,step):
        params["alpha"] = str(i)
        outfile = "result/%s" % params["alpha"]
        run_burst_experiment(params, outfile=outfile, num_flows=10)
        plotperf.iperf_plot(outfile,
                            title=params["alpha"],
                            outfile="%s_band_alpha.png" % outfile,
                            param=plotperf.PlotType.Bandwidth,
                            scaler=plotperf.mega_scaler)
        plotperf.iperf_plot(outfile,
                            title=params["alpha"],
                            outfile="%s_rtt_alpha.png" % outfile,
                            param=plotperf.PlotType.RTT)



def varying_burst_test(low=0, high=50):
    params = get_dualpi2_params()

    outfiles = []

    for i in np.arange(low,high,1):
        outfile = "result/%s_burst" % i
        outfiles.append([outfile, i])
        run_burst_experiment(params, outfile=outfile, num_flows=i, iperf_time=20)
        plotperf.iperf_plot(outfile,
                            title=str(i),
                            outfile="%s_band_burst.png" % outfile,
                            param=plotperf.PlotType.Bandwidth,
                            ylabel="Bandwidth (MBps)",
                            scaler=plotperf.mega_scaler)
        plotperf.iperf_plot(outfile,
                            title=str(i),
                            outfile="%s_rtt_burst.png" % outfile,
                            ylabel="RTT (us)",
                            param=plotperf.PlotType.RTT)
    plotperf.histogram(outfiles, param=plotperf.PlotType.Bandwidth, outfile="bandwidth.png", ylabel="Bandwidth (Bps)")
    plotperf.histogram(outfiles, param=plotperf.PlotType.RTT, outfile="RTT.png", ylabel="RTT (us)")

def varying_long_test(low=0, high=25):
    params = get_dualpi2_params()

    outfiles = []

    for i in np.arange(low,high,1):
        outfile = "result/%s_burst" % i
        outfiles.append([outfile, i])
        run_long_flows_experiment(params, outfile=outfile, num_flows=i, iperf_time=20)
        plotperf.iperf_plot(outfile,
                            title=str(i),
                            outfile="%s_band_long.png" % outfile,
                            param=plotperf.PlotType.Bandwidth,
                            ylabel="Throughput (MBps)",
                            scaler=plotperf.mega_scaler)
        plotperf.iperf_plot(outfile,
                            title=str(i),
                            outfile="%s_rtt_long.png" % outfile,
                            ylabel="RTT (us)",
                            param=plotperf.PlotType.RTT)
    plotperf.histogram(outfiles, param=plotperf.PlotType.Bandwidth, outfile="bandwidth.png", ylabel="Throughput (Bps)")
    plotperf.histogram(outfiles, param=plotperf.PlotType.RTT, outfile="RTT.png", ylabel="RTT (us)")


def long_against_short(low=0, high=25):
    params = get_dualpi2_params()

    outfiles = []

    for i in np.arange(low,high,1):
        outfile = "result/%s_LvsS" % i
        outfiles.append([outfile, i])
        run_long_against_short(params, outfile=outfile, num_flows=i, iperf_time=20)
        plotperf.iperf_plot(outfile,
                            title=str(i),
                            outfile="%s_band_LvsS.png" % outfile,
                            param=plotperf.PlotType.Bandwidth,
                            ylabel="Throughput (MBps)",
                            scaler=plotperf.mega_scaler)
        plotperf.iperf_plot(outfile,
                            title=str(i),
                            outfile="%s_rtt_LvsS.png" % outfile,
                            ylabel="RTT (us)",
                            param=plotperf.PlotType.RTT)
    plotperf.histogram(outfiles, param=plotperf.PlotType.Bandwidth, outfile="bandwidth.png", ylabel="Throughput (Bps)")
    plotperf.histogram(outfiles, param=plotperf.PlotType.RTT, outfile="RTT.png", ylabel="RTT (us)")





long_against_short(0,25)
