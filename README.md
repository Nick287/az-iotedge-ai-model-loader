# How To Enable AI Model On Azure IoT Edge Device

## Background

One of the most popular Edge scenarios is the artificial intelligence (AI) on Edge (Image Classification, Object Detection, Body, Face & Gesture Analysis, Image Manipulation, ETC ... ). Azure IoT Edge can certainly support these scenarios, These AI ability can also be improve over the model update, but in some scenarios the Edge device network environment is not good, Especially for some manufacturing equipment (such as wind power or oil exploitation), in the desert or at sea.

However, as you know, Azure IoT Edge Module is the basis on docker. In generally an Edge module image with the AI environment which size will be around GB level at least, so how to incremental updates the AI model in a narrow bandwidth network its becomes more meaningful. This is the reason I made this sample. I have made a Edge AI loader module which can load *Object Detection* TensorFlow or ONNX AI models and enable this AI module as a WebAPI.

## Overview

In This AI loader sample have some Key concepts need to be clarify first.

TensorFlow:

1. AI Model File: *.tflite its pre-trained AI model which download from [TensorFlow.org - Download starter model with Metadata](https://www.tensorflow.org/lite/examples/object_detection/overview) and its a generic AI model format that can be used in cross-platform applications such as IOS and Android. And about more information about Metadata and associated fields (eg: labels.txt) see [Read the metadata from models](https://www.tensorflow.org/lite/convert/metadata#read_the_metadata_from_models)
2. Model description： An object detection model is trained to detect the presence and location of multiple classes of objects. For example, a model might be trained with images that contain various pieces of fruit, along with a label that specifies the class of fruit they represent (e.g. an apple, a banana, or a strawberry), and data specifying where each object appears in the image.

    When an image is subsequently provided to the model, it will output a list of the objects it detects, the location of a bounding box that contains each object, and a score that indicates the confidence that detection was correct.
3. In case of if you want to build or customize tuning an AI Model please see [TensorFlow Lite Model Maker](https://www.tensorflow.org/lite/guide/model_maker)
4. More free pre-trained detection models with a variety of latency and precision characteristics can be found in the [Detection Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md#mobile-models). Each one of them follows the input and output signatures described in the following sections.

Open Neural Network Exchange (ONNX):

Open Neural Network Exchange (ONNX) is an open standard format for representing machine learning models. ONNX is supported by a community of partners who have implemented it in many frameworks and tools.

1. ONNX supports a variety of tools to Build and deploy models and Frameworks & Converters [Build / Deploy Model](https://onnx.ai/supported-tools.html)
2. You can use ONNX runtime run ONNX Pre-Trained Models [ONNX Model Zoo](https://github.com/onnx/models) for implementation Vision Language Other AI features
3. In this sample i used model of [Object Detection & Image Segmentation - Tiny YOLOv3](https://github.com/onnx/models/tree/master/vision/object_detection_segmentation/tiny-yolov3)

### Input to model

Resized image (1x3x416x416) Original image size (1x2) which is [image.size[1], image.size[0]]

### Output of model

The model has 3 outputs. boxes: (1x'n_candidates'x4), the coordinates of all anchor boxes, scores: (1x80x'n_candidates'), the scores of all anchor boxes per class, indices: ('nbox'x3), selected indices from the boxes tensor. The selected index format is (batch_index, class_index, box_index). The class list is [here](https://github.com/qqwweee/keras-yolo3/blob/master/model_data/coco_classes.txt)

### Preprocessing steps

```python
import numpy as np
from PIL import Image

# this function is from yolo3.utils.letterbox_image
def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128,128,128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image

def preprocess(img):
    model_image_size = (416, 416)
    boxed_image = letterbox_image(img, tuple(reversed(model_image_size)))
    image_data = np.array(boxed_image, dtype='float32')
    image_data /= 255.
    image_data = np.transpose(image_data, [2, 0, 1])
    image_data = np.expand_dims(image_data, 0)
    return image_data

image = Image.open(img_path)
# input
image_data = preprocess(image)
image_size = np.array([image.size[1], image.size[0]], dtype=np.float32).reshape(1, 2)
```

This Edge AI loader module architecture please refer below
![image](image/architecture_diagram.png)
