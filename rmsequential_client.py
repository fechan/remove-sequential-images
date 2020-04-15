import os
from rmsequential import rmsequential

try:
    os.environ['PKG_CONFIG_PATH']
except KeyError:
    os.environ['PKG_CONFIG_PATH'] = "/usr/lib/imagemagick6/pkgconfig"

TARGET_DIRECTORY = "./test"
IMAGEMAGICK_COMPARE_FUZZINESS = .50

rmsequential(TARGET_DIRECTORY, IMAGEMAGICK_COMPARE_FUZZINESS)