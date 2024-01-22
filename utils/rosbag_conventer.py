import rospy
from rosbag.bag import Bag
import pandas as pd
import numpy as np
from std_msgs.msg import Header
import sensor_msgs.point_cloud2 as pc2
from scipy.spatial.transform import Rotation

def create_point_cloud_message(points, timestamp):
    header = Header()
    header.stamp = rospy.Time.from_sec(timestamp)
    header.frame_id = 'velodyne_frame'

    return pc2.create_cloud_xyz32(header, points)

def transform_point_cloud(points, odometry_pose):
    translation = odometry_pose[:3]
    rotation = odometry_pose[3:]

    translated_points = points + translation

    rotation_matrix = quaternion_matrix(rotation)[:3, :3]

    rotated_points = np.dot(rotation_matrix, translated_points.T).T

    return rotated_points

def quaternion_matrix(quaternion):
    r = Rotation.from_quat(quaternion)
    return r.as_matrix()

# Read point cloud data from file
point_cloud_data = pd.read_csv('cloud.xyz', header=None)
point_cloud_data.columns = ['x', 'y', 'z', 'timestamp']

# Read odometry data from file
odom_data = pd.read_csv('odom.txt', header=None)
odom_data.columns = ['x', 'y', 'z', 'qx', 'qy', 'qz', 'qw', 'timestamp']

# Create a ROS bag
bag = Bag('my_data_3.bag', 'w')

# Group points by timestamp
grouped_points = point_cloud_data.groupby('timestamp')

# Iterate over unique timestamps
for timestamp, group in grouped_points:
    points = group[['x', 'y', 'z']].values

    odometry_row = odom_data.iloc[(odom_data['timestamp'] - timestamp).abs().idxmin()]
    odometry_pose = np.array([odometry_row['x'], odometry_row['y'], odometry_row['z'],
                              odometry_row['qx'], odometry_row['qy'], odometry_row['qz'], odometry_row['qw']])

    transformed_points = transform_point_cloud(points, odometry_pose)

    pcl_msg = create_point_cloud_message(transformed_points, timestamp)
    bag.write('/velodyne_points', pcl_msg, t=rospy.Time.from_sec(timestamp))

# Close the bag
bag.close()
