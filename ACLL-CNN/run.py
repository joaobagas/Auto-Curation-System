from numpy import exp
from PIL import ImageEnhance
from module import Net


def run():
    outputs = run_net()
    for output in outputs:
        img = change_brightness(None, exp(output[0]))
        img = change_contrast(img, exp(output[1]))

def run_net():
    transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Resize((200, 200))])
    test_set = datasets.ImageFolder("datasets/acll/test", transform=transform)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=1, shuffle=False)

    net = load()
    net.eval()

    predictions = []

    for i, data in enumerate(test_loader, 0):
        inputs, _ = data
        outputs = net.forward(inputs)
        _, predicted = torch.max(outputs.data, 1)
        predictions.append(outputs)

    return outputs


def load():
    model = Net()
    PATH = "checkpoint/model.pt"

    checkpoint = torch.load(PATH)
    model.load_state_dict(checkpoint['model_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']

    return model, epoch, loss


def change_brightness(img, value):
    image_enhancer = ImageEnhance.Brightness(img)
    return image_enhancer.enhance(value)


def change_contrast(img, value):
    image_enhancer = ImageEnhance.Contrast(img)
    return image_enhancer.enhance(value)
