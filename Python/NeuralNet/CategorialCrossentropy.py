import math

softmax_output = [0.7, 0.1, 0.2]

target_outpuut = [1, 0, 0]

loss = -(math.log(softmax_output[0]) * target_outpuut[0] +
         math.log(softmax_output[1]) * target_outpuut[1] +
         math.log(softmax_output[2]) * target_outpuut[2])

print(loss)