import torch
import torchvision

def main():
    net = torchvision.models.resnet18(pretrained=True)
    net.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
    print(net)

    print(f"cuda:0 is available: {torch.cuda.is_available()}")

if __name__ == '__main__':
    main()