#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_devices/license/LICENSE
#
#################################################################################

# sys
import threading
import subprocess

# ros
import rospy
from rocon_device_msgs.msg import HueState, Hue, HueArray

# phue
from rocon_python_hue import Bridge
from rocon_python_hue import PhueRegistrationException, PhueException


class RoconBridge():
    MAX_HUE = 65535
    MAX_SAT = 255
    MAX_BRI = 255

    def __init__(self, hue_ip='127.0.0.1'):
        self.name = 'ros_hue'
        self.ip = hue_ip
        self.bridge = Bridge()
        self.bridge.set_ip_address(self.ip)
        self.hue_list_publisher = rospy.Publisher('list_hue', HueArray, latch=True, queue_size=10)

        rospy.Subscriber('set_hue', Hue, self.set_hue)

        self.checker_th = threading.Thread(target=self.hue_checker)
        self.is_checking = True
        self.retry_cnt = 0
        self.retry_max_cnt = 5
        self.checker_th.start()
        self.string2color = {}
        self.hues = None

        self._init_color_lookup_table()

    def _init_color_lookup_table(self):
        hue_angle = lambda angle: self.MAX_HUE * angle / 360

        self.string2color['OFF'] = (0, 0, 0, False)
        self.string2color['WHITE'] = (hue_angle(0), 0, self.MAX_BRI, True)
        self.string2color['RED'] = (hue_angle(360), self.MAX_SAT, self.MAX_BRI, True)
        self.string2color['GREEN'] = (hue_angle(140), self.MAX_SAT, self.MAX_BRI, True)
        self.string2color['BLUE'] = (hue_angle(260), self.MAX_SAT, self.MAX_BRI, True)
        self.string2color['YELLOW'] = (hue_angle(130), self.MAX_SAT, self.MAX_BRI, True)
        self.string2color['ORANGE'] = (hue_angle(70), self.MAX_SAT, self.MAX_BRI, True)
        self.string2color['MAGENTA'] = (hue_angle(307), self.MAX_SAT, self.MAX_BRI, True)
        self.string2color['VIOLET'] = (hue_angle(280), self.MAX_SAT, self.MAX_BRI, True)

    def hue_checker(self):
        while self.is_checking and not rospy.is_shutdown():
            if self.ping_checker():
                if not self.bridge.is_connect:
                    try:
                        self.bridge.connect()
                    except PhueRegistrationException as e:
                        self.logwarn_ex(e.message)
                    except PhueException as e:
                        self.logwarn_ex(e.message)
                    else:
                        self.loginfo('bridge connect')
                        self.retry_cnt = 0
                        self.bridge.is_connect = True
                else:
                    self.bulb_checker()
            else:
                self.bridge.is_connect = False
                if self.retry_cnt < self.retry_max_cnt:
                    self.retry_cnt += 1
                elif self.retry_cnt == self.retry_max_cnt:
                    self.retry_cnt += 1
                    self.loginfo('No more display log regarding retrying to connect to bridge')
                self.loginfo_ex('bridge not connect %s' % self.ip)
            rospy.sleep(5)

    def ping_checker(self):
        response = subprocess.call(['ping', '-c', '1', self.ip], stdout=subprocess.PIPE,)
        if response == 0:
            return True
        else:
            return False

    def bulb_checker(self):
        try:
            light_ids = self.bridge.get_light_objects(mode='id')
            hues = HueArray()
            for light_id in light_ids:
                state = self.bridge.get_light(light_id)
                if not state:
                    continue
                elif state is not '':
                    hue = Hue()
                    hue.light_id = light_id
                    hue.name = state['name']
                    hue.state.on = state['state']['on']
                    hue.state.hue = state['state']['hue']
                    hue.state.sat = state['state']['sat']
                    hue.state.bri = state['state']['bri']
                    hue.state.reachable = state['state']['reachable']
                    hues.hue_list.append(hue)
            self.hues = hues
        except Exception, e:
            self.logwarn_ex('failed. Reason:%s' % str(e))
        else:
            self.hue_list_publisher.publish(self.hues)

    def set_hue(self, data):
        self.loginfo(str(data.light_id) + ': ' + str(data.state.color))
        if self.bridge.is_connect:
            state = self.bridge.get_light(data.light_id)
            if data.state.color:
                (h, s, v, on) = self.get_color_from_string(data.state.color)
                if not state['state']['on']:
                    state['on'] = on
                state['on'] = on
                state['hue'] = h
                state['sat'] = s
                state['bri'] = v
            else:
                if not state['state']['on']:
                    state['on'] = on
                if data.state.hue:
                    state['on'] = True
                    state['hue'] = data.state.hue
                if data.state.sat:
                    state['on'] = True
                    state['sat'] = data.state.sat
                if data.state.bri:
                    state['on'] = True
                    state['bri'] = data.state.bri
            self.bridge.set_light([data.light_id], state)

    def get_color_from_string(self, color):
        try:
            return self.string2color[color]
        except KeyError as e:
            self.loginfo('Unsupported Color! Set it to WHITE')
            return self.string2color['WHITE']

    def loginfo(self, msg):
        rospy.loginfo('Rocon Hue : ' + str(msg))

    def logwarn(self, msg):
        rospy.logwarn('Rocon Hue : ' + str(msg))

    def loginfo_ex(self, msg):
        if self.retry_cnt < self.retry_max_cnt:
            rospy.loginfo('Rocon Hue : ' + str(msg))

    def logwarn_ex(self, msg):
        if self.retry_cnt < self.retry_max_cnt:
            rospy.logwarn('Rocon Hue : ' + str(msg))

    def spin(self):
        if self.ip is not None:
            while not rospy.is_shutdown():
                try:
                    rospy.sleep(0.1)
                except:
                    break
            self.is_checking = False
            self.checker_th.join(1)
        else:
            self.logwarn('Must set hue ip')
