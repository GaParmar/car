import torch
from networks.pytorch_networks import MobilenetV2Pilot

model =  MobilenetV2Pilot(pretrained_weights=True)
model.load_state_dict(torch.load("./saved_models/EPOCH_10_TESTLOSS_0.1352904737.statedict", map_location="cpu"))
model.eval()
torch.onnx.export(model, ((torch.randn((1, 3, 320, 240)),torch.randn((1, 3, 320, 240)))), 
    "mobilenetv2.onnx", 
    export_params=True,
    input_names = ['left', 'right'],
    output_names = ['output'])
