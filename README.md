# 1、目录及文件说明

[data]- 存放数据的目录

    - train-supermap.zip: 输入的开源变化检测数据集的样例数据

- convert_to_sm_cd_train_set.py: 超图变化检测数据集转换
- convert_to_sm_cs_train_set.py: 超图分类数据集转换
- py38.yaml: 程序运行的环境，可通过conda创建到本地
- template.sda: 超图sda文件的模板文件


# 2、使用

将data文件夹下的zip压缩包解压到当前文件夹，然后在控制台执行下面的语句

    - python convert_to_sm_cd_train_set.py data\train-supermap
