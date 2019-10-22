robot_self_filter [![Build Status](https://api.travis-ci.com/Nishida-Lab/robot_self_filter.svg?branch=kinetic-devel)](https://travis-ci.com/Nishida-Lab/robot_self_filter)
=====================================================================================================================================================

# Usage
```
$ roslaunch robot_self_filter robot_self_filter.launch
```

# Parameters
Some parameters defined at [config/robot_self_filter.yaml](config/robot_self_filter.yaml)
- min_sensor_dist (default: 0.2)
  - minimum sensor distance [m]
- self_see_default_padding (default: 0.1)
  - self removal filter padding [m]
- self_see_default_scale (default: 1.0)
- keep_organized (default: true)
- subsample_value (default: 0.0)
- **[optional]** see_link_names
  - if not set, it will set see link names which defined at URDF
- **[optional]** ignore_link_names
  - specify link names to ignore filtering
