import logging, re, requests, ffmpeg, os, subprocess
from urllib.request import urlopen
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler)
from pytube import YouTube
from moviepy.editor import *

def start(update, context):
    update.message.reply_text(
        'Hello, world! I will help you download Youtube videos in either .mp3 or .mp4 format. Simply use either /mp3 or /mp4 followed by the link to the video. Use /help for more.'
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
    vid = open(fp2, 'rb')
    update.message.reply_audio(vid)
    vid.close()
    os.remove(fp1)
    os.remove(fp2)


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


def help(update, context):
    update.message.reply_text("""
    Here are the list of commands:
    ---------------------
    /mp3 <link> - downloads the given Youtube video as .mp3
    /mp4 <link> - downloads the given Youtube video as .mp4
    ---------------------
    """)


def test(update, context):
    update.message.reply_text("Test received WOOO")


def main():
    updater = Updater(open("token.txt", 'r').read(), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mp3", mp3))
    dp.add_handler(CommandHandler("mp4", mp4))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()

    print("Successfully started YourMusePal")

    updater.idle()


if __name__ == '__main__':
    main()
