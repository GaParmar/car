import sys
import os
import pdb

import numpy as np
import torch
import torch.nn as nn
from torch.utils.model_zoo import load_url as load_state_dict_from_url

from pytorch_mobilenet import MobileNetV2

weights_url = 'https://download.pytorch.org/models/mobilenet_v2-b0353104.pth'

class MobilenetV2Pilot(nn.Module):
    def __init__(self, pretrained_weights=True, input_shape=(6, 320, 240)):
        super(MobilenetV2Pilot, self).__init__()
        self.backbone = MobileNetV2(image_channels=6, num_classes=2, width_mult=1.0)
        if pretrained_weights:
            state_dict = load_state_dict_from_url(weights_url, progress=True)
            # delete first layer and classification layers at end
            for key in state_dict:
                if "features.0.0" in key or "classifier.1" in key:
                    del state_dict[key]
            self.backbone.load_state_dict(state_dict, strict=False)
        self.sigmoid = torch.sigmoid

    def forward(self, left, right):
        x = torch.cat((left, right), 1)
        x = self.backbone(x)
        x = self.sigmoid(x)
        return x
