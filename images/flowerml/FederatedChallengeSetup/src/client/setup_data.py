from torchvision.datasets import CIFAR10
import torchvision.transforms as transforms

transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)
trainset1 = CIFAR10("../input/client1", train=True, download=True, transform=transform)
testset1 = CIFAR10("../input/client1", train=False, download=True, transform=transform)


trainset2 = CIFAR10("../input/client2", train=True, download=True, transform=transform)
testset2 = CIFAR10("../input/client2", train=False, download=True, transform=transform)
