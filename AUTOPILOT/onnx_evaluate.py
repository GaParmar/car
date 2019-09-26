import onnxruntime
import numpy as np

ort_session = onnxruntime.InferenceSession("mobilenetv2.onnx")

left = np.random.uniform(size = (1, 3, 320, 240)).astype(np.float32)
right = np.random.uniform(size = (1, 3, 320, 240)).astype(np.float32)

# compute ONNX Runtime output prediction
ort_inputs = {"left": left, "right": right}
ort_outs = ort_session.run(None, ort_inputs)
print(ort_outs)