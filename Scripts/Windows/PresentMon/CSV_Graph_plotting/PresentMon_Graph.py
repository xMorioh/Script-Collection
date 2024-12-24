import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, fnmatch
import multiprocessing

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
def plotting_graph(csvFile):
    outPath = Output_filePath + os.path.basename(csvFile) + ".svg"
    while True:
        if os.path.exists(outPath):
            break #Do not plot graphs for already existing files
        print("Plotting Graph for " + os.path.basename(csvFile))
        with open(csvFile, "r") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)

            data = {}
            for column in headers:
                data[column] = []

            for row in csv_reader:
                for i, column in enumerate(headers):
                    data[column].append(row[i])

            #Calculate FrameTime Median and convert Values to float
            FrameTime_median = 0
            headerIndex = headers.index("FrameTime")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
                FrameTime_median += data[headers[headerIndex]][i]
            FrameTime_median /= len(data[headers[headerIndex]])

            #Define FrameTime, conversion already done above
            FrameTime = data[headers[headerIndex]]

            #Define DisplayLatency and convert Values to float. DisplayLatency can be NaN in some cases.
            headerIndex = headers.index("DisplayLatency")
            for i in range(len(data[headers[headerIndex]])):
                if data[headers[headerIndex]][i] == 'NA':
                    data[headers[headerIndex]][i] = float(0)
                else:
                    data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            DisplayLatency = data[headers[headerIndex]]

            #Define CPUBusy and convert Values to float
            headerIndex = headers.index("CPUBusy")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            CPUBusy = data[headers[headerIndex]]

            #Define GPUBusy and convert Values to float
            headerIndex = headers.index("GPUBusy")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = float(data[headers[headerIndex]][i])
            GPUBusy = data[headers[headerIndex]]

            #Define Time
            headerIndex = headers.index("CPUStartDateTime")
            for i in range(len(data[headers[headerIndex]])):
                data[headers[headerIndex]][i] = ((data[headers[headerIndex]][i])[11:][:11])
            times = data[headers[headerIndex]]


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
        plt.xlabel('CPU Time\n' + 'Application: ' + str(data[headers[0]][1]) + '', weight='bold')
        plt.ylabel(f'Frame Time in ms: (Lowest: {FTl}), (Highest: {FTh}), (Median: {FrameTime_median})' + 
                   f'\nFrame Rate in FPS: (Lowest: {round(1000/FTh)}), (Highest: {round(1000/FTl)}), (Median: {round(1000/FrameTime_median)})', weight='bold')

        plt.savefig((outPath))
        plt.close(figure)
        #Remove the .csv file after graph has been plotted
        #os.remove(csvFile)

def run_parallel():
    # multiprocessing pool object
    pool = multiprocessing.Pool()

    # input list by finding all csv files in the Input path
    csvFiles = find('*.csv', Input_filePath)

    # pool object with number of element
    pool = multiprocessing.Pool(processes=len(csvFiles))

    # map the function to the list and pass function and input list as arguments
    pool.map(plotting_graph, csvFiles)

    print(f"All Done! Output-> {Output_filePath}")

if __name__ == '__main__':
    run_parallel()