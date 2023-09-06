import matplotlib
import matplotlib.pyplot as plt
import numpy as np

print(matplotlib.__version__)

# xpoints = np.array([0, 6])
# ypoints = np.array([0, 100])
# plt.plot(xpoints, ypoints)
# plt.show()

figure, axes = plt.subplots()
draw_circle = plt.Circle((0.5, 0.5), 0.3, fill=False,color='#11a300')

axes.set_aspect(1)
axes.add_artist(draw_circle)
plt.title('Circle')
plt.show()