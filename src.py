from typing import final
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Application, filters, ContextTypes, CallbackContext
import aiohttp,datetime, random, inspect
import os, re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


TOKEN: final= os.getenv('TOKEN')
BOTUSERNAME: final= os.getenv('BOTUSERNAME')
API_KEY: final= os.getenv('API_KEY')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ''' This is used to start the bot.'''
    await update.message.reply_text('''Hello there, thanks for chatting with me! 
What do you want me to do for you today?
Type /help to see all commands.''')
    
async def help_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    '''This provides information about all functions or a specific one.\n
To implement, type /help to print information for all functions or type /help {function_name} to print 
information about a specific function.'''
    if context.args:
        func_name = context.args[0]
        func = globals().get(f"{func_name}_command")
        if func and inspect.iscoroutinefunction(func):
            await update.message.reply_text(f"Help for '{func_name}':\n{func.__doc__}")
        else:
            await update.message.reply_text(f"No command named '{func_name}' found.")
    else:
        # Display docstrings of all available commands
        response = "Available commands and their descriptions:\n"
        for name, obj in globals().items():
            if inspect.iscoroutinefunction(obj) and name.endswith('_command'):
                response += f"/{name[:-8]}: {obj.__doc__}\n"

        # Split response into chunks to avoid exceeding Telegram's character limit
        chunk_size = 4000  # Leave some buffer for formatting
        for i in range(0, len(response), chunk_size):
            await update.message.reply_text(response[i:i+chunk_size])


async def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                return f'The weather in {city} is {weather} with a temperature of {temp}'
            else:
                return 'Sorry, couldn\'t find the weather for that city.'
    
async def weather_command(update: Update, context: CallbackContext):
    '''Provides weather updates for city of choice. \n
To use, type /weather {city_name}.'''
    if context.args:
        city = ' '.join(context.args)
        weather_report = await get_weather(city)
        await update.message.reply_text(weather_report)
    else:
        await update.message.reply_text("Please provide a city name after the /weather command.")


reminder_list = [] #Reminder storage

async def reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''It is used to make reminders. \n
    To use, type /remind {message} {time}'''
    #Assigning the arguments
    message = ' '.join (context.args[:-1])
    time = context.args[-1]

    time = time.split(':')
    #Checking for validity of input
    if len(time) !=2:
        await update.message.reply_text('Please type the time in "HH:MM" format')
        return
    
    #Making the the time a datetime object
    try :
        reminder_time = datetime.datetime.now().replace(hour= int(time[0]), minute= int(time[1]), second= 0, microsecond= 0)
    except ValueError:
        await update.message.reply_text('Please type in valid values as your time.')
        return
    
    #Checking for validity of date
    now = datetime.datetime.now()
    if reminder_time < now:
        await update.message.reply_text('Please type in a time that is in the future')
        return
    
    #saving the reminder
    reminder = {'message': message, 'time':reminder_time}
    reminder_list.append(reminder)
    await update.message.reply_text('Reminder has been set')

    #Creating the job queue for the task
    context.application.job_queue.run_once(reminder_callback, when= (reminder_time - now).seconds, context= update.message.chat_id, name= str(reminder_time))

async def reminder_callback(context: CallbackContext):
    job = context.job
    await context.bot.send_message(chat_id=job.context, text="Reminder: " + job.name)
 


async def facts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''This function generates random facts. \n 
    To use, type /fact'''
    with open('facts.txt', 'r') as fact_file:
        facts_list = fact_file.readlines()
        facts_list = re.sub(r'[ ,]*$', '', facts_list)
    fact = random.choice(facts_list)
    await update.message.reply_text(fact)



async def calculator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''This function is used to evaluate mathematical expressions. \n
    To use, type /calculator {expression}'''
    try:
        expression = ''.join(context.args)
        # Validate the expression to contain only numbers and operators
        if not all(char.isdigit() or char in '+-*/.() ' for char in expression):
            await update.message.reply_text('Please use only numbers and operators (+, -, *, /, ., (, )).')
            return
        
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, {})
        await update.message.reply_text(f'The result is: {result}')
    except Exception as e:
        await update.message.reply_text(f'Error: {str(e)}')
       


task_list = []
async def tasks_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''This function is used to manage tasks. \n    
    To use, type /tasks {task} to add a task or /tasks list to list all tasks or /tasks done {task_number} to mark a task as done.'''
    string = ' '.join(context.args)
    if string == 'list':
        num = 1
        for task in task_list:
            await update.message.reply_text(f'{num} {task} \n')
            num += 1
    else:
        task_list.append(string)
        await update.message.reply_text(f'You have added the task: {string}')

async def done_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    task_number = int(context.args[0]) - 1
    if 0 <= task_number < len(task_list):
        removed_task = task_list.pop(task_number)
        await update.message.reply_text(f'Task "{removed_task}" marked as done and removed from the list.')
    else:
        await update.message.reply_text('Invalid task number. Please provide a valid task number.')



def response_handler(text: str):
    processed = text.lower()

    if 'hello' or 'hi' in processed:
        return 'Hey there, how are you doing today?'
    elif  'How are you' in processed:
        return 'I am good.'
    elif 'What are you' in processed:
        return 'I am simpomni bot, a multifunctional bot that can carry out useful tasks and boost your creativity.'
    else:
        return 'I don\'t know how to respond to what you sent.'



async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    message = update.message.text
    user = update.message.chat.id

    print(f'User {user} in {message_type}: {message}')

    if message_type == 'group':
        if BOTUSERNAME in message:
            new_message = message.replace(BOTUSERNAME,'').strip()
            response = response_handler(new_message)
        else:
            return
    else:
        response = response_handler(message)

    print(f'Bot, {response}')
    await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')




def main():
    print('Starting bot...') 

    application = Application.builder().token(TOKEN).build()
    #Commands
    application.add_handler(CommandHandler('start', start_command))

    application.add_handler(CommandHandler('help', help_command))

    application.add_handler(CommandHandler('weather', weather_command))

    application.add_handler(CommandHandler('remind', reminder_command))

    application.add_handler(CommandHandler('fact', facts_command))

    application.add_handler(CommandHandler('calculator', calculator_command))

    application.add_handler(CommandHandler('tasks', tasks_command))

    application.add_handler(CommandHandler('done', done_command))

    #Message
    application.add_handler(MessageHandler(filters.TEXT, message_handler))

    #Error
    application.add_error_handler(error)

    #Polling
    # Polling
    print('Polling...')
    application.run_polling()
    


if __name__ == "__main__":
    main()


