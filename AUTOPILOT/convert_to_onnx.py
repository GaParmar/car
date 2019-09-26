import torch
from networks.pytorch_networks import MobilenetV2Pilot

model =  MobilenetV2Pilot(pretrained_weights=True)
model.load_state_dict(torch.load("./saved_models/EPOCH_10_TESTLOSS_0.1352904737.statedict"))
torch.onnx.export(model, ((torch.randn((20, 3, 320, 240)).cuda(),torch.randn((20, 3, 320, 240)).cuda())), 
    "mobilenetv2.onnx", 
    export_params=True, 
    do_constant_folding=True,
    input_names = ['left', 'right'],
    output_names = ['output'],
    dynamic_axes={'left' : {0 : 'batch_size'}, 'right' : {0 : 'batch_size'}, 'output' : {0 : 'batch_size'}})
