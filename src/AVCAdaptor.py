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

from adb.adbclient import AdbClient

class AVCDevice:
    """ To control an AndroidViewClient-based device
    """
    DOWN_AND_UP = AdbClient.DOWN_AND_UP
    DOWN = AdbClient.DOWN
    UP = AdbClient.UP
    # MOVE = AdbClient.MOVE

    def __init__(self, timeout = 5):
        self.dev = AdbClient()
        self.displayWidth = int(self.getProperty("display.width"))
        self.displayHeight = int(self.getProperty("display.height"))

    def broadcastIntent(self, uri, action, data, mimetype, extras, component, flags):
        # self.dev.broadcastIntent(uri, action, data, mimetype, extras, component, flags)
        raise Exception('Unimplemented')

    def drag(self, start, end, duration, steps):
        self.dev.drag(start, end, duration, steps)
        return self

    def getProperty(self, key):
        return self.dev.getProperty(key)

    def getSystemProperty(self, key):
        return self.dev.getSystemProperty(key)

    def installPackage(self, path):
        #self.dev.installPackage(path)
        raise Exception('Unimplemented')

    def instrument(self, className, args):
        #return self.dev.instrument(className, args)
        raise Exception('Unimplemented')

    def loadImageFromFile(self, fileName):
        #return MonkeyRunner.loadImageFromFile(fileName)
        raise Exception('Unimplemented')

    def press(self, name, t=DOWN_AND_UP):
        self.dev.press(name, t)
        return self

    def reboot(self, into="None"):
        #self.dev.reboot(into)
        raise Exception('Unimplemented')

    def rebootBootloader(self):
        #self.dev.reboot("bootloader")
        raise Exception('Unimplemented')

    def rebootRecovery(self):
        #self.dev.reboot("Recovery")
        raise Exception('Unimplemented')

    def removePackage(self, package):
        #self.dev.removePackage(package)
        raise Exception('Unimplemented')

    def shell(self, cmd):
        r = self.dev.shell(cmd)
        if r is None:
            r = ""
        return r.encode('utf-8')

    def startActivity(self, uri=None, action=None, data=None,
                      mimetype=None, categories=[], extras={},
                      component=None, flags=0):
        #self.dev.startActivity(uri, action, data, mimetype, categories,
        #                       extras, component, flags)
        raise Exception('Unimplemented')

    def takeSnapshot(self):
        return self.dev.takeSnapshot()

    def touch(self, x, y, t=DOWN_AND_UP):
        self.dev.touch(x, y, t)
        return self

    def type(self, message):
        self.dev.type(message)
        return self

    def wake(self):
        self.dev.wake()
        return self

    def slideLeft(self):
        h = self.displayHeight / 2
        w1 = self.displayWidth * 7 / 8
        w2 = self.displayHeight * 1 / 8
        self.dev.drag((w1, h), (w2, h), 0.01, 100)
        return self

    def slideRight(self):
        h = self.displayHeight / 2
        w1 = self.displayWidth * 1 / 8
        w2 = self.displayHeight * 7 / 8
        self.dev.drag((w1, h), (w2, h), 0.01, 100)
        return self

    def unlockScreen(self):
        self.unlock()
        return self

    def sleep(self, seconds):
        time.sleep(seconds)
        return self

    def getInstalledPackage(self):
        raw = str(self.shell("pm list packages"))
        l = []
        for line in raw.split('\n'):
            if line.startswith("package:"):
                l.append(line.replace("package:", "").rstrip())
        return l

    def killAllBgApps(self):
        self.shell("am kill-all")

    def pushFile(self, path):
        #return self.shell("push " + path)
        raise Exception('Unimplemented')

    def pullFile(self, devicePath, localPath):
        #return self.shell("pull %s %s" % (devicePath, localPath))
        raise Exception('Unimplemented')

    def getSystemInfo(self):
        return {"android_version": self.getProperty("build.version.release")}
