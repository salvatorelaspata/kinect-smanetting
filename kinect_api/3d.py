import api
import open3d as o3d

# Ottieni i dati in metri
depth_meters = api.get_depth_in_meters()

# Crea la nuvola di punti
pcd = o3d.geometry.PointCloud()
points = []
fx, fy = 525, 525  # Focal length (da calibrazione)
cx, cy = 319.5, 239.5  # Optical center

for v in range(depth_meters.shape[0]):
    for u in range(depth_meters.shape[1]):
        Z = depth_meters[v, u]
        if Z <= 0 or Z > 5:  # Filtra valori non validi
            continue
        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy
        points.append([X, Y, Z])

pcd.points = o3d.utility.Vector3dVector(points)
o3d.io.write_point_cloud("object_3d.ply", pcd)
