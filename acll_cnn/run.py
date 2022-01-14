import torch
from PIL import Image
from numpy import exp
from PIL import ImageEnhance
from torchvision.transforms import transforms

from acll_cnn.module import Net


def run_cnn(imgs):
    outputs = run_net(imgs)
    out_imgs = []
    c = 0
    for output in outputs:
        img = change_brightness(Image.fromarray(imgs[c]), float(exp(output.detach().numpy()[0])))
        out_imgs.append(img)
        c+=1
    return out_imgs

def run_net(imgs):
    net = load()
    net.eval()

    predictions = []

    for i, data in enumerate(imgs, 0):
        tensor = torch.Tensor(data.transpose(2, 0, 1))
        resize = transforms.Resize((200, 200))
        tensor = resize(tensor)
        outputs = net.forward(tensor.unsqueeze(0))
        _, predicted = torch.max(outputs.data, 1)
        predictions.append(outputs)
    return outputs


def load():
    model = Net()
    PATH = "acll_cnn/checkpoint/model.pt"

    checkpoint = torch.load(PATH)
    model.load_state_dict(checkpoint['model_state_dict'])

    return model


def change_brightness(img, value):
    image_enhancer = ImageEnhance.Brightness(img)
    return image_enhancer.enhance(value)


def change_contrast(img, value):
    image_enhancer = ImageEnhance.Contrast(img)
    return image_enhancer.enhance(value)
