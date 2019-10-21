#!/usr/bin/env python
import rospy
from urdf_parser_py.urdf import URDF

class RobotSelfFilterConfigurator(object):
    def __init__(self, namespace="/self_filter"):
        if namespace[0] is "/":
            self.namespace_ = namespace
        else:
            self.namespace_ = "/" + namespace

        self.semantic_param_name_ = rospy.get_param(
            "~semantic_param_name", "/robot_description_semantic")
        self.min_sensor_dist_ = rospy.get_param("~min_sensor_dist", 0.2)
        self.self_see_default_padding_ = rospy.get_param(
            "~self_see_default_padding", 0.1)
        self.self_see_default_scale_ = rospy.get_param(
            "~self_see_default_scale", 1.0)
        self.keep_organized_ = rospy.get_param("~keep_organized", True)
        self.subsample_value_ = rospy.get_param("~subsample_value", 0.0)
        self.use_rgb_ = rospy.get_param("~use_rgb", False)
        self.robot_description_semantic_ = rospy.get_param(
            self.semantic_param_name_)

    def get_linkname_list_(self):
        robot = URDF.from_parameter_server();
        linkname_list = []
        for link in robot.links:
            link_name = link.name
            rospy.loginfo("%s is included in the robot description.", link_name)
            linkname_list.append({"name": link_name})
        return linkname_list

    def link_configure_(self):
        see_linkname_list = self.get_linkname_list_()

        if not see_linkname_list:
            rospy.logerr("links not found")
        
        self_see_links = rospy.get_param("~see_link_names", see_linkname_list)

        see_list = [i.values() for i in see_linkname_list]
        for link in self_see_links:
            if link.values() not in see_list:
                rospy.logerr("%s is not included in urdf.", link.values())

        ignore_linkname_list = []
        self_ignore_links = rospy.get_param("~ignore_link_names", ignore_linkname_list)
        ignore_list = [i.values() for i in self_ignore_links]
        
        target_links = [i for i in self_see_links if i.values() not in ignore_list]
        return target_links

    def configure(self):
        target_linkname_list = self.link_configure_()
        if not target_linkname_list:
            rospy.logerr("links not found")
            return

        rospy.set_param(self.namespace_ + "/min_sensor_dist",
                        self.min_sensor_dist_)
        rospy.set_param(self.namespace_ + "/self_see_default_padding",
                        self.self_see_default_padding_)
        rospy.set_param(self.namespace_ + "/self_see_default_scale_",
                        self.self_see_default_scale_)
        rospy.set_param(self.namespace_ + "/keep_organized",
                        self.keep_organized_)
        rospy.set_param(self.namespace_ + "/subsample_value",
                        self.subsample_value_)
        rospy.set_param(self.namespace_ + "/use_rgb", self.use_rgb_)
        rospy.set_param(self.namespace_ + "/self_see_links",
                        target_linkname_list)
        rospy.loginfo("configure for robot_self_filter is completed")


if __name__ == "__main__":
    rospy.init_node("robot_self_filter_configurator")
    configurator = RobotSelfFilterConfigurator()
    configurator.configure()
