from matplotlib import pyplot as plt

x_values = list(range(1, 1001))
y_value = [x ** 2 for x in x_values]
plt.scatter(x_values, y_value, s=40, c=y_value, cmap=plt.cm.Blues, edgecolors='none')
plt.axis([0, 1100, 0, 1100000])
plt.show()
