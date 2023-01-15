# 基于PaddleDetection的Docker镜像制作、运行和发布

## 一、项目背景
Docker容器化技术可以将推理模型连同环境一起打包。开发者通过Docker进行模型部署时不需要安装各种包或者项目所需环境，十分方便地构建一个包含已训练的深度学习模型的镜像，直接运行容器就可得到推理的结果。本文利用Docker部署paddledetection训练的模型。实现在Linux环境下对图像一键化推理。

![](https://ai-studio-static-online.cdn.bcebos.com/74979206b17745869e1891f034b6da71b50da7b7ae0f41da9b2f9d0b35d5a8df)

## 二、完成paddledetection的推理过程

#### 2.1 参照[paddledetection官方文档](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.5/deploy/EXPORT_MODEL.md)，在训练完成后生成推理模型文件，主要包含四个部分：

![](https://ai-studio-static-online.cdn.bcebos.com/882d4160351648e89c9d751e0ee6fa30bdc66d7bad9a451f8d6bb5cf9f717d2c)

#### 2.2利用[FastDeploy](https://github.com/PaddlePaddle/FastDeploy)在本地python端进行部署并CPU推理

![](https://ai-studio-static-online.cdn.bcebos.com/4be33ec0a782462f82c47ad6a83e4f976eb03c6da2724a2e9f12ae81f6f9d1cd)


这个项目利用PaddleDetection在自制数据集上训练的PPYOLOE模型进行表面裂纹检测。

具体地，在构建容器时会执行ppyoloe_models.py文件，读取宿主机data/images文件夹下图片，通过训练好的PPYOLOE网络进行预测。

预测结果保存在宿主机data/images下。

在本地python端得到的效果图如下：
![](https://ai-studio-static-online.cdn.bcebos.com/2340bfc165e3499f98a0cf1c0d8a7acc45ddcdb9035f45c38f3e4723c7f07bea)

## 三、Centos7安装Docker

> **yum -y install docker-ce docker-ce-cli contained.io**

在完成安装后，执行下面命令，以确保安装成功：
> **docker run hello-world**

![](https://ai-studio-static-online.cdn.bcebos.com/206a29704900455ab91989393fc8bc003ba61161aedd4972872a92064c038c28)

## 四、编写DockerFile
Docker镜像的制作由Dockerfile文件来指定具体操作。Dockerfile可以理解为一种配置文件，用来告诉在制作镜像时应该执行哪些操作。有了Dockerfile之后，就可以利用build命令构建镜像

> FROM registry.baidubce.com/paddlepaddle/paddle:2.4.1
> 
> WORKDIR /docker_detection
> 
> COPY . /docker_detection 
> 
> RUN pip install -r requirements.txt
> 
> CMD ["python", "ppyoloe_models.py"]

Dockerfile的第1行表明是基于[paddlepaddle/paddle:2.4.1的docker镜像](https://www.paddlepaddle.org.cn/documentation/docs/zh/install/docker/linux-docker.html#anchor-0 )来制作，相当在这个镜像的基础上做了扩展来形成我们自己的镜像，其中registry.baidubce.com/paddlepaddle/paddle 表示docker镜像名，docker镜像的tag为2.4.1；

第2行表示该镜像的工作目录；

第3行表示将当前文件夹下的所有文件(docker_paddledet文件夹)copy到docker镜像中的目录/docker_detection目录下；

第4行表示在docker镜像中使用pip安装所有依赖库；

第5行表示当容器（container）运行时默认执行的命令。

## 五、制作和发布镜像

#### 5.1 制作docker镜像

> 运行以下命令：docker build -t docker_sample:2.0 ./docker_paddledet

其中-t参数指定镜像的名称为docker_sample和tag标签为2.0，其中tag标签相当于版本号，最后的小点"./docker_paddledet"表示当前目录，因为当前目录下有Dockerfile文件。

#### 5.2 运行docker容器

> docker run -it --privileged=true -v /docker_paddledet:/docker_detection e84865604928

-v /docker_paddledet:/docker_detection 表示将容器中的/docker_detection文件与宿主机/docker_paddledet进行映射，这样预测完成的图像可以直接保存宿主机，便于查看。e84865604928是容器名称

#### 5.3 发布镜像到阿里云

登录个人阿里云账号，找到容器镜像服务，然后将本地Docker镜像的tag更改为正确tag格式，然后上传至阿里云中

![](https://ai-studio-static-online.cdn.bcebos.com/b653c28151d643bda1eac78823d63be3ee3bca2598fe4dfea39c997539da0ea8)

#### 5.4 拉取镜像测试

![](https://ai-studio-static-online.cdn.bcebos.com/108cd3e020f547db8e7ec3d541b63253dc8f6b53e3a74ba19763391e923a790b)

## 六、参考资料


----



- [深度学习模型Docker镜像制作、运行和发布](https://zhuanlan.zhihu.com/p/82399067)
- [FastDeploy官方链接](https://github.com/PaddlePaddle/FastDeploy)
- [PaddleDetection官方链接](https://github.com/PaddlePaddle/PaddleDetection)
