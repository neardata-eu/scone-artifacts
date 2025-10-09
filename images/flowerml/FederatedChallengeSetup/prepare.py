from torchvision.datasets import CIFAR10
import torchvision.transforms as transforms

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)
trainset = CIFAR10("input/", train=True, download=True, transform=transform)
testset = CIFAR10("input/", train=False, download=True, transform=transform)