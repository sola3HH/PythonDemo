import matplotlib.pyplot as plt

"""
画一条线
input_value = [1, 2, 3, 4, 5]
squares = [1, 4, 9, 16, 25]
plt.plot(input_value, squares, linewidth=5)
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)
plt.tick_params(axis='both', labelsize=14)
plt.show()
"""

x_values = [1, 2, 3, 4, 5]
y_value = [1, 4, 9, 16, 25]
plt.scatter(x_values, y_value, s=100)
plt.show()
