import os
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from multiprocessing import Pool
import glob
from datetime import datetime


# Define Input and Output directories
Input_filePath = 'C:\\Program Files (x86)\\Steam\\logs\\'
Output_filePath = Input_filePath
UseCSVFilePathForOutput = True

def process_csv_file(csv_file, svg_file_CPU, svg_file_GPU):
    try:
        # Read CSV, skip last two rows (special info)
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            # Skip last two lines (special info)
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

    for row in data:
        try:
            system_time = max(0, float(row['SystemTimeInSeconds']))
            if system_time == 0:
                system_time = max(0, system_time[-1])
            system_times.append(system_time)

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
            gpu_data['Application (scene)'].append((total_render_gpu - gpu_data['Compositor'][-1]) + float(row.get('PreSubmitGpuMs')))

            # Present (count)
            gpu_data['Present (count)'].append(int(row.get('NumFramePresents')))

            # Reprojected - 1 if NumFramePresents > 1, else 0
            gpu_data['Reprojected'].append(int(int(row.get('NumFramePresents')) > 1))

        except Exception as e:
            print(f"Error processing row in {csv_file}: {e}")
            continue

    if not system_times:
        print(f"No valid data in {csv_file}")
        return

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

    print(f"Processed {csv_file}")

def process_folder(folder_path):
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Filter out files that already have SVG counterparts
    valid_csv_files = []
    svg_files_CPU = []
    svg_files_GPU = []
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
        if not os.path.exists(svg_file_CPU) or not os.path.exists(svg_file_GPU):
            valid_csv_files.append(csv_file)
            svg_files_CPU.append(svg_file_CPU)
            svg_files_GPU.append(svg_file_GPU)

    if not valid_csv_files:
        print(f"No new CSV files to process in {folder_path}")
        return
    with Pool(processes=min(len(valid_csv_files), os.cpu_count())) as pool:
        zipped_args = zip(valid_csv_files, svg_files_CPU, svg_files_GPU)
        pool.starmap(process_csv_file, zipped_args)

if __name__ == "__main__":
    if os.path.isdir(Input_filePath):
        process_folder(Input_filePath)
    else:
        print("Invalid folder path")
