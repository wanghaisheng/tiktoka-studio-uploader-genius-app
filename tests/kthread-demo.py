import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import time
import cv2
import psutil
import time
import kthread

model = YOLO('yolov8n.pt')

def load_model():
    print("Loading model...")
    try:
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            print("No file selected.")

        results = model.predict(file_path, device='cpu', show=True)
        print("Done")
    except Exception as e:
        print("Error:", str(e))
        raise


def get_latest_process():
    latest_time = 0
    latest_process = None

    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        if proc.info['name'] == process_name:
            start_time = proc.info['create_time']
            if start_time > latest_time:
                latest_time = start_time
                latest_process = proc

    return latest_process

def get_running_processes():
    running_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            running_processes.append(proc)

    return running_processes
def get_own_process_name():
    current_process = psutil.Process()
    return current_process.name()

def check_and_close_latest_process():
    while True:
        time.sleep(0.1)
        running_processes = get_running_processes()
        if len(running_processes) >= 2:
            latest_process = get_latest_process()

            if latest_process:
                try:
                    print(f"Closing latest process: {latest_process.info['name']} (PID: {latest_process.info['pid']})")
                    latest_process.terminate()
                except psutil.NoSuchProcess:
                    pass
                except psutil.AccessDenied:
                    print(
                        f"Access denied to terminate process: {latest_process.info['name']} (PID: {latest_process.info['pid']})")
                except Exception as e:
                    print(
                        f"Error occurred while terminating process: {latest_process.info['name']} (PID: {latest_process.info['pid']}): {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("YOLO Model GUI")
    root.geometry('200x100')
    btn_load_model = tk.Button(root, text="Load Model and Predict", command=load_model)
    btn_load_model.pack(pady=20)
    process_name = get_own_process_name()
    thread = kthread.KThread(target=check_and_close_latest_process)
    thread.start()
    root.mainloop()