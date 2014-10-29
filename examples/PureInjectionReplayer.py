#
# Copyright 2014 Mingyuan Xia (http://mxia.me) and others
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contributors:
#   Mingyuan Xia
#

"""
This script demonstrates how to replay a trace to a Android device. You need
monkeyrunner to run scripts once including this module
"""

import os
import sys
import inspect


def module_path():
    ''' returns the module path without the use of __file__.
    from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(os.path.dirname(inspect.getsourcefile(module_path)))


sys.path.append(module_path())
sys.path.append(os.path.join(module_path(), '..', 'src'))

from Pipeline import Pipeline
from TroubleMaker import TroubleInjector, TroubleReplayer
from EventGenerator import EventGenerator
import DeviceManager as dm


def main():
    print "Replay started"
    pl = Pipeline()
    pl.addStep(EventGenerator(interval=3000,number=1000))
    pl.addStep(TroubleInjector())
    dev = dm.getDevice()
    pl.addStep(TroubleReplayer(dev))
    pl.execute()
    print "Replay finished"


if __name__ == "__main__":
    main()
