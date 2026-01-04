import os
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from multiprocessing import Pool
import numpy as np
import glob
from datetime import datetime


# Define Input and Output directories
Input_filePath = 'C:\\Program Files (x86)\\Steam\\logs\\'
Output_filePath = Input_filePath
UseCSVFilePathForOutput = True

def process_csv_file(csv_file, svg_file_CPU, svg_file_GPU, svg_files_FrameTime):
    systemInfo = []
    try:
        # Read CSV, skip last two rows (special info)
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            # Skip last two lines (special info)
            systemInfo = lines[-2:]
            lines = lines[:-2]
            if not lines:
                print(f"No data in {csv_file} after skipping last two rows")
                return
            reader = csv.DictReader(lines)
            data = list(reader)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return

    # Extract SystemTimeInSeconds for x-axis
    system_times = []
    cpu_data = {
        'Idle': [],
        'Compositor': [],
        'Application (other)': [],
        'Application (scene)': [],
        'Throttle (frames)': [],
        'Late Start': []
    }
    gpu_data = {
        'Other': [],
        'Compositor': [],
        'Application (other)': [],
        'Application (scene)': [],
        'Present (count)': [],
        'Reprojected': []
    }
    frametime_data = {
        'FrameTime': [],
        'GPUTime': []
    }

    for row in data:
        try:
            # [-1] here is the current value so [-2] is the last one, this also counts for previous time
            system_time = float(row['SystemTimeInSeconds'])
            if system_time == 0:
                system_time = system_times[-2]
            system_times.append(system_time)

            system_time_previous = 0
            if len(system_times) == 1:
                system_time_previous = system_times[-1]
            else:
                system_time_previous = system_times[-2]
            if system_time == 0:
                system_time_previous = system_times[-3]


            # CPU metrics start
            # Application (scene) - NewFrameReadyMs - NewPosesReadyMs
            new_poses_ready = float(row.get('NewPosesReadyMs'))
            new_frame_ready = float(row.get('NewFrameReadyMs'))
            cpu_data['Application (scene)'].append(new_frame_ready - new_poses_ready)

            cpu_data['Idle'].append(float(row.get('CompositorIdleCpuMs', 0.0)))
            cpu_data['Compositor'].append(float(row.get('CompositorRenderCpuMs')) + (new_frame_ready - new_poses_ready))

            # Application (other) - sum of various CPU time metrics
            cpu_data['Application (other)'].append(
                float(row.get('PresentCallCpuMs')) +
                float(row.get('WaitForPresentCpuMs')) +
                float(row.get('SubmitFrameMs')) +
                # Overlay on Application (scene)
                (new_frame_ready - new_poses_ready)
            )

            # Throttle (frames) - extract from ReprojectionFlags
            reprojection_flags = int(row.get('ReprojectionFlags'))
            throttle_count = (reprojection_flags & 0xF00) >> 8
            cpu_data['Throttle (frames)'].append(throttle_count)

            # Late Start
            cpu_data['Late Start'].append(float(row.get('WaitGetPosesCalledMs')))

            # GPU metrics start
            gpu_data['Application (other)'].append(float(row.get('PreSubmitGpuMs')))
            gpu_data['Other'].append(float(row.get('PostSubmitGpuMs')) + float(row.get('PreSubmitGpuMs')))
            gpu_data['Compositor'].append(float(row.get('CompositorRenderGpuMs')) + float(row.get('PreSubmitGpuMs')))

            # Application (scene) - TotalRenderGpuMs - CompositorRenderGpuMs
            total_render_gpu = float(row.get('TotalRenderGpuMs'))
            frametime_data['GPUTime'].append(total_render_gpu)
            gpu_data['Application (scene)'].append((total_render_gpu - gpu_data['Compositor'][-1]) + float(row.get('PreSubmitGpuMs')))

            # Present (count)
            gpu_data['Present (count)'].append(int(row.get('NumFramePresents')))

            # Reprojected - 1 if NumFramePresents > 1, else 0
            gpu_data['Reprojected'].append(int(int(row.get('NumFramePresents')) > 1))

            # FrameTime metrics start
            frame_time = (system_time - system_time_previous) * 1000
            frametime_data['FrameTime'].append(frame_time)

        except Exception as e:
            print(f"Error processing row in {csv_file}: {e}")
            continue

    if not system_times:
        print(f"No valid data in {csv_file}")
        return

    # Ignore dropped or reprojected frames for FrameTime min calculation
    positive_frame_times = [ft for ft in frametime_data['FrameTime'] if ft > 0]

    # Calculate min, max, mean_average for FrameTime
    frame_time_min = round(min(positive_frame_times),6)
    frame_time_max = round(max(frametime_data['FrameTime']),6)
    frame_time_mean_average = round(np.mean(frametime_data['FrameTime']),6)

    frame_rate_min = 1000 / frame_time_max
    frame_rate_max = 1000 / frame_time_min
    frame_rate_mean_average = 1000 / frame_time_mean_average

    late_start_min = round(min(cpu_data['Late Start']),2)
    late_start_max = round(max(cpu_data['Late Start']),2)
    late_start_mean_average = round(np.mean(cpu_data['Late Start']),2)
    # As only positive values are shown we can remove the data that won't be seen anyway to save on filesize
    for i in range(len(cpu_data['Late Start'])):
        if cpu_data['Late Start'][i] < 0:
            cpu_data['Late Start'][i] = -999999.0


    # Create CPU plot
    plt.style.use("dark_background")
    plt.rcParams["grid.alpha"] = 0.2
    plt.figure(figsize=(19.92, 9.92))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    cpu_labels = list(cpu_data.keys())
    cpu_colors = ['#dae6bb', '#64a064', '#7a7ac1', "#6464a0", '#00ffff', '#c41d21']

    for i, label in enumerate(cpu_labels):
        plt.plot(system_times, cpu_data[label], label=label, color=cpu_colors[i])

    plt.title('CPU Metrics Over Time')
    plt.ylabel('Value (ms for time, count for others)', weight='bold')
    plt.xlabel('System Time (seconds)', weight='bold')
    plt.ylim(0, 70)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper right')
    plt.grid(visible=True, which="both", axis="y")
    plt.margins(0.0)
    plt.tight_layout()
    plt.savefig(svg_file_CPU, format='svg')
    plt.close()

    # Create GPU plot
    plt.style.use("dark_background")
    plt.rcParams["grid.alpha"] = 0.2
    plt.figure(figsize=(19.92, 9.92))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))
    gpu_labels = list(gpu_data.keys())
    gpu_colors = ['#82896e', '#64a064', '#7a7ac1', '#6464a0', '#ffffff', '#c41d21']

    for i, label in enumerate(gpu_labels):
        plt.plot(system_times, gpu_data[label], label=label, color=gpu_colors[i])

    plt.title('GPU Metrics Over Time')
    plt.ylabel('Value (ms for time, count for others)', weight='bold')
    plt.xlabel('System Time (seconds)', weight='bold')
    plt.ylim(0, 70)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper right')
    plt.grid(visible=True, which="both", axis="y")
    plt.margins(0.0)
    plt.tight_layout()
    plt.savefig(svg_file_GPU, format='svg')
    plt.close()


    # Create FrameTime plot
    plt.style.use("dark_background")
    plt.rcParams["grid.alpha"] = 0.2
    plt.figure(figsize=(19.92, 9.92))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5))

    # Manually define FPS values and their corresponding frametime in ms
    fps_values = [15, 20, 30, 40, 60, 90, 120, 144]
    frametime_for_fps = [1000 / fps for fps in fps_values] # corresponding frametime in ms

    for fps, frametime in zip(fps_values, frametime_for_fps):
        plt.axhline(y=frametime, color='gray', linestyle='--', alpha=0.25)
        plt.annotate(
            f'{fps}FPS', xy=(system_times[-1], frametime), xytext=(-7, 0), textcoords='offset points', ha='right', color='red', zorder=5, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
        )

    # Data to plot (list of tuples: (data, color, label))
    plot_data =     [frametime_data['GPUTime'], frametime_data['FrameTime'], cpu_data['Compositor'], cpu_data['Late Start']]
    labels =        ['GPU Frametime', 'FrameTime', 'CPU Frametime', 'Late Start']
    alphas =        [1, 0.65, 0.65, 0.75]
    colors =        ["#FEFFB3", '#8DD3C7', '#5057E4', '#FA8174']
    markers =       ['', '_', '', '']
    linewidths =    ['2', '0', '2', '2']
    # Loop to plot all data
    for i in range(len(plot_data)):
        plt.plot(system_times, plot_data[i], color=colors[i], alpha=alphas[i], linewidth=linewidths[i], marker=markers[i], label=labels[i])

    plt.title('FrameTime Metrics Over Time')
    plt.ylabel(f'Frame Time in ms: (Lowest: {frame_time_min}), (Highest: {frame_time_max}), (Mean Average: {frame_time_mean_average})', weight='bold')
    plt.xlabel('System Time (seconds)', weight='bold')
    plt.ylim(0, 70)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper right')

    plt.figtext(0.5, 0.93,
                f'Frame Rate in FPS: (Lowest: {round(frame_rate_min)}), (Highest: {round(frame_rate_max)}), (Mean Average: {round(frame_rate_mean_average)})' +
                f'\nLateStart in ms: (Lowest: {late_start_min}), (Highest: {late_start_max}), (Mean Average: {late_start_mean_average})', weight='bold', ha='center')
    plt.figtext(0.033, 0.93,
                f'GPU: {str(systemInfo[1].split(",")[2]).rstrip(" ")}' +
                f'\nCPU: {str(systemInfo[1].split(",")[3]).rstrip(" ")}', weight='bold', ha='left')

    plt.grid(visible=True, which="both", axis="y")
    plt.margins(0.0)
    plt.tight_layout()
    plt.savefig(svg_files_FrameTime, format='svg')
    plt.close()

    print(f"Processed {csv_file}")

def process_folder(folder_path):
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Filter out files that already have SVG counterparts
    valid_csv_files = []
    svg_files_CPU = []
    svg_files_GPU = []
    svg_files_FrameTime = []
    for csv_file in csv_files:
        if UseCSVFilePathForOutput:
            OutDir = os.path.dirname(csv_file)+'\\'
        else:
            OutDir = Output_filePath
        # Get csv_file last modified date and time
        mod_time = os.path.getmtime(csv_file)
        mod_datetime = datetime.fromtimestamp(mod_time)
        formatted_time = mod_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        svg_file_CPU = f'{OutDir}{os.path.basename(csv_file).rstrip(".csv")}_CPU_{formatted_time}.svg'
        svg_file_GPU = f'{OutDir}{os.path.basename(csv_file).rstrip(".csv")}_GPU_{formatted_time}.svg'
        svg_file_FrameTime = f'{OutDir}{os.path.basename(csv_file).rstrip(".csv")}_FrameTime_{formatted_time}.svg'
        if not os.path.exists(svg_file_CPU) or not os.path.exists(svg_file_GPU) or not os.path.exists(svg_file_FrameTime):
            valid_csv_files.append(csv_file)
            svg_files_CPU.append(svg_file_CPU)
            svg_files_GPU.append(svg_file_GPU)
            svg_files_FrameTime.append(svg_file_FrameTime)

    if not valid_csv_files:
        print(f"No new CSV files to process in {folder_path}")
        return
    with Pool(processes=min(len(valid_csv_files), os.cpu_count())) as pool:
        zipped_args = zip(valid_csv_files, svg_files_CPU, svg_files_GPU, svg_files_FrameTime)
        pool.starmap(process_csv_file, zipped_args)

if __name__ == "__main__":
    if os.path.isdir(Input_filePath):
        process_folder(Input_filePath)
    else:
        print("Invalid folder path")
