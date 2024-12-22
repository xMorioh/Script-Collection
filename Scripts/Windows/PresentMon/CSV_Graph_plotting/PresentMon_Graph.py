import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, fnmatch

#Variables
Input_filePath = "C:\\Utilities\\Random Stuff\\Intels PresentMon\\"
Output_filePath = "C:\\Utilities\\Random Stuff\\Intels PresentMon\\"


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


#Data handling
csvFiles = find('*.csv', Input_filePath)
for csvFile in csvFiles:
    print("Plotting Graph for " + str(csvFile))
    with open(csvFile, "r") as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
            
        data = {}
        for column in headers:
            data[column] = []

        for row in csv_reader:
            for i, column in enumerate(headers):
                data[column].append(row[i])

        #Calculate DisplayLatency Median and convert Values to float
        FrameTime_median = 0
        for i in range(len(data[headers[9]])):
            data[headers[9]][i] = float(data[headers[9]][i])
            FrameTime_median += data[headers[9]][i]
        FrameTime_median /= len(data[headers[9]])

        #Define FrameTime, conversion already done above
        FrameTime = data[headers[9]]

        #Define DisplayLatency and convert Values to float
        for i in range(len(data[headers[16]])):
            data[headers[16]][i] = float(data[headers[16]][i])
        DisplayLatency = data[headers[16]]

        #Define CPUBusy and convert Values to float
        for i in range(len(data[headers[10]])):
            data[headers[10]][i] = float(data[headers[10]][i])
        CPUBusy = data[headers[10]]

        #Define GPUBusy and convert Values to float
        for i in range(len(data[headers[14]])):
            data[headers[14]][i] = float(data[headers[14]][i])
        GPUBusy = data[headers[14]]

        #Define Time
        for i in range(len(data[headers[8]])):
            data[headers[8]][i] = ((data[headers[8]][i])[11:][:11])
        times = data[headers[8]]


        FTh = 0
        FTl = 255
        for i in FrameTime:
            if i > FTh:
                FTh = i
            if i < FTl:
                FTl = i

    FTh = round(FTh,2)
    FTl = round(FTl,2)
    FrameTime_median = round(FrameTime_median,2)
    print("Display Latency: Low", FTl)
    print("Display Latency: High", FTh)
    print("Display Latency: Median", FrameTime_median)

    #Visualization of the Graph
    plt.style.use("dark_background")
    plt.rcParams["xtick.major.top"] = False
    plt.rcParams["xtick.minor.top"] = False
    plt.rcParams["grid.alpha"] = 0.2
    plt.rcParams["lines.linewidth"] = 2
    figure = plt.figure()
    ax = figure.add_subplot()
    ax.set_ylim([0, 100])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.margins(0.0)
    ax.grid(visible=True, which="both", axis="y")
    figure.set_size_inches(19.92, 9.92)
    figure.subplots_adjust(0.05, 0.05, 0.99, 0.99, 0.1, 0.1)
    ax.xaxis.set_major_locator(locator=ticker.MaxNLocator(nbins=15))
    figure.autofmt_xdate(rotation='horizontal', bottom=0.075)
    ax.plot(times, list(zip(DisplayLatency, CPUBusy, GPUBusy)), label=['DisplayLatency', 'CPUBusy', 'GPUBusy'])
    ax.legend()
    plt.xlabel('Time\n' + 'Application: ' + str(data[headers[0]][1]) + '', weight='bold')
    plt.ylabel(f'Frame Time in ms: (Lowest: {FTl}), (Highest: {FTh}), (Median: {FrameTime_median})' + 
               f'\nFrame Rate in FPS: (Lowest: {round(1000/FTh)}), (Highest: {round(1000/FTl)}), (Median: {round(1000/FrameTime_median)})', weight='bold')
    outPath = Output_filePath + os.path.basename(csvFile) + ".svg"
    plt.savefig((outPath))
    plt.close(figure)
    #Remove the .csv file after graph has been plotted
    #os.remove(csvFile)
print("All Done!")