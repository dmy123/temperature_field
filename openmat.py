
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt

# dataFile = '/tmp/pycharm_project_128/data/temperature_data.mat'
# data = scio.loadmat(dataFile)
# print(data.keys())
# print(type(data))
# print(data['temperature_field_data'])
# print(data['temperature_field_data'].shape)

# for example in range(0,240,241):
#     pred_output = data['temperature_field_data'][example]
#     for time in range(0,1920,500):
#         pred_output_slice = pred_output[:, :, time]
#         plt.imshow(pred_output_slice)
#         plt.axis('on')
#         plt.xlabel("example_"+str(example)+" predict_time_"+str(time))
#         plt.show()

dataFile = 'pred/temperature_field_eval.mat'
data = scio.loadmat(dataFile)
print(data.keys())
print(type(data))
#print(data['temperature_field_data'])
print('pred.shape:',data['pred'].shape,',u.shape:',data['u'].shape)
for example in range(0,20,21):
    pred_output = data['pred'][example]
    u_output = data['u'][example]
    for time in range(0, 960, 100):
        # pred_output_slice = (pred_output[:,:,time]).astype(np.int)
        pred_output_slice = pred_output[:, :, time]
        u_output_slice = u_output[:, :, time]
        plt.imshow(pred_output_slice)
        plt.axis('on')
        plt.xlabel("example_" + str(example) + " predict_time_" + str(time))
        plt.show()
        plt.imshow(u_output_slice)
        plt.axis('on')
        plt.xlabel("example_" + str(example) + " u_time_" + str(time))
        plt.show()