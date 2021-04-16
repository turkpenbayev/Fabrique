import os
from .base import *

if os.environ.get('MODE') == 'prod':
   from .prod import *
elif os.environ.get('MODE') == 'heroku':
   from .heroku import *
else:
   from .dev import *