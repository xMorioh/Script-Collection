import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
from multiprocessing import Pool
import glob
from datetime import datetime


# Define Input and Output directories
Input_filePath = 'C:\\Program Files (x86)\\Steam\\logs\\'
Output_filePath = Input_filePath
UseCSVFilePathForOutput = True

def process_csv_file(csv_file, svg_file):
    frames = []
    systemInfo = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            frames.append(row)

    # Remove last 2 rows but save them into systemInfo
    systemInfo = frames[-2:]
    frames = frames[:-2]

    # Initialize lists
    frame_time_ms = []
    cpu_frametime_ms = []
    gpu_frametime_ms = []
    late_start_ms = []
    system_times = []

    for i in range(1, len(frames)):
        try:
            row = frames[i]
            prev_row = frames[i-1]

            # Convert fields
            row['SystemTimeInSeconds'] = float(row['SystemTimeInSeconds'])
            row['NewFrameReadyMs'] = float(row['NewFrameReadyMs'])
            row['NewPosesReadyMs'] = float(row['NewPosesReadyMs'])
            row['CompositorRenderCpuMs'] = float(row['CompositorRenderCpuMs'])
            row['WaitGetPosesCalledMs'] = float(row['WaitGetPosesCalledMs'])
            row['TotalRenderGpuMs'] = float(row['TotalRenderGpuMs'])
            row['CompositorIdleCpuMs'] = float(row['CompositorIdleCpuMs'])
            row['WaitForPresentCpuMs'] = float(row['WaitForPresentCpuMs'])
            row['PresentCallCpuMs'] = float(row['PresentCallCpuMs'])
            prev_row['SystemTimeInSeconds'] = float(prev_row['SystemTimeInSeconds'])

            # Calculate metrics
            frame_time = max(0, (row['SystemTimeInSeconds'] - prev_row['SystemTimeInSeconds']) * 1000)
            # If FrameTime is wanky due to reused frames or something then just use the data from before.
            if frame_time == 0:
                frame_time = max(0, (row['SystemTimeInSeconds'][i-1] - row['SystemTimeInSeconds'][i-2]) * 1000)
            frame_time_ms.append(frame_time)

            cpu_frametime = row['NewFrameReadyMs'] - row['NewPosesReadyMs'] + row['CompositorRenderCpuMs']
            cpu_frametime_ms.append(cpu_frametime)

            gpu_frametime = row['TotalRenderGpuMs']
            gpu_frametime_ms.append(gpu_frametime)

            late_start = row['WaitGetPosesCalledMs']
            late_start_ms.append(late_start)

            if late_start > 50.0:
                print(late_start)

            system_times.append(row['SystemTimeInSeconds'])

        except Exception as e:
            print(f"Skipping row {i} due to error: {e}")
            continue

    # Calculate min, max, median for FrameTime, FrameRate and Late Start
    frame_time_min = round(min(frame_time_ms),2)
    frame_time_max = round(max(frame_time_ms),2)
    frame_time_median = round(np.median(frame_time_ms),2)

    frame_rate_min = 1000 / frame_time_max #if frame_time_max > 0 else 0
    frame_rate_max = 1000 / frame_time_min #if frame_time_min > 0 else 0
    frame_rate_median = 1000 / frame_time_median #if frame_time_median > 0 else 0

    late_start_min = round(min(late_start_ms),2)
    late_start_max = round(max(late_start_ms),2)
    late_start_median = round(np.median(late_start_ms),2)

    for i in range(len(late_start_ms)):
        if late_start_ms[i] < 0:
            late_start_ms[i] = -999999.0


    # Plot Graph
    plt.style.use("dark_background")
    plt.rcParams["grid.alpha"] = 0.2
    figure = plt.figure()
    figure.set_size_inches(19.92, 9.92)
    ax = figure.add_subplot()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    #figure.subplots_adjust(0.05, 0.05, 0.99, 0.99, 0.1, 0.1)
    #figure.autofmt_xdate(rotation='horizontal', bottom=0.075)
    ax.margins(0.0)
    ax.grid(visible=True, which="both", axis="y")
    ax.set_ylim(0, 70)
    ax.set_title('FrameTime Metrics Over Time')
    ax.set_xlabel('System Time (seconds)', weight='bold')
    ax.set_ylabel(f'Frame Time in ms: (Lowest: {frame_time_min}), (Highest: {frame_time_max}), (Median: {frame_time_median})', weight='bold')
    figure.tight_layout()

    # Manually define FPS values and their corresponding frametime in ms
    fps_values = [15, 20, 30, 40, 60, 90, 120, 144]
    frametime_for_fps = [1000 / fps for fps in fps_values] # corresponding frametime in ms

    for fps, frametime in zip(fps_values, frametime_for_fps):
        ax.axhline(y=frametime, color='gray', linestyle='--', alpha=0.25)
        ax.annotate(
            f'{fps}FPS', xy=(system_times[-1], frametime), xytext=(-7, 0), textcoords='offset points', ha='right', color='red', zorder=5, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
        )

    # Data to plot (list of tuples: (data, color, label))
    plot_data =     [gpu_frametime_ms, frame_time_ms, cpu_frametime_ms, late_start_ms]
    labels =        ['GPU Frametime', 'FrameTime', 'CPU Frametime', 'Late Start']
    alphas =        [1, 0.65, 0.65, 0.75]
    colors =        ["#FEFFB3", '#8DD3C7', '#5057E4', '#FA8174']
    markers =       ['', '_', '', '']
    linewidths =    ['2', '0', '2', '2']
    # Loop to plot all data
    for i in range(len(plot_data)):
        ax.plot(system_times, plot_data[i], color=colors[i], alpha=alphas[i], linewidth=linewidths[i], marker=markers[i], label=labels[i])

    ax.legend(bbox_to_anchor=(1, 1), loc='upper right')

    plt.figtext(0.5, 0.93,
                f'Frame Rate in FPS: (Lowest: {round(frame_rate_min)}), (Highest: {round(frame_rate_max)}), (Median: {round(frame_rate_median)})' +
                f'\nLateStart in ms: (Lowest: {late_start_min}), (Highest: {late_start_max}), (Median: {late_start_median})', weight='bold', ha='center')
    plt.figtext(0.033, 0.93,
                f'{str(systemInfo[0]["NumMisPresented"]).upper()}: {str(systemInfo[1]["NumMisPresented"]).rstrip(" ")}' +
                f'\n{str(systemInfo[0]["NumDroppedFrames"]).upper()}: {str(systemInfo[1]["NumDroppedFrames"]).rstrip(" ")}', weight='bold', ha='left')



    # Save as SVG
    plt.savefig(svg_file, format='svg')
    print(f"Saved graph for {csv_file} as {svg_file}")
    plt.close()

    print(f"Processed {csv_file}")

def process_folder(folder_path):
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Filter out files that already have SVG counterparts
    valid_csv_files = []
    svg_files = []
    for csv_file in csv_files:
        if UseCSVFilePathForOutput:
            OutDir = os.path.dirname(csv_file)+'\\'
        else:
            OutDir = Output_filePath
        # Get csv_file last modified date and time
        mod_time = os.path.getmtime(csv_file)
        mod_datetime = datetime.fromtimestamp(mod_time)
        formatted_time = mod_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        svg_file = f'{OutDir}{os.path.basename(csv_file).rstrip(".csv")}_FrameTime_{formatted_time}.svg'
        if not os.path.exists(svg_file):
            valid_csv_files.append(csv_file)
            svg_files.append(svg_file)

    if not valid_csv_files:
        print(f"No new CSV files to process in {folder_path}")
        return
    with Pool(processes=min(len(valid_csv_files), os.cpu_count())) as pool:
        zipped_args = zip(valid_csv_files, svg_files)
        pool.starmap(process_csv_file, zipped_args)

if __name__ == '__main__':
    if os.path.isdir(Input_filePath):
        process_folder(Input_filePath)
    else:
        print("Invalid folder path")
