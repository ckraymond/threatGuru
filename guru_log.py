import logging

LOG_NAME = './gurulog.txt'

logging.basicConfig(filename = LOG_NAME, encoding='utf-8',
                    filemode = 'w',format='%(asctime)s-%(levelname)s-%(message)s')
gurulog = logging.getLogger()
gurulog.setLevel(logging.DEBUG)