import pretrainedmodels
from torch import nn
from torchvision import models


class FCViewer(nn.Module):
    def forward(self, x):
        return x.view(x.size(0), -1)


class PretrainedModel(nn.Module):
    def __init__(self, backbone, drop, ncls):
        super().__init__()
        model = pretrainedmodels.__dict__[backbone](num_classes=1000, pretrained='imagenet')

        self.encoder = list(model.children())[:-2]

        self.encoder.append(nn.AdaptiveAvgPool2d(1))
        self.encoder = nn.Sequential(*self.encoder)

        if drop > 0:
            self.classifier = nn.Sequential(FCViewer(),
                                            nn.Dropout(drop),
                                            nn.Linear(model.last_linear.in_features, ncls))
        else:
            self.classifier = nn.Sequential(
                FCViewer(),
                nn.Linear(model.last_linear.in_features, ncls)
            )

    def forward(self, x):
        x = self.encoder(x)
        x = self.classifier(x)
        return x


class KneeNet(nn.Module):
    """
    Aleksei Tiulpin, Unversity of Oulu, 2017 (c).

    """

    def __init__(self, backbone_net, drop):
        super(KneeNet, self).__init__()
        backbone = PretrainedModel(backbone_net, 1, 1)

        self.features = backbone.encoder

        # 5 KL-grades
        self.classifier_kl = nn.Sequential(nn.Dropout(p=drop),
                                           nn.Linear(backbone.classifier[-1].in_features, 5))
        # 3 progression sub-types
        self.classifier_prog = nn.Sequential(nn.Dropout(p=drop),
                                             nn.Linear(backbone.classifier[-1].in_features, 3))

    def forward(self, x):
        o = self.features(x)
        feats = o.view(o.size(0), -1)
        return self.classifier_kl(feats), self.classifier_prog(feats)
