import telebot
import subprocess
import os
import uuid

bot = telebot.TeleBot('6539659434:AAGYu_H-WpEguArXm95eAvwemrKiVo11rtY')

ffmpeg_location = 'E:\\ffmepg\\ffmpeg-master-latest-win64-gpl-shared\\bin'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Welcome to the YouTube to MP3 converter bot!\nSend me a YouTube video URL, and I'll send you the MP3 audio.")


@bot.message_handler(func=lambda message: True)
def convert_to_mp3(message):
    try:
        video_url = message.text

        unique_filename = str(uuid.uuid4()) + '.mp3'

        subprocess.call(
            ['yt-dlp', '--ffmpeg-location', ffmpeg_location, '--extract-audio', '--audio-format', 'mp3', '-o',
             unique_filename, video_url])

        if os.path.isfile(unique_filename):

            with open(unique_filename, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file)

            os.remove(unique_filename)
        else:
            bot.send_message(message.chat.id, "Conversion failed. Please try again.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


if __name__ == "__main__":
    bot.polling()
