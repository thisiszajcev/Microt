import os
import sys
import requests
import zipfile
import tkinter as tk
from tkinter import ttk
from ping3 import ping
import threading
import time
from datetime import datetime

# Ссылки на файл с информацией о версии и файл обновления
VERSION_INFO_URL = "https://drive.google.com/file/d/130Hd6OT4d0fMu8Ollugz3dOd9R_1omZi/view?usp=sharing"
APP_DIR = os.path.dirname(os.path.abspath(__file__))

__version__ = "1.2"

def get_current_version():
    return __version__

def get_latest_version_info():
    response = requests.get(VERSION_INFO_URL)
    version_info = response.json()
    return version_info

def download_update(url, dest):
    response = requests.get(url, stream=True)
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def install_update(update_file):
    with zipfile.ZipFile(update_file, 'r') as zip_ref:
        zip_ref.extractall(APP_DIR)

def update_program(root):
    current_version = get_current_version()
    root.title(f"Статус доступности контейнеров v{current_version} - проверка обновлений...")

    try:
        version_info = get_latest_version_info()
        latest_version = version_info["version"]
        update_url = version_info["url"]

        if latest_version > current_version:
            root.title(f"Статус доступности контейнеров v{current_version} - загрузка обновлений...")
            update_file = os.path.join(APP_DIR, "update.zip")
            download_update(update_url, update_file)

            root.title(f"Статус доступности контейнеров v{current_version} - установка обновлений...")
            install_update(update_file)
            os.remove(update_file)

            # Перезапуск программы
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            root.title(f"Статус доступности контейнеров v{current_version}")
    except Exception as e:
        root.title(f"Статус доступности контейнеров v{current_version} - последняя версия")

# Инициализация GUI
root = tk.Tk()
current_version = get_current_version()
root.title(f"Статус доступности контейнеров v{current_version}")

# Запуск обновления перед основной логикой программы
update_thread = threading.Thread(target=update_program, args=(root,))
update_thread.start()

# Далее следует основной код программы...

# Данные для проверки
sosnovoborsk_mikrotiks = [
    {'name': 'Контейнер 401', 'ip': '10.8.121.28'},
    {'name': 'Контейнер 402', 'ip': '10.8.121.29'},
    {'name': 'Контейнер 403', 'ip': '10.8.121.30'},
    {'name': 'Контейнер 404', 'ip': '10.8.121.31'},
    {'name': 'Контейнер 405', 'ip': '10.8.121.32'},
    {'name': 'Контейнер 406', 'ip': '10.8.121.33'},
    {'name': 'Контейнер 407', 'ip': '10.8.121.34'},
    {'name': 'Контейнер 408', 'ip': '10.8.121.35'},
    {'name': 'Контейнер 409', 'ip': '10.8.121.36'},
    {'name': 'Контейнер 410', 'ip': '10.8.121.37'},
    {'name': 'Контейнер 411', 'ip': '10.8.121.38'},
    {'name': 'Контейнер 412', 'ip': '10.8.121.39'},
    {'name': 'Контейнер 413', 'ip': '10.8.121.40'},
    {'name': 'Контейнер 414', 'ip': '10.8.121.41'},
    {'name': 'Контейнер 415', 'ip': '10.8.121.42'},
    {'name': 'Контейнер 416', 'ip': '10.8.121.43'},
]

gres_mikrotiks = [
    {'name': 'Контейнер 601', 'ip': '10.8.121.2'},
    {'name': 'Контейнер 602', 'ip': '10.8.121.5'},
    {'name': 'Контейнер 603', 'ip': '10.8.121.6'},
    {'name': 'Контейнер 604', 'ip': '10.8.121.7'},
    {'name': 'Контейнер 605', 'ip': '10.8.121.23'},
    {'name': 'Контейнер 606', 'ip': '10.8.121.24'},
    {'name': 'Контейнер 607', 'ip': '10.8.121.21'},
    {'name': 'Контейнер 608', 'ip': '10.8.121.20'},
    {'name': 'Контейнер 609', 'ip': '10.8.121.9'},
    {'name': 'Контейнер 610', 'ip': '10.8.121.8'},
    {'name': 'Контейнер 612', 'ip': '10.8.121.3'},
]

irkutsk_mikrotiks = [
    {'name': 'Контейнер 201', 'ip': '10.8.121.44'},
    {'name': 'Контейнер 202', 'ip': '10.8.121.44'},
    {'name': 'Контейнер 203', 'ip': '10.8.121.45'},
    {'name': 'Контейнер 204', 'ip': '10.8.121.45'},
    {'name': 'Контейнер 205', 'ip': '10.8.121.46'},
    {'name': 'Контейнер 206', 'ip': '10.8.121.46'},
    {'name': 'Контейнер 207', 'ip': '10.8.121.48'},
    {'name': 'Контейнер 208', 'ip': '10.8.121.48'},
    {'name': 'Контейнер 209', 'ip': '10.8.121.52'},
    {'name': 'Контейнер 210', 'ip': 'nodata'},
]

podolsk_mikrotiks = [
    {'name': 'Контейнер 2201', 'ip': '10.8.121.27'},
]


# Класс для хранения состояния и времени последнего успешного пинга
class ContainerState:
    def __init__(self):
        self.last_seen = {}

# Функция для выполнения пинга и обновления результатов для конкретного региона
def ping_and_update_results(container_list, treeview, container_state):
    while True:
        treeview.delete(*treeview.get_children())
        
        containers_online = 0
        containers_offline = 0
        
        for container in container_list:
            ip = container['ip']
            result = ping(ip)
            now = datetime.now().strftime("%d.%m.%Y %H:%M")
            
            if result is not None:
                status = "Доступен"
                status_color = "black"
                containers_online += 1
                container_state.last_seen[ip] = now
            else:
                status = "Недоступен"
                status_color = "red"
                containers_offline += 1
            
            last_seen_time = container_state.last_seen.get(ip, "Нет данных")
            treeview.insert("", "end", values=(container['name'], ip, status, last_seen_time), tags=(status,))
            treeview.tag_configure(status, foreground=status_color)
        
        time.sleep(30)  # каждые полминуты

# Создание GUI с использованием Tkinter
notebook = ttk.Notebook(root)

# Создание вкладок для каждого региона
sosnovoborsk_frame = ttk.Frame(notebook)
gres_frame = ttk.Frame(notebook)
irkutsk_frame = ttk.Frame(notebook)
podolsk_frame = ttk.Frame(notebook)

notebook.add(sosnovoborsk_frame, text='Сосновоборск')
notebook.add(gres_frame, text='Грэс')
notebook.add(irkutsk_frame, text='Иркутск')
notebook.add(podolsk_frame, text='Подольск')
notebook.pack(expand=True, fill='both')

# Создание и настройка виджета Treeview для каждого региона
columns = ('Контейнер', 'IP', 'Статус', 'Last seen')

treeview_sosnovoborsk = ttk.Treeview(sosnovoborsk_frame, columns=columns, show='headings')
treeview_sosnovoborsk.heading('Контейнер', text='Контейнер')
treeview_sosnovoborsk.heading('IP', text='IP')
treeview_sosnovoborsk.heading('Статус', text='Статус')
treeview_sosnovoborsk.heading('Last seen', text='Последняя активность')
treeview_sosnovoborsk.pack(pady=10, expand=True, fill='both')

treeview_gres = ttk.Treeview(gres_frame, columns=columns, show='headings')
treeview_gres.heading('Контейнер', text='Контейнер')
treeview_gres.heading('IP', text='IP')
treeview_gres.heading('Статус', text='Статус')
treeview_gres.heading('Last seen', text='Последняя активность')
treeview_gres.pack(pady=10, expand=True, fill='both')

treeview_irkutsk = ttk.Treeview(irkutsk_frame, columns=columns, show='headings')
treeview_irkutsk.heading('Контейнер', text='Контейнер')
treeview_irkutsk.heading('IP', text='IP')
treeview_irkutsk.heading('Статус', text='Статус')
treeview_irkutsk.heading('Last seen', text='Последняя активность')
treeview_irkutsk.pack(pady=10, expand=True, fill='both')

treeview_podolsk = ttk.Treeview(podolsk_frame, columns=columns, show='headings')
treeview_podolsk.heading('Контейнер', text='Контейнер')
treeview_podolsk.heading('IP', text='IP')
treeview_podolsk.heading('Статус', text='Статус')
treeview_podolsk.heading('Last seen', text='Последняя активность')
treeview_podolsk.pack(pady=10, expand=True, fill='both')

# Создание экземпляра класса ContainerState для хранения состояния
container_state = ContainerState()

# Запуск проверки доступности микротиков в отдельном потоке для каждого региона
threading.Thread(target=ping_and_update_results, args=(sosnovoborsk_mikrotiks, treeview_sosnovoborsk, container_state)).start()
threading.Thread(target=ping_and_update_results, args=(gres_mikrotiks, treeview_gres, container_state)).start()
threading.Thread(target=ping_and_update_results, args=(irkutsk_mikrotiks, treeview_irkutsk, container_state)).start()
threading.Thread(target=ping_and_update_results, args=(podolsk_mikrotiks, treeview_podolsk, container_state)).start()

root.iconbitmap('C:/microt.ico')
root.mainloop()
