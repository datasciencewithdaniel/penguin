from unicodedata import lookup


def command_log(ctx):
    print(
        f"| {str(ctx.message.author.name):^32} | {str(ctx.message.channel):^32} | {str(ctx.command):^32} |"
    )


def role_log(user, emoji, channel, role, action):
    print(
        f"""| {str(user.name):^32} | {str(channel):^32} | {str(f'{emoji} - {role} - {action.split("_")[-1]}'):^32}|"""
    )


def find_emoji(name):
    return lookup(name.replace("_", " "))
