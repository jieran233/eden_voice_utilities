# eden_voice_utilities

面向机器学习的eden*语音与文本实用工具

## Usage

如无特殊说明，本文中 `./` 均指本项目的本地根目录（WorkDir）

### Tutorial

#### 提取语音与脚本

> Resource    `eden*` or `eden* PLUS MOSAIC`
> 
> Tool    [morkt/GARbro](https://github.com/morkt/GARbro)

提取    `voice.paz`    (语音)    到    `./raw_data/voice/`

提取    `scr.paz`        (脚本)    到    `./raw_data/scr/`

![](https://s2.loli.net/2022/08/07/vncRYrtUEsi1jFk.png)

#### 合并全部脚本 (merge_scr)

> Input	`./raw_data/scr/[A-Z][0-9]{3}.sc`	(Shift-JIS)
>
> Output	`./temp/scr-all.txt`	(UTF-8)

```
cd ./
# 用法 main.py merge_scr
python3 main.py merge_scr
```

#### 生成filelists (filelists)

> Input	`./temp/scr-all.txt`	(UTF-8)
>
> Output
>
> - train set 	`./output/filelists/transcript_train.txt`	(UTF-8)
> - validation set 	`./output/filelists/transcript_val.txt`	(UTF-8)

```
cd ./
# 用法 main.py filelists [--speaker]
python3 main.py filelists
# 等效于 main.py filelists --sio
```

可选参数`speaker`的默认值为[^sio]（请注意不要忘记`--`）

程序会默认将收集到的的所有的 文本与对应语音文件 随机排序，并从中取出`10%`作为验证集，剩下的`90%`作为训练集

[^sio]: 也就是形如`sio-C013-0186.ogg`的eden\*语音文件名的前3个字符，在eden\*中可选值有`eri`(エリカ/艾莉卡), `etc`(其他), `ina`(稲葉直人/稻叶直人), `may`(塔野真夜/塔野真夜), `nat`(ナツメ/夏目), `rav`(浅井･F･ラヴィニア/浅井·F·拉维尼娅), `ryo`(榛名亮/榛名亮), `sio`(シオン/诗音)

#### 处理音频文件 (process_voice)

> Input	`./raw_data/voice/*`
>
> Output	`./output/wav/*.wav`

```
cd ./
# 用法 main.py process_voice
python3 main.py process_voice
```

程序默认会将收集到的所有文件调用[^ffmpeg]可执行文件将其重采样为`22050Hz`并转换为`wav`格式

[^ffmpeg]:毋庸置疑，你的设备上需要安装ffmpeg并将其添加到PATH

## Reference

灵感来源    [基于tacotron2合成宁宁语音（day1-2）_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1rV4y177Z7)

用途    **[CjangCjengh/tacotron2-japanese: Tacotron2 implementation of Japanese (github.com)](https://github.com/CjangCjengh/tacotron2-japanese)**

资源提取

- [morkt/GARbro: Visual Novels resource browser (github.com)](https://github.com/morkt/GARbro)
