# Elyabot
Telegram bot to fetch coin price data from crypto exchanges

Written on python

Tested OS: Ubuntu 16.04 LTS

## How To install:

In commandline, run:
```
curl -L https://github.com/streamtv85/elyabot/raw/master/install.sh | bash
```

#### Edit config file:

Go to `/usr/local/bin/bot-service/elyabot/config.ini`
and put your bot's token at `token=` line

## How to run:
#### In console mode so it is writing messages to the stdout:
```
/usr/local/bin/bot-service/run.sh
```

#### In detached mode using 'screen'
```
screen -S bot -d -m /usr/local/bin/bot-service/run.sh
```

### To autostart the bot on reboot:
```
crontab -e
```
then add line:
```
@reboot ( sleep 90 ; screen -S bot -d -m /usr/local/bin/bot-service/run.sh )
```

or, in commandline:
```
echo @reboot ( sleep 90 ; screen -S bot -d -m /usr/local/bin/bot-service/run.sh ) > crontab-fragment.txt
crontab -l | cat - crontab-fragment.txt >crontab.txt && crontab crontab.txt
```

### Working with screen sessions:

to attach to the session:
```
screen -x bot
```
to detach: press `Ctrl-A D`

to stop the bot:
either
```
pkill screen
```
or
```
screen -XS bot quit
```

Log file is located at
```
/usr/local/bin/bot-service/elyabot/bot-service.log
```

you can monitor the output with
```
tail -f /usr/local/bin/bot-service/elyabot/bot-service.log
```
## Update the bot to the current version from GitHub:

either:
```
/usr/local/bin/bot-service/update.sh
```
or (better)
```
curl -L https://github.com/streamtv85/elyabot/raw/master/update.sh | bash
```

OR you can update the bot with Telegram command /update
for this to work,
make sure that the user you are running the bot with does have permissions to run sudo commands without password prompt!
How to enable this:
```
sudo adduser <username> sudo
sudo visudo
```
In the editor, append following line
```
<username> ALL=(ALL) NOPASSWD:ALL
```
And save your changes

## Telegram commands:

```
price - Get current ELYA/BTC prices
```
