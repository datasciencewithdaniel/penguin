from unicodedata import lookup


def command_log(ctx, logger):
    text = f"| {str(ctx.message.author.name):^32} | {str(ctx.message.channel):^32} | {str(ctx.command):^32} |"
    print(text)
    logger.info(text)


def role_log(user, emoji, channel, role, action, logger):
    text = f"""| {str(user.name):^32} | {str(channel):^32} | {str(f'{emoji} - {role} - {action.split("_")[-1]}'):^32}|"""
    print(text)
    logger.info(text)


def find_emoji(name):
    return lookup(name.replace("_", " "))


# def get_user_mention(username):
#     return username
