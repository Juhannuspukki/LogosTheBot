# timer functions
def alarm1(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text='One minute has passed.')


def alarm2(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text='One minute remaining.')


def alarm3(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text="Time's up!")


def set(bot, update, args, job_queue, chat_data):
    """Adds a job to the queue"""

    chat_id = update.message.chat_id
    if 'job' in chat_data:
        update.message.reply_text('You already have an active timer.')
        return

    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry, we can not go back to future!')
            return

        job = job_queue.run_once(alarm3, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        job = job_queue.run_once(alarm1, 60, context=chat_id)
        chat_data['debate1'] = job
        job = job_queue.run_once(alarm2, 360, context=chat_id)
        chat_data['debate2'] = job
        job = job_queue.run_once(alarm3, 420, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Default value set: 7 minutes.')


def unset(bot, update, chat_data):
    """Removes the job if the user changed their mind"""

    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer.')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    try:
        job = chat_data['debate1']
        job.schedule_removal()
        del chat_data['debate1']

        job = chat_data['debate2']
        job.schedule_removal()
        del chat_data['debate2']
    except ValueError:
        pass

    update.message.reply_text('Timer successfully unset!')
