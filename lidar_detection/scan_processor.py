import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
import numpy as np

from .clustering import cluster_points
from .tracking import Tracker
from .zones import classify_zone


class ScanProcessor(Node):

    def __init__(self):
        super().__init__('scan_processor')

        # Subscribe to LiDAR
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Publisher for markers (both spheres + text)
        self.marker_pub = self.create_publisher(Marker, '/visualization_marker', 10)

        self.tracker = Tracker()

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        angles = np.linspace(msg.angle_min, msg.angle_max, len(ranges))

        points = []

        # Convert polar → Cartesian
        for r, a in zip(ranges, angles):
            if np.isfinite(r):
                x = r * np.cos(a)
                y = r * np.sin(a)
                points.append([x, y])

        if len(points) == 0:
            return

        points = np.array(points)

        # Clustering
        clusters = cluster_points(points)

        # Tracking
        tracked_objects = self.tracker.update(clusters)

        # Process each object
        for obj in tracked_objects:
            pos = obj['position']

            if len(pos) < 2:
                continue

            dist = np.linalg.norm(pos)
            zone = classify_zone(dist)

            # Publish sphere
            self.publish_marker(pos, obj['id'], zone)

            # Publish text (ID + distance)
            self.publish_text(pos, obj['id'], dist, zone)

            # Log
            self.get_logger().info(
                f"ID {obj['id']} | Dist: {dist:.2f} | Vel: {obj['velocity']:.2f} | Zone: {zone}"
            )

    # 🟢 Sphere marker
    def publish_marker(self, pos, obj_id, zone):
        marker = Marker()

        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "objects"
        marker.id = obj_id

        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        marker.pose.position.x = float(pos[0])
        marker.pose.position.y = float(pos[1])
        marker.pose.position.z = 0.0

        marker.scale.x = 0.25
        marker.scale.y = 0.25
        marker.scale.z = 0.25

        # Color based on zone
        if zone == "DANGER":
            marker.color.r = 1.0
            marker.color.g = 0.0
        elif zone == "WARNING":
            marker.color.r = 1.0
            marker.color.g = 1.0
        else:
            marker.color.r = 0.0
            marker.color.g = 1.0

        marker.color.b = 0.0
        marker.color.a = 1.0

        self.marker_pub.publish(marker)

    # 🟡 Text marker (ID + distance)
    def publish_text(self, pos, obj_id, dist, zone):
        marker = Marker()

        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "labels"
        marker.id = obj_id + 1000   # avoid ID conflict

        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        # Position above object
        marker.pose.position.x = float(pos[0])
        marker.pose.position.y = float(pos[1])
        marker.pose.position.z = 0.5

        marker.scale.z = 0.3

        # White text
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0

        marker.text = f"ID {obj_id}\n{dist:.2f}m\n{zone}"

        self.marker_pub.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = ScanProcessor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
