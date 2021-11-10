import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = 'lesson_3/static/'
print(BASE_DIR)
x=os.path.join(BASE_DIR, STATIC_URL, 'img/img1.jpg')
print(' ')
print(x)

def path_normalize(path):
    path = re.sub(r'[\/\\]', r'\\\\', path)
    print(path)

    return path 

print(path_normalize(x))
