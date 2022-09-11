# -*-coding:utf-8-*-
import argparse

from model.models import * 
from model.utils.datasets import *
from model.utils.utils import *
from model.foodname import foodname
from xml.etree.ElementTree import Element, SubElement


class FoodModel:
    optData={}
    def __init__(self,folderName) -> None:
        self.optData["cfg"]=check_file("model/cfg/yolov3-spp-403cls.cfg")
        self.optData["names"]="model/data/403food.names"
        self.optData["output"]="model/output"
        self.optData["source"]=check_file(folderName)
        self.optData["weights"]="model/weights/best_403food_e200b150v2.pt"
        self.optData["half"]="store_true"
        self.optData["img_size"]=320
        self.optData["device"]=''
        self.optData["augment"]="store_true"
        self.optData["conf_thres"]=0.3
        self.optData["iou_thres"]=0.5
        self.optData["classes"]=''
        self.optData["agnostic_nms"]=''
        
    async def detect(self):
        imgsz = (320, 192) if ONNX_EXPORT else self.optData["img_size"]
        out, source, weights, half = self.optData["output"], self.optData["source"], self.optData["weights"], self.optData["half"]
        webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')
        # Initialize
        device = torch_utils.select_device(device='cpu' if ONNX_EXPORT else self.optData["device"])
        if os.path.exists(out):
            shutil.rmtree(out)  # delete output folder
        os.makedirs(out)  # make new output folder

        # Initialize model
        model = Darknet(self.optData["cfg"], imgsz)

        # Load weights
        attempt_download(weights)
        if weights.endswith('.pt'):  # pytorch format
            model.load_state_dict(torch.load(weights, map_location=device)['model'], strict=False)
        else:  # darknet format
            load_darknet_weights(model, weights)

        # Second-stage classifier
        classify = False
        if classify:
            modelc = torch_utils.load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'],
                                strict=False)  # load weights
            modelc.to(device).eval()

        # Eval mode
        model.to(device).eval()

        # Half precision
        half = half and device.type != 'cpu'  # half precision only supported on CUDA
        if half:
            model.half()

        if webcam:
            torch.backends.cudnn.benchmark = True
            dataset = LoadStreams(source, img_size=imgsz)
        else:
            dataset = LoadImages(source, img_size=imgsz)

        names = load_classes(self.optData["names"])
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img.float()) if device.type != 'cpu' else None  # run once
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            pred = model(img, augment=self.optData["augment"])[0]

            # to float
            if half:
                pred = pred.float()

            # Apply NMS
            pred = non_max_suppression(pred, self.optData["conf_thres"], self.optData["iou_thres"],
                                    multi_label=False, classes=self.optData["classes"], agnostic=self.optData["agnostic_nms"])

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections for image i
                if webcam:  # batch_size >= 1
                    p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                else:
                    p, s, im0 = path, '', im0s

                save_path = str(Path(out) / Path(p).name)
                #s += '%gx%g ' % img.shape[2:]  # print string

                root = Element('annotation')
                SubElement(root, 'folder').text = str(Path(out))
                SubElement(root, 'filename').text = str(Path(p))
                SubElement(root, 'path').text = save_path
                
                if det is not None and len(det):
                    # Rescale boxes from imgsz to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    foods=[]

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %s, ' % (n, names[int(c)])  # add to string
                        try:
                            foods.append(foodname[names[int(c)]])
                        except:
                            pass
                return " ".join(foods)
                
        print('Done. (%.3fs)' % (time.time() - t0))
