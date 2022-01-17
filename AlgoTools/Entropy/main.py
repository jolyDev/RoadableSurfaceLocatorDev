import Shared.data_provider as data_manager
import matplotlib.pyplot as plt

composite = data_manager.get_composite()
entropy_estimator = data_manager.entropy_calculator(composite)
composite.entropy = entropy_estimator.calc_entropy(lambda first, second: abs(first[0]**2) + abs(first[1] ** 2) + abs(first[2] ** 2))

plt.subplots(1,1, figsize = (13,3) )
plt.imshow(composite.entropy)
plt.axis('off')
plt.show()
print("done")