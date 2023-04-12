import numpy as np
import open3d.visualization.rendering as rendering
import open3d as o3d
import trimesh
import argparse
render = o3d.visualization.rendering.OffscreenRenderer(720, 720)
yellow = rendering.MaterialRecord()
yellow.base_color = [1.0, 1.0, 1.0, 1.0]
yellow.shader = "defaultLit"

def create_o3d_mesh_from_vertices_faces(vertices, faces):
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)
    mesh.vertex_colors = o3d.utility.Vector3dVector([])
    mesh.vertex_normals = o3d.utility.Vector3dVector([])
    mesh.triangle_normals = o3d.utility.Vector3dVector([])
    return mesh

def trimesh2o3d(mesh):
    vertices = mesh.vertices
    face = mesh.faces
    trans_matrix = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    vertices = np.dot(vertices, trans_matrix)
    mesh = create_o3d_mesh_from_vertices_faces(vertices, face)
    return mesh


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_mesh_path', type=str, default='demo.obj')
    parser.add_argument('--render_img_path', type=str, default='demo_open3d.png')
    args = parser.parse_args()

    mesh = trimesh.load(args.input_mesh_path)
    scale = 2 # scale up the mesh for a clear visualization
    mesh.vertices = mesh.vertices * scale
    mesh = trimesh2o3d(mesh)
    render.scene.add_geometry(f"mesh", mesh, yellow)
    render.scene.set_background([0, 0, 0, 0])
    render.setup_camera(70.0, [0, 0, 0], [3, 2, 5], [0, 1, 0])
    render.scene.scene.set_sun_light([0.707, 0.0, -.707], [1.0, 1.0, 1.0],
                                     75000)
    render.scene.scene.enable_sun_light(True)
    render.scene.show_axes(True)
    img = render.render_to_image()
    o3d.io.write_image(args.render_img_path, img, 9)
    render.scene.remove_geometry('mesh')