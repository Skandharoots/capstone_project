# 1) Read note at line - 74 !!!
# 2) Replace WHOLE __init__ and _update_geometries funcitons inside KISS-ICP's visualizer.py file.



def __init__(self):
    try:
        self.o3d = importlib.import_module("open3d")
    except ModuleNotFoundError as err:
        print(f'open3d is not installed on your system, run "pip install open3d"')
        exit(1)

    # Initialize GUI controls
    self.block_vis = True
    self.play_crun = False
    self.reset_bounding_box = True

    # Create data
    self.source = self.o3d.geometry.PointCloud()
    self.keypoints = self.o3d.geometry.PointCloud()
    self.target = self.o3d.geometry.PointCloud()
    self.frames = []

    # Initialize visualizer
    self.vis = self.o3d.visualization.VisualizerWithKeyCallback()
    self._register_key_callbacks()
    self._initialize_visualizer()

    # Visualization options
    self.render_map = True
    self.render_source = True
    self.render_keypoints = False
    self.global_view = False
    self.render_trajectory = True
    # Cache the state of the visualizer
    self.state = (
        self.render_map,
        self.render_keypoints,
        self.render_source,
    )

    gizmo_size = 1.0
    self.gizmo_at_origin = self.o3d.geometry.TriangleMesh.create_coordinate_frame(size=gizmo_size, origin=[0, 0, 0])
    self.vis.add_geometry(self.gizmo_at_origin)
        
def _update_geometries(self, source, keypoints, target, pose):
    # Source hot frame
    if self.render_source:
        self.source.points = self.o3d.utility.Vector3dVector(source)
        self.source.paint_uniform_color(YELLOW)
        if self.global_view:
            self.source.transform(pose)
    else:
        self.source.points = self.o3d.utility.Vector3dVector()

    # Keypoints
    if self.render_keypoints:
        self.keypoints.points = self.o3d.utility.Vector3dVector(keypoints)
        self.keypoints.paint_uniform_color(YELLOW)
        if self.global_view:
            self.keypoints.transform(pose)
    else:
        self.keypoints.points = self.o3d.utility.Vector3dVector()

    # Target Map
    if self.render_map:
        target = copy.deepcopy(target)
        self.target.points = self.o3d.utility.Vector3dVector(target)
        if not self.global_view:
            self.target.transform(np.linalg.inv(pose))
    else:
        self.target.points = self.o3d.utility.Vector3dVector()

    # Note(Fortuna) - ADDED PART - just works :)
    # Here I've placed CUSTOM modification to how the trajectory looks like   
    # Basicaly, we enhance the trajectory visualization by introducing a moving gizmo representing
    # the position and orientation of the robot at each frame. This includes a line connecting the origin
    # to the gizmo, a yellow sphere indicating the current robot position, and additional information
    # such as the distance from the origin and coordinates of the moving gizmo.
    gizmo_size = 1.0
    moving_gizmo = self.o3d.geometry.TriangleMesh.create_coordinate_frame(size=gizmo_size, origin=[0, 0, 0])
    moving_gizmo.transform(pose)
    self.frames.append(moving_gizmo)

    for frame in self.frames[:-3]:
        self.vis.remove_geometry(frame, reset_bounding_box=False)

    line_points = np.vstack([np.zeros(3), np.asarray(moving_gizmo.vertices[0])])
    line = self.o3d.geometry.LineSet(points=self.o3d.utility.Vector3dVector(line_points),
                                        lines=self.o3d.utility.Vector2iVector([[0, 1]]))
    line.paint_uniform_color([0, 1, 0])
    self.vis.add_geometry(line, reset_bounding_box=False)
    self.frames.append(line)

    sphere_size = 0.2
    sphere = self.o3d.geometry.TriangleMesh.create_sphere(sphere_size)
    sphere.compute_vertex_normals()
    sphere.paint_uniform_color([1, 1, 0])
    sphere.transform(pose)
    self.vis.add_geometry(sphere, reset_bounding_box=False)
    self.frames.append(sphere)

    distance = np.linalg.norm(np.array(self.gizmo_at_origin.get_center()) - np.array(moving_gizmo.get_center()))
    distance_str = str(distance)

    print(f"Distance from origin: {distance_str}")
    print(f"Coordinates of the moving gizmo: {moving_gizmo.get_center()}")

    if self.render_trajectory and self.global_view:
        self.vis.add_geometry(self.frames[-3], reset_bounding_box=False)

    self.vis.update_geometry(self.keypoints)
    self.vis.update_geometry(self.source)
    self.vis.update_geometry(self.target)

    if len(self.frames) > 4:
        self.vis.remove_geometry(self.frames[-4], reset_bounding_box=False)  # Line
        self.vis.remove_geometry(self.frames[-5], reset_bounding_box=False)

    if self.reset_bounding_box:
        self.vis.reset_view_point(True)
        self.reset_bounding_box = False
