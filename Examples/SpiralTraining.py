# Author: Colin Pollard
# Date: 10/30/2020
# Example for creating trajectories using the toolbox.
from Core.PointGeneration import circleSet, compression
from Core.Exporting import exportToCSV
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

xList, yList, zList = circleSet(0.04, 0.04, 0.001, 4, 4)
exportToCSV("Circle Set", xList, yList, zList)
print("Points Generated: " + str(len(xList)))
xList, yList, zList = compression(0.04, 0.02, 0.001)
exportToCSV("Test Set", xList, yList, zList)
print("Points Generated: " + str(len(xList)))

# Plot values
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xList, yList, zList)
plt.show()
# Export to CSV