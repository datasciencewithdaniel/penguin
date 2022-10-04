# Penguin

Penguin is a Discord Bot build for the Data Science with Daniel Discord Server.

Current functionality:

- Message Replies (responses)
- Reaction Roles (roles)
- Welcome Message (notifications)
- Tutoring Support (tutoring)
- Suggestions (suggestions)

Future Functionality:

- Twitch Stream Notification (background)

## Admin

To run a local version of the bot:

```
make run DISCORD_TOKEN=<DISCORD_TOKEN> GUILD_NAME="<GUILD_NAME>" AWS_ACCOUNT_DSWD=<DSWD_ACCOUNT_NUMBER>
make run-baby DISCORD_TOKEN=<DISCORD_TOKEN> GUILD_NAME="<GUILD_NAME>" AWS_ACCOUNT_DSWD=<DSWD_ACCOUNT_NUMBER>
```

## To Find and Kill the Process

```
sudo ps -U ubuntu
kill [PID]
```
