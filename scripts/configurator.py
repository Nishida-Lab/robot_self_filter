#!/usr/bin/env python

import rospy
import re


class RobotSelfFilterConfigurator(object):
    def __init__(self, namespace="/self_filter"):
        if namespace[0] is "/":
            self.namespace_ = namespace
        else:
            self.namespace_ = "/" + namespace

        self.semantic_param_name_ = rospy.get_param("~semantic_param_name", "/robot_description_semantic")
        self.min_sensor_dist_ = rospy.get_param("~min_sensor_dist", 0.2)
        self.self_see_default_padding_ = rospy.get_param("~self_see_default_padding", 0.1)
        self.self_see_default_scale_ = rospy.get_param("~self_see_default_scale", 1.0)
        self.keep_organized_ = rospy.get_param("~keep_organized", True)
        self.subsample_value_ = rospy.get_param("~subsample_value", 0.0)
        self.use_rgb_ = rospy.get_param("~use_rgb", False)
        self.robot_description_semantic_ = rospy.get_param(self.semantic_param_name_)

    def get_linkname_list_(self):
        pre_pattern = "(.*)link\ name=(.*)"
        post_pattern = "(?<=\").*?(?=\")"

        linkname_list = re.findall(post_pattern, "\n".join(map(str, re.findall(pre_pattern, self.robot_description_semantic_))))

        return linkname_list

    def configure(self):
        linkname_list = self.get_linkname_list_()
        if not linkname_list:
            rospy.logerr("links not found")
            return

        linkname_param_format = []
        for linkname in linkname_list:
            linkname_param_format.append({"name": linkname})

        rospy.set_param(self.namespace_ + "/min_sensor_dist", self.min_sensor_dist_)
        rospy.set_param(self.namespace_ + "/self_see_default_padding", self.self_see_default_padding_)
        rospy.set_param(self.namespace_ + "/self_see_default_scale_", self.self_see_default_scale_)
        rospy.set_param(self.namespace_ + "/keep_organized", self.keep_organized_)
        rospy.set_param(self.namespace_ + "/subsample_value", self.subsample_value_)
        rospy.set_param(self.namespace_ + "/use_rgb", self.use_rgb_)
        rospy.set_param(self.namespace_ + "/self_see_links", linkname_param_format)
        rospy.loginfo("configure for robot_self_filter is completed")


if __name__ == "__main__":
    rospy.init_node("robot_self_filter_configurator")
    configurator = RobotSelfFilterConfigurator()
    configurator.configure()

