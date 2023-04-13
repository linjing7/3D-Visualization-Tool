# Render offscreen -- make sure to set the PyOpenGL platform
import os
import cv2
os.environ["PYOPENGL_PLATFORM"] = "egl"
import numpy as np
import trimesh
import pyrender

# Load the FUZE bottle trimesh and put it in a scene
mesh = trimesh.load('demo.obj')
material = pyrender.MetallicRoughnessMaterial(metallicFactor=0.0, alphaMode='OPAQUE',
                                                  baseColorFactor=(1.0, 1.0, 0.9, 1.0))
mesh = pyrender.Mesh.from_trimesh(mesh, material=material, smooth=False)
# mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
scene = pyrender.Scene(ambient_light=(0.3, 0.3, 0.3))
scene.add(mesh, 'mesh')

# Set up the camera -- z-axis away from the scene, x-axis right, y-axis up
focal, princpt = [8885.424931844076, 8885.424733161926], [864.7579956054688, 465.5693054199219]
camera = pyrender.IntrinsicsCamera(fx=focal[0], fy=focal[1], cx=princpt[0], cy=princpt[1])
scene.add(camera)

# camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
# s = np.sqrt(2)/2
# camera_pose = np.array([
#        [0.0, -s,   s,   0.3],
#        [1.0,  0.0, 0.0, 0.0],
#        [0.0,  s,   s,   0.35],
#        [0.0,  0.0, 0.0, 1.0],
#     ])
# scene.add(camera, pose=camera_pose)

# Set up the light -- a single spot light in the same spot as the camera
# light = pyrender.SpotLight(color=np.ones(3), intensity=3.0,
#                                innerConeAngle=np.pi/16.0)
# scene.add(light, pose=camera_pose)



# Render the scene
renderer = pyrender.OffscreenRenderer(viewport_width=640, viewport_height=480, point_size=1.0)
light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=0.8)
light_pose = np.eye(4)
light_pose[:3, 3] = np.array([0, -1, 1])
scene.add(light, pose=light_pose)
light_pose[:3, 3] = np.array([0, 1, 1])
scene.add(light, pose=light_pose)
light_pose[:3, 3] = np.array([1, 1, 2])
scene.add(light, pose=light_pose)

# renderer = pyrender.OffscreenRenderer(640, 480)
rgb, depth = renderer.render(scene, flags=pyrender.RenderFlags.RGBA)
rgb = rgb[:, :, :3].astype(np.float32)

valid_mask = (depth > 0)[:, :, None]
img = np.zeros((480, 640, 3))
img = rgb * valid_mask + img * (1 - valid_mask)
cv2.imwrite('demo_pyrender.png', img)