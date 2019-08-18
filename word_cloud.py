from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import jieba
import os


def _generate_cn_words(text, want_words=[], stop_words=[]):
    """
    :param text: the source text, like an article
    :param want_words: the special word that you want. like "xxyy" not "xx" and "yy"
    :param stop_words: the words you do not want to show
    :return: return the words list like "xxx xxx"
    """
    for word in want_words:
        jieba.add_word(word)

    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = ' '.join(seg_list)

    for myword in liststr.split(' '):
        if len(myword.strip()) > 1 and myword.strip() not in stop_words:
            mywordlist.append(myword)
    return ' '.join(mywordlist)


def generate_wordcloud(text_path, mask_path=None, width=400, height=400, lan='en', font_path=None, want_worlds=[],
                       stop_words=[], path_to_save='.'):
    """
    generate a word cloud of the mask picture you provide and a word cloud color by your picture
        :param text_path: use to generate words
        :param mask_path: picture you want to show
        :param width: the width of the word cloud picture, if mask_path is not provided
        :param height: the height of the word cloud picture, if mask_path is not provided
        :param lan: the language of your text
        :param font_path: if lan is 'cn', a chinese font must provide
        :param want_worlds:  the special word you don't want to separate
        :param stop_words:  the words you don't want to show up in your word cloud
        :param path_to_save: the directory you want to save your word cloud (!! is directory not file)
        :return: no return
    """
    image_colors = None
    wc = WordCloud(background_color='white',
                   max_words=1000,
                   max_font_size=400,
                   random_state=42)
    # check path
    if not os.path.isfile(text_path):
        print('## text_path is invalid !!')
        return

    if lan == 'cn':
        # if the lan is cn, then the path of chinese font path can't be null
        if not os.path.isfile(font_path):
            print('## chinese font_path cannot be null !!')
            return
        text = _generate_cn_words(text=open(text_path).read(), want_words=want_worlds, stop_words=stop_words)
        wc.font_path = font_path
    else:
        text = open(text_path).read()

	if not os.path.isfile(font_path):
		wc.font_path = font_path

    if mask_path is None and width > 0 and height > 0:
        wc.height = height
        wc.width = width
    elif os.path.isfile(mask_path):
        mask = np.array(Image.open(mask_path))
        wc.mask = mask
        image_colors = ImageColorGenerator(mask)
    else:
        print('## mask_path is invalid !!')
        return

    wc.generate(text=text)
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    plt.show()

    if os.path.isdir(path_to_save):
        wc.to_file(os.path.join(path_to_save, 'words.png'))
    else:
        print('## path_to_save is invalid !!')
        return

    if mask_path is not None:
        img1 = Image.open(os.path.join(path_to_save, 'words.png'))
        img2 = Image.open(mask_path)
        width = img1.size[0]
        height = img1.size[1]

        for i in range(0, width):
            for j in range(0, height):
                data1 = (img1.getpixel((i, j)))
                data2 = (img2.getpixel((i, j)))
                if (data1[0] <= 250
                        or data1[1] <= 250
                        or data1[2] <= 250):
                    img1.putpixel((i, j), (data2[0], data2[1], data2[2], 255))
        # if (data1[0] == 255
        #         and data1[1] == 255
        #         and data1[2] == 255):
        #     img1.putpixel((i, j), (205, 205, 205, 255))

        plt.imshow(img1)
        plt.axis('off')
        plt.show()
        img1.save(os.path.join(path_to_save, 'wordcloud.png'))

# example
# generate_wordcloud(mask_path='../file/ant.jpeg', lan='cn', font_path='../file/STHUPO.TTF', text_path='../file/novel',
#                  path_to_save='/home/zjs/Desktop/')
