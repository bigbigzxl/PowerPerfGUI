# AI移动端底层性能优化利器

> 在当前AI移动端的环境下，主流还是使用CPU以及GPU进行底层计算，其中GPU如高通系列均有完善配套的性能优化工具配套使用，但是ARM移动端则没有免费的、趁手的工具来进行使用，因此我就仿照ARM-DS5 streamline 进行设计，造一个免费的轮子出来，而且针对我们目前的AI场景来说更趁手。




用一两段话介绍这个项目以及它能做些什么。

我们在移动端会设计一套推理框架，框架的计算核心就是一些汇编kernel

![](https://github.com/bigbigzxl/PowerPerfGUI/blob/master/PowerPerfGUI/schedule0.jpg)

![](https://github.com/bigbigzxl/PowerPerfGUI/blob/master/PowerPerfGUI/schedule1.jpg)


## Getting Started 使用指南

项目使用条件、如何安装部署、怎样运行使用以及使用演示

### Prerequisites 项目使用条件

你需要安装什么软件以及如何去安装它们。

```
Give examples
```

### Installation 安装

通过一步步实例告诉你如何安装部署、怎样运行使用。

OS X & Linux:

```sh
Give the example
```

Windows:

```sh
Give the example
```

### Usage example 使用示例

给出更多使用演示和截图，并贴出相应代码。

## Deployment 部署方法

部署到生产环境注意事项。

## Contributing 贡献指南

Please read [CONTRIBUTING.md](#) for details on our code of conduct, and the process for submitting pull requests to us.

清阅读 [CONTRIBUTING.md](#) 了解如何向这个项目贡献代码

## Release History 版本历史

* 0.2.1
    * CHANGE: Update docs
* 0.2.0
    * CHANGE: Remove `README.md`
* 0.1.0
    * Work in progress

## Authors 关于作者

* **WangYan** - *Initial work* - [WangYan](https://wangyan.org)

查看更多关于这个项目的贡献者，请阅读 [contributors](#) 

## License 授权协议

这个项目 MIT 协议， 请点击 [LICENSE.md](LICENSE.md) 了解更多细节。

