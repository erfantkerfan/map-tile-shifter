import logging
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from threading import Thread

from dotenv import load_dotenv
from pick import pick
from tqdm import tqdm

logging.basicConfig(level=logging.WARNING, filename='log.log', filemode='w', format='%(levelname)s - %(message)s')

VERSION = '1.1.1'
SIMULTANEOUS_THREADS = 50


# get initialising values from user via console
def config():
    global zoom_shift, column_shift, row_shift

    # zoom_options = [i for i in range(0, 11)]
    # title = 'Please your zoom shift level:'
    # zoom_shift, index = pick(zoom_options, title)
    zoom_shift = 3

    column_options = [i for i in range(0, 8)]
    title = 'Please choose your column shift:'
    column_shift, index = pick(column_options, title)

    row_options = [i for i in range(0, 5)]
    title = 'Please choose your row shift:'
    row_shift, index = pick(row_options, title)


def shift():
    global zoom_shift, column_shift, row_shift
    errors = 0
    threads = []
    for zoom in range(0, MAX_ZOOM + 1):
        bar = tqdm(total=2 ** zoom, desc='zoom ' + str(zoom), unit='pic')
        for column in range(0, 2 ** zoom):
            for row in range(0, 2 ** zoom):
                src_path = os.path.join(SRC_DIR, str(zoom), str(column), str(row)) + '.png'
                dst_path = os.path.join(DST_DIR, str(zoom + zoom_shift), str(column + (2 ** zoom) * column_shift),
                                        str(row + (2 ** zoom) * row_shift) + '.png')
                if not os.path.exists(src_path):
                    logging.error('source file not found ' + src_path)
                    errors += 1
                else:
                    if not os.path.exists(dst_path):
                        logging.error('destination file not found ' + dst_path)
                        errors += 1
                    else:
                        try:
                            # throttle the conversion parallel processes
                            while threading.activeCount() > SIMULTANEOUS_THREADS:
                                pass
                            threads = [t for t in threads if t.is_alive()]
                            name = 't: ' + ' - '.join([str(zoom), str(column), str(row)])
                            threads.append(Thread(name=name, target=execute,
                                                  args=(src_path, dst_path)))
                            threads[-1].start()
                        except:
                            logging.error(
                                'moving and deleting webp-image encountered error' + src_path + ' to ' + dst_path)
                            errors += 1
            bar.update(1)
            # stay here until all threads are finished
            while any([t.is_alive for t in threads]):
                threads = [t for t in threads if t.is_alive()]
        bar.close()
    logging.error('total errors: ' + str(errors))


def execute(src, dst):
    shutil.move(src, dst)
    if PRODUCTION:
        os.remove(dst + '.webp')


def clear_cache():
    os.system('php /home/alaa/alaatv/artisan alaaTv:abrishamMapVersion:generate')
    os.system('php /home/alaa/alaatv/artisan config:clear')
    os.system('php /home/alaa/alaatv/artisan config:cache')
    os.system('sudo service php7.3-fpm restart')


# update the code with github
def update():
    command = 'git fetch --all'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    status = process.wait()

    if status == 0:
        update_text = tk.StringVar()
        update_text.set('✔')
        update_label = tk.Label(root, textvariable=update_text, fg='green')
        update_label.pack(pady=5)
        command = 'git reset --hard ' + GIT_REMOTE + '/' + GIT_BRANCH
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        status = process.wait()
        if status == 0:
            update_text.set('✔ ✔')
            command = 'pip install -r requirements.txt'
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
            status = process.wait()
            if status == 0:
                update_text.set('✔ ✔ ✔')
                reload(updated=True)


# show update progress bar
def waiting():
    global root

    def progress():
        while progress:
            if progress_bar['value'] > 100:
                progress_bar['value'] = 0
            progress_bar['value'] += 1
            time.sleep(0.01)

    root = tk.Tk()
    root.geometry("250x150")
    root.resizable(height=None, width=None)
    root.iconbitmap(default=os.path.join(os.getcwd(), 'alaa.ico'))
    # root.protocol('WM_DELETE_WINDOW', root.iconify)
    root.title('Alaa QR-code app')
    update_title = tk.Label(root, text='در حال بروزرسانی از اینترنت')
    update_title.pack(pady=20)
    progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=10)
    t = threading.Thread(target=progress)
    progress = 1
    t.start()
    root.mainloop()


# reload the app with needed sys arguments
def reload(updated=False):
    if updated:
        os.execv(sys.executable, ['python ' + str(__file__) + ' updated'])
    else:
        os.execv(sys.executable, ['python ' + str(__file__)])


if __name__ == '__main__':
    # set up initial variables
    PRODUCTION = platform.system() != 'Windows'
    MAX_ZOOM = 7  # in the src_map
    load_dotenv()
    DEBUG = bool(os.getenv("DEBUG"))
    GIT_REMOTE = 'production'
    GIT_BRANCH = 'master'

    if PRODUCTION:
        SRC_DIR = '/alaa_media/cdn/upload/pom'
        DST_DIR = '/alaa_media/cdn/upload/raheAbrishamMap'
    else:
        import tkinter as tk
        import tkinter.ttk as ttk

        SRC_DIR = 'pom'
        DST_DIR = 'map'

    asci_shahb_hi = '''
 __    __  __         ______   __                  __                  __       
|  \  |  \|  \       /      \ |  \                |  \                |  \      
| $$  | $$ \$$      |  $$$$$$\| $$____    ______  | $$____    ______  | $$____  
| $$__| $$|  \      | $$___\$$| $$    \  |      \ | $$    \  |      \ | $$    \ 
| $$    $$| $$       \$$    \ | $$$$$$$\  \$$$$$$\| $$$$$$$\  \$$$$$$\| $$$$$$$\\
| $$$$$$$$| $$       _\$$$$$$\| $$  | $$ /      $$| $$  | $$ /      $$| $$  | $$
| $$  | $$| $$      |  \__| $$| $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$| $$__/ $$
| $$  | $$| $$       \$$    $$| $$  | $$ \$$    $$| $$  | $$ \$$    $$| $$    $$
 \$$   \$$ \$$        \$$$$$$  \$$   \$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$$$$$$ 
    '''
    asci_shahb_bye = '''
 _______                              ______   __                  __                  __       
|       \                            /      \ |  \                |  \                |  \      
| $$$$$$$\ __    __   ______        |  $$$$$$\| $$____    ______  | $$____    ______  | $$____  
| $$__/ $$|  \  |  \ /      \       | $$___\$$| $$    \  |      \ | $$    \  |      \ | $$    \ 
| $$    $$| $$  | $$|  $$$$$$\       \$$    \ | $$$$$$$\  \$$$$$$\| $$$$$$$\  \$$$$$$\| $$$$$$$\\
| $$$$$$$\| $$  | $$| $$    $$       _\$$$$$$\| $$  | $$ /      $$| $$  | $$ /      $$| $$  | $$
| $$__/ $$| $$__/ $$| $$$$$$$$      |  \__| $$| $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$| $$__/ $$
| $$    $$ \$$    $$ \$$     \       \$$    $$| $$  | $$ \$$    $$| $$  | $$ \$$    $$| $$    $$
 \$$$$$$$  _\$$$$$$$  \$$$$$$$        \$$$$$$  \$$   \$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$$$$$$ 
          |  \__| $$                                                                            
           \$$    $$                                                                            
            \$$$$$$                                                                             
    '''

    # answer if is update needed?
    if DEBUG or PRODUCTION or (len(sys.argv) > 1 and sys.argv[1] == 'updated'):
        config()
        print(asci_shahb_hi)
        shift()
        print(asci_shahb_bye)
        input("Press ENTER key to exit . . .")
    else:
        tt = threading.Thread(target=waiting)
        tt.start()
        update()
        root.quit()
        os._exit(0)
