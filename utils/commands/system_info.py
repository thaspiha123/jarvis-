import platform
import psutil


def get_cpu_usage():
    return f"CPU usage is {psutil.cpu_percent(interval=0.5)} percent."


def get_ram_usage():
    memory = psutil.virtual_memory()
    return f"RAM usage is {memory.percent} percent."


def get_system_information():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    return (
        f"You are using {platform.system()} {platform.release()}. "
        f"CPU usage is {cpu} percent and RAM usage is {memory.percent} percent."
    )
