import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the random walks
n_steps = 10000 # Number of steps
step_size = 0.01 # Size of each step

# Generate the random walks
np.random.seed(42) # Set the random seed for reproducibility
x = np.arange(n_steps) # Generate the x-values representing the steps
y = np.cumsum(np.random.normal(0, step_size, n_steps)) # Generate the y-values representing the walk
y -= np.min(y) # Shift the walk so that it starts at 0
y /= np.max(y) # Normalize the walk so that it ends at 1
x2 = np.arange(n_steps) # Generate the x-values for the second walk
y2 = np.cumsum(np.random.normal(0, step_size, n_steps)) # Generate the y-values for the second walk
y2 -= np.min(y2) # Shift the walk so that it starts at 0
y2 /= np.max(y2) # Normalize the walk so that it ends at 1

# Set the plot style to XKCD
plt.xkcd()

# Plot the trajectories of the random walks
fig, ax = plt.subplots()
ax.plot(x, y, 'r-', label='Red')
ax.plot(x2, y2, 'b-', label='Blue')
#ax.legend(loc='upper left')
ax.set_xlabel('Generation')
ax.set_ylabel('Frequency')
ax.set_ylim([0, 1])
ax.set_title('Allele Trajectories')

# Add some annotations and a label to the plot
ax.annotate('Population 1', xy=(6000, 0.75), xytext=(8000, 0.9),
            arrowprops=dict(arrowstyle='->'), fontsize=12)
ax.annotate('Population 2', xy=(6000, 0.25), xytext=(8000, 0.1),
            arrowprops=dict(arrowstyle='->'), fontsize=12)
#ax.text(2000, 0.1, '', fontsize=16)

plt.savefig('random_walks.png', dpi=300)

plt.show()
