from typing import final
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Application, filters, ContextTypes, CallbackContext
import aiohttp,datetime, random, inspect
import os
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
        await update.message.reply_text(response)


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
 


async def facts_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''This function generates random facts. \n 
    To use, type /fact'''
    facts_list = ["Honey never spoils", "Bananas are berries, but strawberries aren’t", "Octopuses have three hearts",
        "The Eiffel Tower can be 15 cm taller during the summer", "The speed of light is approximately 299,792 kilometers per second",
        "Koalas sleep up to 22 hours a day", "A group of flamingos is called a flamboyance", 
        "The human body contains around 37.2 trillion cells", "The Amazon rainforest produces 20% of the world's oxygen", 
        "The shortest war in history lasted 38 to 45 minutes", "Sharks existed before trees", "Polar bear fur is actually transparent, not white", 
        "The longest hiccuping spree lasted 68 years", "An octopus has three hearts", "Venus is the hottest planet in the solar system", 
        "A day on Venus is longer than a year on Venus", "Slugs have four noses", "The first oranges weren’t orange", 
        "A group of crows is called a murder", "Wombat poop is cube-shaped", 
        "The longest-living mammal is the bowhead whale, which can live more than 200 years", "Hot water freezes faster than cold water", 
        "Humans share 60% of their DNA with bananas", "There are more stars in the universe than grains of sand on all the beaches on Earth", 
        "Ants can lift up to 50 times their body weight", "A blue whale’s tongue weighs as much as an elephant", 
        "Sea otters hold hands while they sleep to keep from drifting apart", "It rains diamonds on Jupiter and Saturn", 
        "The longest recorded flight of a chicken was 13 seconds", "Giraffes have the same number of neck vertebrae as humans", 
        "Butterflies can taste with their feet", "Mosquitoes are the deadliest animals on Earth", "Elephants are the only mammals that can’t jump", 
        "A sneeze travels at about 100 miles per hour", "The human nose can detect more than 1 trillion scents", 
        "Tigers have striped skin, not just striped fur", "The unicorn is the national animal of Scotland", 
        "The shortest commercial flight in the world lasts just 57 seconds", "A single strand of hair can support up to 100 grams in weight", 
        "The Great Wall of China is not visible from space with the naked eye", "Dolphins have names for each other", 
        "Penguins propose to their mates with a pebble", "Some turtles can breathe through their butts", 
        "There are more possible iterations of a game of chess than atoms in the known universe", "An ostrich’s eye is bigger than its brain", 
        "The word 'typewriter' can be typed using only the top row of a keyboard", "A jiffy is an actual unit of time, representing 1/100th of a second", 
        "The longest wedding veil was longer than 63 football fields", "Cats can’t taste sweetness", "The first computer was invented in the 1940s", 
        "A bolt of lightning contains enough energy to toast 100,000 slices of bread", "Dragonflies have been on Earth for over 300 million years", 
        "Alaska is the only state whose name is on one row on a keyboard", "A crocodile can’t stick its tongue out", "Bananas glow blue under black lights", 
        "The inventor of the microwave oven received $2 for his invention", "Kangaroos can’t walk backwards", "Humans are the only animals that blush", 
        "Some fish can recognize themselves in a mirror", "Mantis shrimp can punch with the force of a bullet", "The moon has moonquakes", 
        "There’s a basketball court on the top floor of the U.S. Supreme Court building", 
        "The scientific term for brain freeze is sphenopalatine ganglioneuralgia", 
        "The average person will spend six months of their life waiting for red lights to turn green", "A cloud can weigh more than a million pounds", 
        "Your body has more bacteria cells than human cells", "Humans are born with 300 bones but only have 206 by adulthood", 
        "Cows have best friends and get stressed when they are separated", "Owls don’t have eyeballs, they have eye tubes", 
        "There are more plastic flamingos in the U.S. than real flamingos", "Bubble wrap was originally invented as wallpaper", 
        "Pigeons can recognize human faces", "The Empire State Building has its own ZIP code", "A flea can accelerate faster than a space shuttle", 
        "The dot over the letter 'i' is called a tittle", "The world’s smallest mammal is the bumblebee bat", "Octopuses have blue blood", 
        "Peanuts are not nuts; they’re legumes", "Jellyfish have been around for more than 500 million years", "You can’t hum while holding your nose closed", 
        "A giraffe’s tongue is about 45 centimeters long", "The unicorn is the national animal of Scotland", 
        "The letter 'e' is the most common letter in the English language", "Carrots were originally purple", 
        "You can hear a blue whale’s heartbeat from more than 2 miles away", "Human thigh bones are stronger than concrete", 
        "A snail can sleep for three years", "The human body contains enough fat to make seven bars of soap", 
        "Sloths can hold their breath longer than dolphins can", "A jiffy is an actual unit of time", 
        "The longest word in the English language has 189,819 letters", "A flock of ravens is called an unkindness", 
        "The largest snowflake on record measured 15 inches across", "A bolt of lightning is five times hotter than the surface of the sun", 
        "The shortest war in history was between Britain and Zanzibar in 1896", "A day on Mercury is longer than its year", 
        "Sharks are the only fish that can blink with both eyes", "Your stomach gets a new lining every three to four days", "Gorillas can catch human colds", 
        "The heart of a blue whale is as big as a car", "The highest wave ever surfed was 80 feet", "Cows produce more milk when they listen to music", 
        "The first alarm clock could only ring at 4 a.m.", "A strawberry is not a berry, but a banana is", "Bees can recognize human faces", 
        "The longest recorded flight of a chicken is 13 seconds", "Tomatoes are the most popular fruit in the world", 
        "A small child could swim through the veins of a blue whale", "The average person walks the equivalent of five times around the world in their lifetime", 
        "It would take 1,200,000 mosquitoes, each sucking once, to completely drain the average human of blood", "Water makes different pouring sounds depending on its temperature", 
        "Human saliva contains a painkiller called opiorphin that is six times more powerful than morphine", "Spiders can’t fly but some can glide",
        "An eagle's nest can weigh up to two tons", "More people visit France than any other country", 
        "The tallest mountain in our solar system is on Mars and is three times the height of Mount Everest", 
        "You are more likely to be killed by a falling coconut than by a shark", "The tongue is the strongest muscle in the body relative to its size", 
        "Saturn’s rings are made of billions of ice and rock particles", "One in five people believe aliens are already living on Earth", 
        "There are more trees on Earth than stars in the Milky Way galaxy", 
        "The deepest part of the ocean is called the Mariana Trench and it’s deeper than Mount Everest is tall", 
        "The average person produces enough saliva in their lifetime to fill two swimming pools", "Some cats are allergic to humans", 
        "There are more possible iterations of a game of chess than atoms in the known universe", "Polar bears have black skin under their fur", 
        "The Statue of Liberty’s full name is Liberty Enlightening the World", "A crocodile’s brain weighs only 3 ounces", 
        "M&Ms were originally developed to allow soldiers to eat chocolate without it melting", "Antarctica is the largest desert in the world", 
        "An apple floats in water because it’s 25% air", "A chameleon’s tongue is twice the length of its body", "Squirrels can’t burp or vomit", 
        "Cleopatra lived closer in time to the moon landing than to the construction of the Great Pyramid", "Avocados are toxic to birds", 
        "Butterflies taste with their feet", "A cubic inch of human bone can bear the weight of five pickup trucks", "A group of jellyfish is called a smack", 
        "Humans are the only animals with chins", "Octopuses have nine brains", "Sharks can live for five centuries", "A flea can jump 350 times its body length", 
        "Some fish can walk on land", "Humans share 98% of their DNA with chimpanzees", "A rhinoceros’ horn is made of hair", 
        "The shortest commercial flight in the world is 1.7 miles long", "Lobsters have blue blood", "You can’t fold a paper in half more than seven times", 
        "Goats have rectangular pupils", "The unicorn is the national animal of Scotland", "Snakes can sense earthquakes", 
        "Lightning strikes about 8 million times a day", "An octopus has nine brains, three hearts, and blue blood", "Apples are made of 25% air, which is why they float", 
        "The speed of a computer mouse is measured in 'Mickeys'", "In Switzerland, it’s illegal to own just one guinea pig", 
        "The most shoplifted food item in the U.S. is cheese", "Cows can walk upstairs but not downstairs",
        "The creator of this bot is Matthew, if you like his bot, send him a message. This is his telegram username: @tbaaon_1"]

    fact = random.choice(facts_list)
    await update.message.reply_text(fact)



async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
async def tasks (update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def done(update : Update, context : ContextTypes.DEFAULT_TYPE):
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




async def main():
    print('Starting bot...') 

    application = Application.builder().token(TOKEN).build()
    #Commands
    application.add_handler(CommandHandler('start', start_command))

    application.add_handler(CommandHandler('help', help_command))

    application.add_handler(CommandHandler('weather', weather_command))

    application.add_handler(CommandHandler('remind', reminder_command))

    application.add_handler(CommandHandler('fact', facts_generator))

    application.add_handler(CommandHandler('calculator', calculator))

    application.add_handler(CommandHandler('tasks', tasks))

    application.add_handler(CommandHandler('done', done))

    #Message
    application.add_handler(MessageHandler(filters.TEXT, message_handler))

    #Error
    application.add_error_handler(error)

    #Polling
    print('Polling...')
    await application.start_polling()
    await application.run_polling(poll_interval=3)
    await application.idle()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


