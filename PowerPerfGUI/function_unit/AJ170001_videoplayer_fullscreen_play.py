#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2017 - Allwinner Technology Co., Ltd.

@version: 1.0

@author: moubinmo@allwinnertech.com

@prerequisite:
    based on Python 2.7

@usage:
    通过nose测试框架运行该Case

@Precondition:
    将adb配置到系统环境变量当中    

@description: 
    本地视频全屏循环播放12H

@module: 稳定性测试

@timeout: 432000

"""

import os
import sys
import time

from util import PythonUiautomatorUtil
from uiautomator import Device
from uiautomator import Adb


class AJ170001VideoplayerFullscreenPlay(PythonUiautomatorUtil):

    PRE_INSTALL_APK = []
    PRE_INSTALL_JAR = []
    PRE_INSTALL_RES = [("resource\AWTestVideo1.mkv", "/sdcard/", ""),
                       ("resource\AWTestVideo2.mkv", "/sdcard/", "")]

    self_Device = Device()

    def test(self):
        # 启动Videos
        self.logger.info('========    Step1:     Videos_Run        ========')
        self.uiautomator_dev.press.home()
        self.uiautomator_dev(className=u"android.widget.TextView", description=u'Apps list').click()
        self.uiautomator_dev(text=u"Videos").click()
        time.sleep(3)
        while True:
            self.logger.info("========    Step2: Starting_application        ========")
            # 检测权限弹窗Allow
            while self.check_current_activity("com.google.android.packageinstaller/com.android.packageinstaller.permission.ui.GrantPermissionsActivity"):
                print 'step 11'
                self.uiautomator_dev(
                    resourceId=u"com.android.packageinstaller:id/permission_allow_button", index="2").click()
            # 检测权限弹窗Agree，多次退出进入
            if self.uiautomator_dev(resourceId=u"com.softwinner.fireplayer:id/title", text=u"User agreement").exists:
                self.uiautomator_dev(resourceId=u"com.softwinner.fireplayer:id/positive_button",
                                     text=u"AGREE", index=u'1', clickable=u'true').click()
            # 点击跳过指南
            self.self_Device.click(17, 622)
            # 检测视频存在，进入播放；
            if self.uiautomator_dev(text=u'AWTestVideo1.mkv').exists:
                self.uiautomator_dev(text=u'AWTestVideo1.mkv').click()
                break
            # 视频检测不到重新进入
            else:
                self.uiautomator_dev.press.home()
                self.uiautomator_dev(className=u"android.widget.TextView",
                                     description=u'Apps list').click()
                self.uiautomator_dev(text=u"Videos").click()

        self.logger.info('========    Step3:     4K_Video_Play       ========')
        time.sleep(1)
        # 点击播放设置
        self.uiautomator_dev(
            resourceId=u"com.softwinner.fireplayer:id/setting_bttn", index=u"4").click()
        # 点击全部循环
        self.uiautomator_dev(resourceId=u"android:id/text1", text=u"Repeat all").click()
        self.uiautomator_dev.press.back()
        # 点击全屏和播放
        self.uiautomator_dev(
            resourceId=u"com.softwinner.fireplayer:id/zoom_bttn", index=u"0").click()

        self.logger.info('========    Step4:     Play_12hours_and_TestCaseExit      ========')
        # 循环播放视频12hours，约每100秒检查一次视频是否播放正常
        for i in xrange(720):
            self.check_Video()
            print"It's %d mins of stability test.(totally 720mins)" % i
            time.sleep(60)

        self.logger.info('========    Step5:     Clear_the_Environment     ========')
        self.clean_Environment()

    # 进程检测
    def check_current_activity(self, activity_name):
        ret = Adb().shell('dumpsys activity |grep mFocusedActivity')
        ret = str(ret).strip().replace("\n", "").replace("\r", "")
        self.logger.info("get current activity name: %s" % str(ret))
        if activity_name in str(ret):
            result = True
        else:
            result = False
        return result

    # 播放检测
    def check_Video(self):
        ret = self.device.adb.shell("dumpsys activity | grep Focus")
        ret = str(ret).strip().replace("\n", "").replace("\r", "")
        self.logger.info(ret)
        # 检测当前命令，若Activity被退出则出错并截屏
        if not "com.softwinner.fireplayer/.ui.VideoPlayerActivity" in ret:
            first_screenshot = self.self_Device.screenshot(filename="a.jpg")
            assert False, "the Video apk wasn't in the current page!"

    def clean_Environment(self):
        self.logger.info("tearDown: stopping es")
        self.device.stop_app("com.estrongs.android.pop")
        os.system(
            "adb shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:1\n")
        os.system("adb shell pm clear com.softwinner.fireplayer")
        self.uiautomator_dev.press.home()
