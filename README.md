# israel_covid_child_form_sender
A bot for Telegram that sends child health form to Israel ministry of health

# How to deploy with docker-compose:  
```
child-report-bot:
  image: benyomin/health-report-bot:latest
  environment:
    BOT_TOKEN: {YOR TELEGRAM BOT TOKEN}
  volumes:
    - "{PATH TO YOUR config.yml}:/home/app/config.yaml"```
    
Don't forget to fill config.yaml!
