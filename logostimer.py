from telegram.ext import Job

timers = {}


def setalarmhelper(bot, update, alarm, due, chat_id, job_queue):
    job = Job(alarm, due, repeat=False, context=chat_id)

    timers[chat_id] = job
    job_queue.put(job)


# timer functions
def alarm1(bot, job):
    """Function to send the alarm message"""
    if job.context in timers.keys():
        bot.sendMessage(job.context, text='One minute has passed. Questions may now be asked.')


def alarm2(bot, job):
    """Function to send the alarm message"""
    if job.context in timers.keys():
        bot.sendMessage(job.context, text='One minute remaining. No more questions allowed.')


def alarm3(bot, job):
    """Function to send the alarm message"""
    if job.context in timers.keys():
        bot.sendMessage(job.context, text="Time's up!")


def set(bot, update, args, job_queue):
    """Adds a job to the queue"""

    chat_id = update.message.chat_id
    if chat_id in timers:
        update.message.reply_text('You already have an active timer.')
        return

    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry, we can not go back to future!')
            return

        setalarmhelper(bot, update, alarm3, due, chat_id, job_queue)

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Default value set: 7 minutes.')

        setalarmhelper(bot, update, alarm1, 60, chat_id, job_queue)
        setalarmhelper(bot, update, alarm2, 360, chat_id, job_queue)
        setalarmhelper(bot, update, alarm3, 420, chat_id, job_queue)


def unset(bot, update):
    """Removes the job if the user changed their mind"""
    chat_id = update.message.chat_id

    if chat_id not in timers:
        update.message.reply_text('You have no active timer.')
        return

    job = timers[chat_id]
    job.schedule_removal()
    del timers[chat_id]
    update.message.reply_text('Timer successfully unset!')