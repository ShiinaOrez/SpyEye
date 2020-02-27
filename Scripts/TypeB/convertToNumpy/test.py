import numpy as np

position = np.dtype([('x', np.int16), ('y', np.int16)])
report = np.dtype([('time', np.float16), ('is_btn', 'b'), ('pos', position), ('width', np.int16)])

track = np.array([(0.222, False, (1, 1,), 8,), (0.222, False, (1, 1,), 8,)], dtype=report)
collection = np.array([track, track])

print(collection)

np.save('demo', collection)

def save_as_np(store):
    
