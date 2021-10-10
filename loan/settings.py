from .constant import PRODUCTION, LOCAL, STAGING

env = "local"  # make sure which env you are running on

try:
    if env == LOCAL:
        from .local import *
    elif env == STAGING:
        from .staging import *
    else:
        from .production import *
except:
    print("Error in environment")
