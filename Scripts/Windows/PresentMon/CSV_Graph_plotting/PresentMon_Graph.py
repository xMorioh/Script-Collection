#This script requires 'pip install matplotlib' to be run first before calling it
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, fnmatch
import multiprocessing

#Variables
Input_filePath = "C:\\Utilities\\Random Stuff\\Intels PresentMon\\"
Output_filePath = "C:\\Utilities\\Random Stuff\\Intels PresentMon\\"


def findPaths(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def findFile(pattern, path):
    result = False
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result = True
    return result

#Data handling
def graph_plotting(csvFile):
    while True:
        outPathTest = findFile(os.path.basename(csvFile).rstrip(".csv") + '*.svg', Output_filePath)
        if outPathTest:
            break #Do not plot graphs for already existing files
        print("Plotting Graph for " + os.path.basename(csvFile))
        with open(csvFile, "r") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)

            # Create new Lists to work with for each column in the csv file
            data = {}
            for column in headers:
                data[column] = []

            # Populate each new Column/List with the csv files rows
            for row in csv_reader:
                for i, column in enumerate(headers):
                    data[column].append(row[i])

            # Remove first and last entries as the game is not in focus at that time and driver optimizations may scew the graph
            if (len(data[column])) > 300:
                for i, column in enumerate(headers):
                    del data[column][:200]
                    del data[column][(len(data[column]) - 100):len(data[column])]


            #Calculate FrameTime Median and convert Values to float
            FrameTime_median = 0
            headerIndex = headers.index("MsBetweenAppStart")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
                FrameTime_median += data[headers[headerIndex]][i]
            FrameTime_median /= len(data[headers[headerIndex]])
            FrameTime = data[headers[headerIndex]]

            #Define DisplayLatency and convert Values to float. MsBetweenDisplayChange can be NaN in some cases.
            headerIndex = headers.index("MsBetweenDisplayChange")
            for i in range(len(data[headers[headerIndex]])):
                if data[headers[headerIndex]][i] == 'NA':
                    data[headers[headerIndex]][i] = float(0)
                else:
                    data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            MsBetweenDisplayChange = data[headers[headerIndex]]

            #Define MsCPUWait and convert Values to float
            headerIndex = headers.index("MsCPUWait")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            MsCPUWait = data[headers[headerIndex]]

            #Define MsGPUWait and convert Values to float
            headerIndex = headers.index("MsGPUWait")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            MsGPUWait = data[headers[headerIndex]]

            #Define MsCPUBusy and convert Values to float
            headerIndex = headers.index("MsCPUBusy")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            MsCPUBusy = data[headers[headerIndex]]

            #Define MsGPUBusy and convert Values to float
            headerIndex = headers.index("MsGPUBusy")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i]) #+ MsGPUWait[i] #Convert to GPUTime
            MsGPUBusy = data[headers[headerIndex]]

            #Define Time
            headerIndex = headers.index("CPUStartDateTime")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = ((data[headers[headerIndex]][i])[11:][:11])
            times = data[headers[headerIndex]]

            #Define MsAnimationError ground thruth value at 0 point and median
            AnimationError_median = 0
            headerIndex = headers.index("MsAnimationError")
            for i in range(len(data[headers[headerIndex]])):
                AnimationError_median += float(data[headers[headerIndex]][i])
                data[headers[headerIndex]][i-1] = float(data[headers[headerIndex]][i])
            AnimationError_median /= len(data[headers[headerIndex]])
            MsAnimationError = data[headers[headerIndex]]


            #FrameTime highest and lowest
            FTh = 0
            FTl = 255
            for i in FrameTime:
                if i > FTh:
                    FTh = i
                if i < FTl:
                    FTl = i

            #AnimationError highest and lowest
            AEh = 0
            AEl = 255
            for i in MsAnimationError:
                if i > AEh:
                    AEh = i
                if i < AEl:
                    AEl = i


            # Overlay AnimationError on top of Graph Data
            # Using either 1 second in the past from sample point or 12 sample points
            # Using 12 sample points turned out to be best, generally lower counts are best but going too low is not good either
            headerIndex = headers.index("MsAnimationError")
            for i in range(len(data[headers[headerIndex]])):
                #FPSFromSampledFrameTime = int(round(1000 / FrameTime[i]))
                #PastFrameTimes = FrameTime[i-1]
                #for j in range(FPSFromSampledFrameTime):
                #    PastFrameTimes += FrameTime[i-j-1]
                #PastFrameTimes /= (FPSFromSampledFrameTime + 1)
                #data[headers[headerIndex]][i] += PastFrameTimes
                data[headers[headerIndex]][i] += ((FrameTime[i-1] + FrameTime[i-2] + FrameTime[i-3] + FrameTime[i-4] + FrameTime[i-5] + FrameTime[i-6] + FrameTime[i-7] + FrameTime[i-8] + FrameTime[i-9] + FrameTime[i-10] + FrameTime[i-11] + FrameTime[i-12]) / 12)
            MsAnimationError = data[headers[headerIndex]]

        FTh = round(FTh,2)
        FTl = round(FTl,2)
        FrameTime_median = round(FrameTime_median,2)

        AEh = round(AEh,2)
        AEl = round(AEl,2)
        AnimationError_median = round(AnimationError_median,2)

        #Visualization of the Graph
        plt.style.use("dark_background")
        plt.rcParams["xtick.major.top"] = False
        plt.rcParams["xtick.minor.top"] = False
        plt.rcParams["grid.alpha"] = 0.2
        figure = plt.figure()
        ax = figure.add_subplot()
        ax.set_ylim([-30, 60])
        #ax.set_ylim([-FrameTime_median * 1.5, FrameTime_median * 3]) #Auto scale to average frametime, the above is for static y limit
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.margins(0.0)
        ax.grid(visible=True, which="both", axis="y")
        figure.set_size_inches(19.92, 9.92)
        figure.subplots_adjust(0.05, 0.05, 0.99, 0.99, 0.1, 0.1)
        ax.xaxis.set_major_locator(locator=ticker.MaxNLocator(nbins=15))
        figure.autofmt_xdate(rotation='horizontal', bottom=0.075)
        plt.figtext(0.98, 0.1,
                    f'Frame Rate in FPS: (Lowest: {round(1000/FTh)}), (Highest: {round(1000/FTl)}), (Median: {round(1000/FrameTime_median)})' +
                    f'\nAnimation Error in ms: (Lowest: {AEl}), (Highest: {AEh}), (Median: {AnimationError_median})', weight='bold', ha='right')
        #ax.plot(times, list(zip(MsBetweenDisplayChange, MsCPUBusy, MsGPUBusy, MsAnimationError)), label=['DisplayLatency', 'CPUBusy', 'GPUBusy', 'AnimationError'])

        plot_data =     [MsGPUBusy, MsBetweenDisplayChange, MsCPUBusy, MsAnimationError]
        labels =        ['GPUBusy', 'DisplayLatency', 'CPUBusy', 'AnimationError']
        alphas =        [1, 0.65, 0.65, 0.325]
        colors =        ["#FEFFB3", '#8DD3C7', '#5057E4', '#FA8174']
        markers =       ['', '_', '', '']
        linewidths =    ['2', '0', '2', '2']
        for i in range(len(plot_data)):
            ax.plot(times, plot_data[i], color=colors[i], alpha=alphas[i], linewidth=linewidths[i], marker=markers[i], label=labels[i])

        ax.legend()
        plt.xlabel('CPU Time\n' + 'Application: ' + str(data[headers[0]][1]), weight='bold')
        plt.ylabel(f'Frame Time in ms: (Lowest: {FTl}), (Highest: {FTh}), (Median: {FrameTime_median})', weight='bold')

        outPath = f'{Output_filePath}{os.path.basename(csvFile).rstrip(".csv")}_{str(data[headers[0]][1]).rstrip(".exe")}.svg'
        plt.savefig((outPath))
        plt.close(figure)
        #Remove the .csv file after graph has been plotted
        #os.remove(csvFile)

def run_parallel():
    # multiprocessing pool object
    pool = multiprocessing.Pool()

    # input list by finding all csv files in the Input path
    csvFiles = findPaths('*.csv', Input_filePath)

    # pool object with number of element
    pool = multiprocessing.Pool(processes=len(csvFiles))

    # map the function to the list and pass function and input list as arguments
    pool.map(graph_plotting, csvFiles)

    print(f"All Done! Output-> {Output_filePath}")

if __name__ == '__main__':
    run_parallel()
