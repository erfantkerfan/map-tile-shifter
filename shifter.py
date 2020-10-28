import logging
import os

from pick import pick

logging.basicConfig(level=logging.WARNING, filename='log.log', filemode='w',
                    format='%(levelname)s - %(message)s')

VERSION = '0.1.0'


# get initialising values from user via console
def config():
    global zoom_shift, column_shift, row_shift

    # zoom_options = [i for i in range(0, 11)]
    # title = 'Please your zoom shift level:'
    # zoom_shift, index = pick(zoom_options, title)
    zoom_shift = 3

    column_options = [5] + [i for i in range(0, 8)]
    title = 'Please choose your column shift:'
    column_shift, index = pick(column_options, title)

    row_options = [1] + [i for i in range(0, 5)]
    title = 'Please choose your row shift:'
    row_shift, index = pick(row_options, title)


def start():
    global zoom_shift, column_shift, row_shift

    for zoom in range(0, MAX_ZOOM + 1):
        for column in range(0, 2 ** zoom):
            for row in range(0, 2 ** zoom):
                src_path = os.path.join(SRC_DIR, str(zoom), str(column), str(row)) + '.png'
                dst_path = os.path.join(DST_DIR, str(zoom + zoom_shift), str(column + column_shift),
                                        str(row + row_shift) + '.png')
                if not os.path.exists(src_path):
                    logging.error('source file not found ' + src_path)
                else:
                    if not os.path.exists(dst_path):
                        logging.error('destination file not found ' + dst_path)
                    else:
                        try:
                            print('dish ', end='')
                            # shutil.move(src_path, dst_path)
                        except:
                            logging.error('moving encountered error' + src_path + ' to ' + dst_path)

        print(10 * '*')


if __name__ == '__main__':
    SRC_DIR = 'map t'
    DST_DIR = 'silkroadmap'
    MAX_ZOOM = 7  # in the src_map

    config()
    start()
