import logging, re, requests, ffmpeg, os, subprocess
from urllib.request import urlopen
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler)
from pytube import YouTube
from moviepy.editor import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        'Hello, world!'
        'I will help you download Youtube videos in either .mp3 or .mp4 format.'
        'Simply use either /mp3 or /mp4 followed by the link to the video.'
    )


def mp3(update, context):
    link = context.args[0]
    print(link)
    yt = YouTube(link)

    update.message.reply_text('Roger! It may take a couple of minutes, depending on the length of the video. Please be patient!')
    stream = yt.streams.first()
    stream.download('./downloads')
    print(stream.title)
    fp1 = ('./downloads/' + yt.title + '.mp4')
    fp2 = ('./downloads/' + yt.title + '.mp3')
    video = VideoFileClip(os.path.join(fp1))
    video.audio.write_audiofile(os.path.join(fp2))
    # subprocess.call([
    #     'ffmpeg',
    #     '-i', os.path.join('./downloads', yt.title+'.mp4'), os.path.join('./downloads', yt.title+'.mp3')
    # ], shell=True)
    vid = open(fp2, 'rb')
    update.message.reply_audio(vid)
    vid.close()
    os.remove(fp1)
    os.remove(fp2)

    # if 'youtube' not in link:
    #     update.message.reply_text('Please send a valid youtube link!')
    # else:
    #     l = urlopen(link)
    #     contents = str(l.read())
    #     print(type(contents))
    #     # m = re.search('formats.+url.+mimeType.+;', contents)
    #     # src = m.group(0)
    #     # print(src)
    #     src = contents[44550:-357000]
    #     print('string slicer:', src)
    #     m = re.search('formats.+:18.+url(.+)mimeType.+;', src)
    #     src = m.group(0)
    #     print(m.group(1))
    #     print('src:', src)
    #     # src = src[40:-15]
    #     # print(src)
    #     patt = '\\\\'
    #     print(patt)
    #     src = re.sub(patt, '', src)
    #     print(src)
    #     src = src[28:-10270]
    #     print(src)
    #     m2 = re.search('(https.+)","mimeType', src)
    #     print(m2.group(0))
    #     x = m2.group(0)
    #     src = x[0:-11]
    #     print(src)


def mp4(update, context):
    link = context.args[0]
    print(link)
    yt = YouTube(link)

    update.message.reply_text('Roger! It may take a couple of minutes, depending on the length of the video. Please be patient!')
    stream = yt.streams.first()
    stream.download('./downloads')
    print(stream.title)
    fp = ('./downloads/' + yt.title + '.mp4')
    vid = open(fp, 'rb')
    update.message.reply_video(vid)
    vid.close()
    os.remove(fp)


def test(update, context):
    update.message.reply_text("Test received WOOO")


def main():
    updater = Updater(open("token.txt", 'r').read(), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mp3", mp3))
    dp.add_handler(CommandHandler("mp4", mp4))
    dp.add_handler(CommandHandler("test", test))

    updater.start_polling()

    print("Successfully started YourMusePal")

    updater.idle()


if __name__ == '__main__':
    main()
