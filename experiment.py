import numpy as np
import matplotlib.pyplot as plt

energy = [10, 15, 20, 25, 30]
current = [4, 5, 4.98, 5.02, 5]
collection = [0.22, 1.61, 2.16, 2.67, 3.03]

input_power = [a * b for a, b in zip(energy, current)]
output_power = [a * 1.8 for a in collection]
print(input_power)
print(output_power)

eff = [a * 100 / b for a, b in zip(output_power, input_power)]
print(eff)

plt.plot(energy, eff, linestyle='-')
plt.title("Efficiency of solar panel at different energy levels")
plt.xlabel("Energy (keV)")
plt.ylabel("Efficiency (%)")
plt.show()
