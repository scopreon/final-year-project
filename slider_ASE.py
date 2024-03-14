import numpy as np
from matplotlib.widgets import Slider

# Initial value of dt
dt_init = 0.01

# Placeholder function to simulate the SteeringCircuit and generate points
def simulate_steering_circuit(dt):
    points = []
    for x in range(0, 1000):
        if 300 < x < 500:
            # Simulating an increase when ASE is updated with 1, influenced by dt
            points.append((x * dt, x * dt * 2))  # Example values for illustration
        else:
            # Flat values when ASE is not updated (0), not influenced by dt
            points.append((1, 2))  # Example values for illustration
    return points

# Function to update the plot based on the slider value (dt)
def update(val):
    dt = s_dt.val  # Get the value of dt from the slider
    points = simulate_steering_circuit(dt)  # Generate new points with the updated dt
    ase_0, ase_1 = zip(*points)  # Extract ASE[0] and ASE[1] values
    
    # Update the data for each line
    line_ase_0.set_ydata(ase_0)
    line_ase_1.set_ydata(ase_1)
    fig.canvas.draw_idle()  # Redraw the figure to update the plot

# Initial points generation
points = simulate_steering_circuit(dt_init)
ase_0, ase_1 = zip(*points)
time_series = [x * dt_init for x in range(1000)]

# Creating the plot
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # Make room for the slider
line_ase_0, = plt.plot(time_series, ase_0, label='ASE 0')
line_ase_1, = plt.plot(time_series, ase_1, label='ASE 1')
plt.xlabel('Time (s)')
plt.ylabel('ASE Value')
plt.title('ASE 0 and ASE 1 Over Time')
plt.legend()

# Adding the slider
axcolor = 'lightgoldenrodyellow'
ax_dt = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)  # Slider axis
s_dt = Slider(ax_dt, 'dt', 0.01, 0.1, valinit=dt_init)  # Slider object

s_dt.on_changed(update)  # Call update function when slider value is changed

plt.show()
