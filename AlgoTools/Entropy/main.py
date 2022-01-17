import Shared.data_provider as data_manager
import matplotlib.pyplot as plt

composite = []
composite.points = data_manager.get_data()
composite.pano = data_manager.velo_points_2_pano(composite.points)

plt.subplots(1,1, figsize = (13,3) )
plt.imshow(pano_debth_img)
plt.axis('off')
plt.show()

composite = data_manager.tie_data(data, pano_debth_img)

composite.points = np.ndarray
composite.grid2d = np.ndarray

print(pano_debth_img.shape)
print("done")