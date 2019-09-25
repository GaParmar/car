from torchvision import transforms, utils

def transform_sample(sample):
    image_transform = transforms.Compose([
                            transforms.Resize((320,240)),
                            transforms.ToTensor(),
                            transforms.Normalize(mean=(0,0,0), std=(1,1,1))
                        ])
    # crop and apply transform
    sample["image_left"] = image_transform(sample["image"].crop((0,0,320,240)))
    sample["image_right"] = image_transform(sample["image"].crop((320,0,640,240)))
    # throttle from [90, 105] to [0,1]
    sample["throttle"] -= 90.0
    sample["throttle"] /= 15.0
    # steer from [60,120] to [0,1]
    sample["steer"] -= 60.0
    sample["steer"] /= 60.0
    del sample["image"]
    return sample