import os
import re
import random
import sys


class EdenVoiceUtilities:
    def __init__(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        global paths_ipt
        global paths_opt
        global encoding_raw
        global encoding_opt
        global ipt_files
        global tmp_files
        global opt_files
        paths_ipt = {'scr': os.path.join(path, 'raw_data/scr'), 'voice': os.path.join(path, 'raw_data/voice')}
        paths_tmp = os.path.join(path, 'temp')
        paths_opt = {'filelists': os.path.join(path, 'output/filelists'), 'wav': os.path.join(path, 'output/wav')}
        encoding_raw = 'Shift-JIS'
        encoding_opt = 'UTF-8'
        ipt_files = {'filelists': os.path.join(paths_tmp, 'scr-all.txt')}
        tmp_files = {'merge_scr': os.path.join(paths_tmp, 'scr-all.txt')}
        opt_files = {'filelists': [os.path.join(paths_opt['filelists'], 'transcript_train.txt'),
                                   os.path.join(paths_opt['filelists'], 'transcript_val.txt')]}

    def __find_all_files__(self, base):
        fullnames = []
        for root, ds, fs in os.walk(base):
            for f in fs:
                fullname = os.path.join(root, f)
                fullnames.append(os.path.normpath(fullname))
                # yield fullname
        return fullnames

    def merge_scr(self):
        i_d = paths_ipt['scr']
        o_f = tmp_files['merge_scr']
        files = os.listdir(i_d)
        files.sort()
        # print(files)
        scr_ = []
        filter_reg = r'[A-Z][0-9]{3}.sc'
        for i in files:
            if re.match(filter_reg, i) is not None:
                # print(os.path.join(scr_i, i))
                print('Collecting {} in {}'.format(i, i_d))
                with open(os.path.join(i_d, i), 'r', encoding=encoding_raw) as f:
                    scr_ += f.readlines()
        print('Writing {}'.format(o_f))
        with open(o_f, 'w', encoding=encoding_opt) as f:
            f.writelines(scr_)

    def filelists(self, speaker='sio'):
        print('Filtering voices of {}'.format(speaker))
        i_f = ipt_files['filelists']
        o_f = opt_files['filelists']
        o_lines = []
        filter_reg = [r'\[[0-9,-]*\]', r'{.*}']
        with open(i_f, 'r', encoding=encoding_opt) as f:
            i_c = f.readlines()
        for i in i_c:
            li = i.split(' ')
            l_ = {'type': li[0]}
            if l_['type'] == '.message':
                li[-1] = li[-1].replace('\\v\\a', '').replace('\n', '')[1:-1]  # 去掉直角引号以及结尾的\v\a还有\n
                l_ = {'type': li[0], 'voice': li[2], 'speaker': li[2][:3], 'context': li[-1]}
                for j in range(len(filter_reg)):
                    if j == 0:
                        x = re.search(filter_reg[j], l_['voice'])
                        if x is not None:
                            l_['voice'] = re.sub(filter_reg[j], "", l_['voice'])  # 过滤掉诸如 sio-C013-0002[20,0] 中的 [20,0]
                            # print(l_['voice'])
                    elif j == 1:
                        x = re.search(filter_reg[j], l_['context'])
                        if x is not None:
                            l_['context'] = re.sub(filter_reg[j], "", l_['context'])  # 过滤掉诸如 生{いの}命{ち} 中的 {いの} {ち}
                            # print(l_['context'])

                if l_['speaker'] == speaker:
                    # print(li)
                    o_l = '{}|{}'.format('wav/{}.wav'.format(l_['voice']), l_['context'])
                    o_lines.append(o_l + '\n')
                    print(o_l)

        print('Dividing all data into train set and validation set')
        random.shuffle(o_lines)  # 将序列的所有元素随机排序
        o_val = o_lines[:int(len(o_lines) * 0.1)]  # 从所有元素中取出10%作为验证集
        o_train = o_lines[int(len(o_lines) * 0.1):]  # 剩下的90%作为训练集

        print('Writing {}'.format(o_f[0]))  # 训练集
        with open(o_f[0], 'w', encoding=encoding_opt) as f:
            f.writelines(o_train)

        print('Writing {}'.format(o_f[1]))  # 验证集
        with open(o_f[1], 'w', encoding=encoding_opt) as f:
            f.writelines(o_val)

    def process_voice(self, speaker='ALL'):
        i_d = paths_ipt['voice']
        o_d = paths_opt['wav']
        files = self.__find_all_files__(i_d)
        founded = []
        # skipped = []
        for i in files:
            f = os.path.splitext(os.path.basename(i))  # 返回文件名然后分割文件名与扩展名
            speaker_ = f[0][:3]
            if speaker != 'ALL':
                if speaker_ == speaker:
                    founded.append([os.path.normpath(i), os.path.normpath(os.path.join(o_d, f[0]))])
            else:
                founded.append([os.path.normpath(i), os.path.normpath(os.path.join(o_d, f[0]))])
                # print('Found a voice of {}'.format(speaker_))
            # else:
            #     skipped.append('')
            #     print('Skipped a voice of {}'.format(speaker_))

        print('Found {} voices of {}'.format(len(founded), speaker))
        for i in range(len(founded)):
            cli = 'ffmpeg -i \"{}\" -ar 22050 \"{}.wav\"'.format(founded[i][0], founded[i][1])
            print('Executing: {}'.format(cli))
            os.system(cli)
            print('\n\n{}/{}\n\n'.format(i+1, len(founded)))

if __name__ == '__main__':
    eden = EdenVoiceUtilities()
    # eden.merge_scr()
    switchers = []
    help_text = 'jieran233/eden_voice_utilities\nThis is a help text.\nPlease see README.md at first.'

    if len(sys.argv) == 1:
        print(help_text)
        exit()
    elif len(sys.argv) >= 2:
        func = sys.argv[1]
        if len(sys.argv) > 2:
            switchers = sys.argv[2:]
    # print(func, switchers)

    if func == 'merge_scr':
        eden.merge_scr()
    elif func == 'filelists':
        if len(switchers) == 0:
            eden.filelists()
        else:
            eden.filelists(switchers[0][2:])
    elif func == 'process_voice':
        eden.process_voice()
        # # The filter has an unknown bug, do noe use.
        # if len(switchers) == 0:
        #     eden.process_voice()
        # else:
        #     eden.process_voice(switchers[0][2:])
    else:
        print(help_text)
