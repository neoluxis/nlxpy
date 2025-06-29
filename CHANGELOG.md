# Changelog

<!-- 
指导原则
    记住日志是写给人而非机器的。
    每个版本都应该有独立的入口。
    同类改动应该分组放置。
    不同版本应分别设置链接。
    新版本在前，旧版本在后。
    应包括每个版本的发布日期。
    注明是否遵守语义化版本规范。
变动类型
    Added 新添加的功能。
    Changed 对现有功能的变更。
    Deprecated 已经不建议使用，即将移除的功能。
    Removed 已经移除的功能。
    Fixed 对 bug 的修复。
    Security 对安全性的改进。
 -->

All notable changes to this project (NlxPy) will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-06-29

### Added 

- Experiment management: folder creation [misc]
- Random seed mutator and accesor [dl]
- Dependencies checker: add `requirements.txt` support [misc]

### Changed 

- Denpendencies checker: detect all deps and install together [misc]
- General dependency update `numpy` 

## [0.0.1] - 2025-06-12

### Added

- Dependency checker and installer [misc]
- Arbitrary direction gray transform of image [cv]
- Create basic skeletons of deep learning modules [dl]
- Add registration and unregistration for models [dl]
- Add somple module: MLP and Conv2d Block [dl]
- add a basic template for model definition yaml, may need more modifications [dl]

