def command_log(ctx):
    print(
        f"| {str(ctx.message.author.name):^32} | {str(ctx.message.channel):^32} | {str(ctx.command):^32} |"
    )
