import os
from .base import *

if os.environ.get('MODE') == 'prod':
   from .prod import *
   print('prod')
else:
   from .dev import *
   print('dev')
   o