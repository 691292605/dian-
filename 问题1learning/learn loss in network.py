import torchvision.datasets
from torch import nn, optim
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
"""
该部分代码主要是进行将损失函数运用于神经网络的实践以及搭建优化器的实践，神经网络利用的是自己搭建的简单RNN（循环神经网络）
同时在最后搭建出了简单的神经网络的训练过程
"""
#导入加载数据集
dataset = torchvision.datasets.FashionMNIST(root = './data', train = False,
                                            transform = transforms.ToTensor(), download = False)
dataloader = DataLoader(dataset = dataset, batch_size = 10, shuffle = True)

"""
复制之前已经写好的简单RNN网络
"""

class New_hidden(nn.Module):#对数据进行处理，得到新的隐藏层
    def __init__(self, input_size, hidden_size):
        super(New_hidden, self).__init__()
        self.input_size = input_size#初始化输入层的大小
        self.hidden_size = hidden_size#初始化隐藏层的大小
        self.i_to_h = nn.Linear(input_size, hidden_size)#定义从输入层到隐藏层的线性变换
        self.h_to_h = nn.Linear(hidden_size, hidden_size)#定义从隐藏层到隐藏层的线性变换

    def forward(self, x, hidden):
        combined = self.i_to_h(x) + self.h_to_h(hidden)
        new_hidden = torch.tanh(combined)
        return new_hidden


class MyRNN(nn.Module):#搭建RNN的模型
    def __init__(self, input_size, hidden_size, output_size):
        super(MyRNN, self).__init__()
        self.hidden_size = hidden_size#初始化隐藏层的大小
        self.h_to_o = nn.Linear(hidden_size, output_size)#定义从隐藏层到输出层的线性变换
        self.new_hidden = New_hidden(input_size, hidden_size)

    def forward(self, x):#定义RNN的前进层
        batch_size, seq_len, _= x.size()#获取样本每次训练处理的数量和序列长度
        hidden = torch.zeros(batch_size, self.hidden_size)
        for data in range(seq_len):#对序列进行循环的处理
            hidden = self.new_hidden(x[:, data,: ], hidden)
        output = self.h_to_o(hidden)#获取最终的输出层
        return output

#初始化变量和定义网络模型
inputsize = 28
hiddensize = 128
outputsize = 10
my_rnn = MyRNN(inputsize, hiddensize, outputsize)

"""
定义损失函数，构造优化器
"""

loss = nn.CrossEntropyLoss()    #选择交叉熵作为损失函数
optimizer = optim.Adam(my_rnn.parameters(), lr = 0.001)    #选择优化器

"""
结合learn data的内容来调取dataloader的返回值
由于是分类问题故选择交叉熵损失函数
通过result_loss.backward()语句来获得反向输入的梯度，为选择优化器做铺垫
"""
#由于在搭建dataloader的过程中选择了将数据打乱，故可以加上一个训练次数（epochs）来进行多次训练
epochs = 4  #进行的训练次数

for epoch in range(epochs):
    running_loss = 0.0
    for Data in dataloader:
        imgs, targets = Data
        imgs = imgs.view(imgs.size(0), 28, 28)      #将imgs的原数据类型[batch_size, 1, 28, 28]去掉其中的通道数(1)以适应输入
        optimizer.zero_grad()   #将上一步所得到的梯度清零
        outputs = my_rnn(imgs)      #获得神经网络的输出
        #print(outputs)
        #print(targets)
        result_loss = loss(outputs, targets)
        result_loss.backward()   #反向获得梯度
        #print(result_loss)
        optimizer.step()
        running_loss = running_loss + result_loss     #将每一轮训练所产生的loss叠加
    print(running_loss)     #输出本轮训练过程中的loss，相当于训练过程的可视化

"""
自此以上的for循环搭建出了简单的循环网络的训练过程
"""







