#!/usr/bin/env python
import sys
import time
from vas.vas import Vas

if __name__ == '__main__':
    try:
        assistant = Vas()
        assistant.launch()

        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        sys.exit()
