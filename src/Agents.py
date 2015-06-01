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
#   Xinye Lin
#   Ran Shu
#
import re


class CellularAgent:

    def __init__(self, device):
        self.device = device

    def turnOnCellularData(self):
        """ Turn on cellular data service (need root access)
        """
        try:
            self.device.shell('su')
            self.device.shell('svc data enable')
            return True
        except:
            print("Failed to turn on the cellular data.")
            return False

    def turnOffCellularData(self):
        """ Turn off cellular data service (need root access)
        """
        try:
            self.device.shell('su')
            self.device.shell('svc data disable')
            return True
        except:
            print("Failed to turn off the cellular data.")
            return False

    def getCellularDataStatus(self):
        """ Report the current data service status
        Return True when the data service is on
        """
        sysAgent = SystemStatusAgent(self.device)
        return sysAgent.getCellularDataStatus() == '2'

    def toggleCellularDataStatus(self):
        if self.getCellularDataStatus():
            self.turnOffCellularData()
        else:
            self.turnOnCellularData()


class LogcatAgent:
    MAIN = 'main'
    EVENTS = 'events'
    RADIO = 'radio'
    """ LogcatAgent controls logcat, the logging facility of Android"""

    def __init__(self, device):
        """ Initialize the agent with a given device
        @param device: should be an EMonkeyDevice
        """
        self.device = device

    def logcat(self, args):
        """ Send a raw logcat command and return its output"""
        s = "logcat"
        for arg in args:
            s += ' ' + arg
        return self.device.shell(s).encode('utf-8')

    def clear(self):
        """ Clear the logcat logs"""
        self.logcat(['-c'])

    def dumpBuf(self, buf=MAIN):
        return self.logcat(['-b ', buf])

    def dump(self, fmt=None, filterTuples=[]):
        """ Dump the logcat logs with given filters and formats
        @param fmt: the output format
        @param filterTuples: a list of (TAG,LEVEL) tuples that specify filtering
        according to Android doc, LEVEL could be:
        V - Verbose (lowest priority)
        D - Debug
        I - Info
        W - Warning
        E - Error
        F - Fatal
        S - Silent (highest priority, on which nothing is ever printed)
        """
        cmd = ['-d']
        if fmt is not None:
            cmd.append('-v')
            cmd.append(fmt)
        for tp in filterTuples:
            cmd.append('%s:%s' % tp)
        return self.logcat(cmd)


class ScreenAgent:

    def __init__(self, device):
        self.device = device
        self.METHOD_CHANGE_ORIENTATION = r'testChangeOrientation'
        self.METHOD_CHANGE_RIGHT_DOWN = r'testChangeRightDown'
        self.METHOD_CHANGE_LEFT_DOWN = r'testChangeLeftDown'
        self.METHOD_FREEZE_ROTATION = r'testFreezeRotation'
        self.METHOD_UNFREEZE_ROTATION = r'testUnfreezeRotation'
        self.METHOD_TOGGLE_SCREEN = r'testToggleScreen'

    def getScreenRotationStatus(self):
        sysAgent = SystemStatusAgent(self.device)
        return sysAgent.getScreenRotationStatus()

    def getOrientation(self):
        sysAgent = SystemStatusAgent(self.device)
        return sysAgent.getOrientation()

    def changeOrientation(self):
        sysAgent = SystemStatusAgent(self.device)
        current = sysAgent.getOrientation()
        sysAgent.testAndroidJarMethod(self.METHOD_CHANGE_ORIENTATION)
        newStatus = sysAgent.getOrientation()
        if current != newStatus:
            return True
        else:
            return False

    def changeRightDown(self):
        sysAgent = SystemStatusAgent(self.device)
        current = sysAgent.getOrientation()
        sysAgent.testAndroidJarMethod(self.METHOD_CHANGE_RIGHT_DOWN)
        newStatus = sysAgent.getOrientation()
        if current != newStatus:
            return True
        else:
            return False

    def changeLeftDown(self):
        sysAgent = SystemStatusAgent(self.device)
        current = sysAgent.getOrientation()
        sysAgent.testAndroidJarMethod(self.METHOD_CHANGE_LEFT_DOWN)
        newStatus = sysAgent.getOrientation()
        if current != newStatus:
            return True
        else:
            return False

    def freezeRotation(self):
        sysAgent = SystemStatusAgent(self.device)
        sysAgent.testAndroidJarMethod(self.METHOD_FREEZE_ROTATION)
        return sysAgent.getScreenRotationStatus() == 1

    def unfreezeRotation(self):
        sysAgent = SystemStatusAgent(self.device)
        sysAgent.testAndroidJarMethod(self.METHOD_UNFREEZE_ROTATION)
        return sysAgent.getScreenRotationStatus() == 0

    def toggleScreen(self):
        sysAgent = SystemStatusAgent(self.device)
        current = sysAgent.getScreenOnOffStatus()
        sysAgent.testAndroidJarMethod(self.METHOD_TOGGLE_SCREEN)
        return sysAgent.getScreenOnOffStatus() == current


class SnapshotAgent:

    def __init__(self, device):
        self.device = device

    def takeSnapshot(self):
        ''' Return a snapshot object
        '''
        return self.device.takeSnapshot()

    def saveSnapshot(self, snapshot, fileName):
        ''' Save a snapshot object to a png file
        '''
        snapshot.writeToFile(fileName, 'png')

    def compareSnapshots(self, snapshot1, snapshot2):
        ''' Check if two snapshot objects are the same
        '''
        return snapshot1.sameAs(snapshot2, 1)

    def takeAndCompareSnapshots(self, snapshotCheck):
        ''' Take a snapshot and check if it is the same as another one
        '''
        return self.compareSnapshots(self.takeSnapshot(), snapshotCheck)

    def getSubSnapshot(self, snapshot, coordinates):
        ''' Get a region from a snapshort
        '''
        return snapshot.getSubImage(coordinates)

    def loadSnapshot(self, fileName):
        ''' Load a snapshot object from a png file
        '''
        return self.device.loadImageFromFile(fileName)


class KeypressAgent:

    def __init__(self, device):
        self.device = device
        self.METHOD_PRESS_BACK = r'testPressBack'
        self.METHOD_PRESS_HOME = r'testPressHome'
        self.METHOD_CLICK_XY = r'testClick'
        self.METHOD_DRAG = r'testDrag'

    def pressBack(self):
        sysAgent = SystemStatusAgent(self.device)
        sysAgent.testAndroidJarMethod(self.METHOD_PRESS_BACK)

    def pressHome(self):
        sysAgent = SystemStatusAgent(self.device)
        sysAgent.testAndroidJarMethod(self.METHOD_PRESS_HOME)

    def clickXY(self, x, y):
        sysAgent = SystemStatusAgent(self.device)
        sysAgent.testAndroidJarMethod(
            self.METHOD_CLICK_XY + ' -e x ' + str(x) + ' -e y ' + str(y))

    def drag(self, startX, startY, endX, endY, steps):
        sysAgent = SystemStatusAgent(self.device)
        sysAgent.testAndroidJarMethod(self.METHOD_DRAG + ' -e startX ' + str(startX) + ' -e startY ' + str(
            startY) + ' -e endX ' + str(endX) + ' -e endY ' + str(endY) + ' -e steps ' + str(steps))


class WifiAgent:

    def __init__(self, device):
        self.device = device

    def turnOnWifi(self):
        """ Need root access
        """
        try:
            self.device.shell('su')
            self.device.shell('svc wifi enable')
            return True
        except:
            print("Failed to turn on the Wifi.")
            return False

    def turnOffWifi(self):
        """ Need root access
        """
        try:
            self.device.shell('su')
            self.device.shell('svc wifi disable')
            return True
        except:
            print("Failed to turn off the Wifi.")
            return False

    def getWiFiStatus(self):
        sysAgent = SystemStatusAgent(self.device)
        return sysAgent.getWifiStatus()

    def changeWifiStatus(self):
        status = self.getWiFiStatus()
        if status == 'enabled':
            return self.turnOffWifi()
        elif status == 'disabled':
            return self.turnOnWifi()
        else:
            print("Wifi status unchangable for now.")
            return False


class SystemStatusAgent:

    def __init__(self, device):
        self.device = device
        self.SCRIPT_PATH = r'/sdcard/'
        self.TEST_JAR = r'AndroidTest.jar'
        self.TEST_PACKAGE = r'edu.mcgill.lynxiayel.androidtest'
        self.TEST_CLASS = r'AndroidTest'
        self.UIAUTOMATOR_TEST_PREFIX = 'uiautomator runtest ' + self.SCRIPT_PATH + \
            self.TEST_JAR + ' -c ' + self.TEST_PACKAGE + \
            '.' + self.TEST_CLASS + '#'

    def getWifiStatus(self):
        """Possible status:
           disabled | connected | enabled | disconnected
        """
        msg = self.device.shell("dumpsys wifi").encode('utf-8')
        pat = re.compile(r'^Wi-Fi is (\w*)')
        try:
            status = pat.findall(msg)[0]
            if status != "":
                return status
            else:
                raise Exception()
        except Exception:
            print("Fail to acquire WiFi status!")
            return False

    def getCellularDataStatus(self):
        """Possible status:
            0 - DATA_DISCONNECTED (Disconnected. IP traffic not available. )
            1 - DATA_CONNECTING(Currently setting up a data connection.)
            2 - DATA_CONNECTED (Connected. IP traffic should be available.)
            3 - DATA_SUSPENDED (Suspended. The connection is up, but IP traffic is temporarily unavailable.
                For example, in a 2G network, data activity may be suspended when a voice call arrives.)
        """
        msg = self.device.shell('dumpsys telephony.registry').encode('utf-8')
        pat = re.compile(r'mDataConnectionState=([0-3])')
        try:
            status = pat.findall(msg)[0]
            if status in ['0', '1', '2', '3']:
                return status
            else:
                raise Exception()
        except Exception:
            print("Fail to acquire Cellular data connection status!")
            return False

    def getScreenRotationStatus(self):
        """Possible status
           1 - Rotation locked
           0 - Auto Rotation
        """
        msg = self.device.shell('dumpsys window').encode('utf-8')
        pat = re.compile(r'mUserRotationMode=([01])')
        try:
            status = pat.findall(msg)[0]
            if status in ['0', '1']:
                return status
            else:
                raise Exception()
        except Exception:
            print("Fail to acquire screen rotation status!")
            return False

    def getScreenOnOffStatus(self):
        """Possible status
           True - On
           False - Off
        """
        msg = self.device.shell('dumpsys power').encode('utf-8')
        pat = re.compile(r'mScreenOn=(true|false)')
        try:
            status = pat.findall(msg)[0]
            if status in ['true', 'false']:
                return status == 'true'
            else:
                raise Exception()
        except Exception:
            print("Fail to acquire screen On/Off status!")

    def getOrientation(self):
        """Possible status:
           0 - portrait
           1 - landscape (left side down)
           2 - portrait (upside down)
           3 - landscape (right side down)
        """
        msg = self.device.shell('dumpsys display').encode('utf-8')
        pat = re.compile(r'mCurrentOrientation=([0-3])')
        try:
            status = pat.findall(msg)[0]
            if status in ['0', '1', '2', '3']:
                return status
            else:
                raise Exception()
        except Exception:
            print("Fail to acquire screen orientation!")
            return False

    def getBatteryLevel(self):
        """return the remaining percentage of battery
        """
        msg = self.device.shell('dumpsys battery').encode('utf-8')
        pat = re.compile(r'level: (\d*)')
        try:
            status = pat.findall(msg)[0]
            if 0 <= int(status) <= 100:
                return status
            else:
                raise Exception()
        except Exception:
            print("Fail to acquire the battery level!")
            return False

    def hasFile(self, fileName):
        try:
            if not fileName:
                raise ValueError('File name is empty!')
            msg = self.device.shell(
                'ls ' + self.SCRIPT_PATH + fileName).encode('utf-8')
            fileName = re.escape(fileName)
            pat = re.compile(r'(' + fileName + r')')
            result = pat.findall(msg)[0]
            if result:
                return True
            else:
                return False
        except Exception, e:
            if isinstance(e, ValueError):
                print(e.message)
            else:
                print("Checking file existence failed!")
            return False

    def hasTestScript(self):
        return self.hasFile(self.TEST_JAR)

    def pushTestScript(self):
        return self.pushFile(self.TEST_JAR)

    def prepareScript(self):
        if not self.hasTestScript():
            self.pushTestScript()
        else:
            pass

    def testAndroidJarMethod(self, methodName):
        self.prepareScript()
        self.device.shell(
            self.UIAUTOMATOR_TEST_PREFIX + methodName).encode('utf-8')

# TODO need to fx pushFile and PullFile in first
    def pushFile(self, fileName):
        return self.device.pushFile(self.SCRIPT_PATH + fileName)
