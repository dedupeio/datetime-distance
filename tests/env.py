import sys
import os

# Append module root directory to sys.path so that we can run tests
# without installing the module
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
