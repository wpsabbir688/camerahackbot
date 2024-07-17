import cv2
import os
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open camera")

    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise Exception("Could not read frame")

    filename = "capture.jpg"
    cv2.imwrite(filename, frame)
    cap.release()
    return filename

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! Send /capture to take a photo.')

def capture(update: Update, context: CallbackContext):
    try:
        filename = capture_image()
        with open(filename, 'rb') as photo:
            update.message.reply_photo(photo=InputFile(photo))
        os.remove(filename)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    updater = Updater("7206173478:AAGAC_RhjKKs_hWPtOY-U_A6DrUw8XEIseE")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("capture", capture))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
