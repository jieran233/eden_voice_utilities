# eden_voice_utilities

面向机器学习的 `eden*` 语音与文本实用工具

## Usage

如无特殊说明，本文中 `./` 均指本项目的本地根目录（WorkDir）

### 提取语音与脚本

> 资源	`eden*` or `eden* PLUS MOSAIC`
>
> 工具	[morkt/GARbro](https://github.com/morkt/GARbro)

提取	`voice.paz`	(语音)	到	`./voice`

提取	`scr.paz`		(脚本)	到	`./scr`

![](https://s2.loli.net/2022/08/07/vncRYrtUEsi1jFk.png)

### merge_texts.py

> 用于合并`texts/`中的所有`*.xlsx`表格为`texts_all.xlsx`

```
cd ./Test
python merge_texts.py
# 输出文件 ./Test/texts_all.xlsx
```

### 将 xlsx 转换为 csv

最简单的方法就是用 MS Office Excel打开`texts_all.xlsx`，然后另存为`texts_all.csv`

 (当然你也可以用LibreOffice Calc，但是我不确定两者另存的内容会不会有差异) 

### filter.py

> 从`texts_all.csv`中过滤内容（去除旁白和男主这两个没有语音的角色，还有同样没有语音的省略句）
>
> （debug `gen-tacotron2-filelists.py`的时候找了好久才发现省略句也没有语音...）

```
cd ./Test
python filter.py
# 输出文件 ./Test/texts_all.withoutblk.marked.csv
```

### process-voices.py

> 调用`ffmpeg`批量将语音转为`wav`格式并重采样为`22050Hz`
>
> （毋庸置疑，你需要安装ffmpeg并将其添加到PATH）

```
cd ./Test
# It will take a few time
python process-voices.py
# 输出目录 ./wav/
```

### 手动修正

> 有一些内容无法处理，需要手动将其剔除
>
> （解决不了问题就解决问题本身，宁可数据集里少一点也不能有错误数据）

```
cd ./wav
move .\z6430\ .\z6430.bak\
```

### gen-tacotron2-filelists.py

> 生成用于tacotron2的`transcript_train.txt`和`transcript_val.txt`

编辑`gen-tacotron2-filelists.py`以筛选角色（语音的朗读者）

(at about line `50` in `gen-tacotron2-filelists.py`)

```
#### 在此处筛选角色
if reader[1:-1] == '古河' or reader[1:-1] == '＄古河' or reader[1:-1] == '渚' or reader[1:-1] == '＄渚':
```

然后运行

```
cd ./Test
# It will take a few time
python gen-tacotron2-filelists.py
# 输出文件
# ./Test/transcript_train.txt	(training set)
# ./Test/transcript_val.txt		(validation set)
```

## Reference

灵感来源	[基于tacotron2合成宁宁语音（day1-2）_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1rV4y177Z7)

用途	**[CjangCjengh/tacotron2-japanese: Tacotron2 implementation of Japanese (github.com)](https://github.com/CjangCjengh/tacotron2-japanese)**

资源提取

- [morkt/GARbro: Visual Novels resource browser (github.com)](https://github.com/morkt/GARbro)

