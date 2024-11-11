from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random, os

API_TOKEN = os.getenv("API_TOKEN")

# Dictionary to keep track of user states
guess_data = {}

# Handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    number_to_guess = random.randint(1, 100)
    guess_data[chat_id] = {'number': number_to_guess, 'attempts': 5}

    update.message.reply_text('Привет! Я загадал число от 1 до 100, попробуй угадать.')
    update.message.reply_text('У тебя есть 5 попыток. Вводи ответ так: /guess XX, где XX - число. Например /guess 57')

# Handler for the /guess command
def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    if chat_id not in guess_data:
        update.message.reply_text('Пожалуйста, начните новую игру с помощью команды /start.')
        return

    try:
        user_guess = int(context.args[0])
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите корректное число после команды /guess.')
        return

    number_to_guess = guess_data[chat_id]['number']
    attempts_left = guess_data[chat_id]['attempts']

    if attempts_left <= 0:
        update.message.reply_text('К сожалению, у тебя закончились попытки. Начни новую игру с /start.')
        return

    if user_guess == number_to_guess:
        update.message.reply_text(f'Поздравляю, ты угадал число {number_to_guess}!')
        del guess_data[chat_id]
    else:
        guess_data[chat_id]['attempts'] -= 1
        attempts_left -= 1

        if attempts_left == 0:
            update.message.reply_text(f'Ты проиграл. Загаданное число было {number_to_guess}. Начни новую игру с /start.')
            del guess_data[chat_id]
        else:
            hint = 'больше' if user_guess < number_to_guess else 'меньше'
            update.message.reply_text(f'Неверно. Загаданное число {hint}. Осталось попыток: {attempts_left}.')

# Main function to start the bot
def main() -> None:
    updater = Updater(API_TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("guess", guess, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
