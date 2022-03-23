
import pickle
import numpy as np
import logging
import torch
from torchvision import models
from torchvision import transforms
import numpy as np
np.random.seed(0)
torch.manual_seed(0)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(0)
import torch.backends.cudnn as cudnn
from fastapi import UploadFile
from PIL import Image
import io
from scipy import stats

    
class IQAModel(object):

    def __init__(self, cnn_path, svr_path, scaler_path):
        self.cnn_path = cnn_path
        self.svr_path = svr_path
        self.scaler_path = scaler_path
        self._load_local_model()

    def _load_local_model(self):
        self.cnn = FeatureMode(self.cnn_path)
        with open(self.svr_path, "rb") as f:
            self.svr = pickle.load(f)
        with open(self.scaler_path, "rb") as f:
            self.scaler = pickle.load(f)
    
    def _pre_process(self, file_name):#: UploadFile):
        logging.debug(f"Pre-processing payload... {file_name}")
        with open(file_name, "rb") as f:
            payload = f.read()
    
        img = np.array(Image.open(io.BytesIO(payload)))
        print("TYPE ", type(payload), type(img), img.shape)
 
        normalize = get_imagenet_normalize()
        img_transform = transforms.Compose([transforms.ToTensor(), normalize])

        crop_w = 224
        crop_h = 224
        img_h, img_w, channels = img.shape
        crop_num_w = 5
        crop_num_h = 5

        crop_imgs = np.array([])
        crop_box = get_crop_box(img_w, img_h, crop_w, crop_h, crop_num_w, crop_num_h)
        for box in crop_box:
            w, h, w2, h2 = box
            w = int(w)
            h = int(h)
            w2 = int(w2)
            h2 = int(h2)
            part = img[h:h2, w:w2]
            crop_imgs = np.append(crop_imgs, img_transform(part))
        crop_imgs = crop_imgs.reshape(crop_num_w * crop_num_h, 3, 224, 224)
        crop_imgs = torch.from_numpy(crop_imgs).float() # (25, 3, 224, 224)
        return crop_imgs

    def _post_process(self, prediction):
        # return self.scaler.transform(np.array(prediction).reshape(-1,1))
        percentile = stats.percentileofscore(self.scaler, prediction)
        return percentile
    
    def predict(self, file_name):#: UploadFile):
        crop_imgs = self._pre_process(file_name)
        crop_out = self.cnn.extract_feature(crop_imgs) # (25, 4096)
        crop_out = np.average(crop_out, axis=0) # average of 25 patches (1, 4096)
        crop_out = crop_out.reshape(-1, 4096)
        logging.info(f"X shape: {crop_out.shape}")
        prediction = self.svr.predict(crop_out) # (25,)
        print('test score:', np.mean(prediction))
        prediction = self._post_process(prediction)
        print(prediction) # [[-1.40337523]]
        return prediction #.item()
    
    
def get_imagenet_normalize():
    return transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

def get_pretrained_model(model_name):
    print("=> using pre-trained model '{}'".format(model_name))
    if model_name == "alexnet": # TODO: try resnet, inception
        model = models.alexnet(pretrained = True)
        mod = list(model.classifier.children())
        mod.pop() # remove 1000-class last layer
        mod.append(torch.nn.Linear(4096, 5))
        new_classifier = torch.nn.Sequential(*mod)
        model.classifier = new_classifier
        model.features = torch.nn.DataParallel(model.features)# device_ids = ) # if there is more than one gpu.
        #  model.features itself is a nn.Sequential https://pytorch.org/vision/stable/_modules/torchvision/models/alexnet.html#alexnet
    
    if torch.cuda.is_available():
        model.cuda()
        cudnn.benchmark = True
    # print(model)
    return model

class FeatureMode(object):
    def __init__(self, cnn_path):
        self.model = get_pretrained_model(model_name = "alexnet")
        print("=> loading checkpoint '{}'".format(cnn_path))
        checkpoint = torch.load(cnn_path, map_location = "cpu")
        self.model.load_state_dict(checkpoint['state_dict'])
        print("=> loaded checkpoint '{}' (epoch {})"
              .format(cnn_path, checkpoint['epoch']))   
        mod = list(self.model.classifier.children())
        mod.pop()
        mod.pop() # relu
        new_classifier = torch.nn.Sequential(*mod)
        self.model.classifier = new_classifier
           
        self.model.eval()

    def extract_feature(self, input):
        with torch.no_grad():
            input_var = torch.Tensor(input)
            output = self.model(input_var)
            return output.data.cpu().numpy()

def get_crop_box(img_w, img_h, crop_w, crop_h, crop_num_w, crop_num_h):
    interval_w = (img_w - crop_w) / crop_num_w
    interval_h = (img_h - crop_h) / crop_num_h
    w = []
    h = []
    for i in range(crop_num_w):
        w.append(0 + i * interval_w)
    for i in range(crop_num_h):
        h.append(0 + i * interval_h)
    crop_box = []
    for i in h:
        for j in w:
            crop_box.append((j, i, j + crop_w, i + crop_h))
    return crop_box
