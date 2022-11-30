import matplotlib.pyplot as plt
import numpy as np

# set the timestamp as the index and forward fill the data for plotting
sensor_data_clean = sensor_data.set_index('timestamp').astype(float).ffill()
# Edit the indexes just for visualization purposes
indexes = [i.split('T')[0] for i in list(sensor_data_clean.index)]
sensor_data_clean.index = indexes
fig = sensor_data_clean.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('Fahrenheit',fontdict={'fontsize':15})
fig.set_xlabel('time stamp',fontdict={'fontsize':15})
plt.show()