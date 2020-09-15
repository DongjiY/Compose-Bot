
import discord
from datetime import date
client = discord.Client()

whiteList = ['bmp','jpeg','jpg','png']

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name ="Fiddle Faddle"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "http" in message.content:
        print(" ^This is a link, do not run")
        return

    #this gets the current day instead of relying on user input
    today = date.today()
    dateLine = today.strftime("%d %B %Y")

    sender = str(message.author)
    print(sender+" has sent a message for conversion")

    if len(message.content) != 0:
        while True:
            try:
                messageInput = str(message.content)
                await message.delete()
                inputLines = messageInput.split('\n')
                msgLines = messageInput[len(inputLines[0])+len(inputLines[1])+1:]
                #print(inputLines[0])
                #print(inputLines[1])
                await message.channel.send("**"+inputLines[0]+"**"+'\n'+"*"+dateLine.strip()+"*"+'\n'+"```"+msgLines+"```")
                await message.channel.send("-"+sender[:-5])
            except:
                break
    else:
        #reading in inputs from attachments

        if message.attachments[0].filename.split('.')[-1] in whiteList:
            print(" ^This is a photo, do not run")
            return

        thisAttachment = message.attachments[0]
        temp = await thisAttachment.read()
        textInput = temp.decode("utf-8")
        #print(textInput)
        await message.delete()
        #breaking into paragraphs and isolating the title and date
        lineBreaks = textInput.split('\n')
        #print("lnbrk1",lineBreaks)
        await message.channel.send("**"+lineBreaks[0][:-1]+"**"+'\n'+"*"+dateLine.strip()+"*")
        for x in range(len(lineBreaks)):
            lineBreaks[x] = lineBreaks[x][:-1]
        if lineBreaks[-1] == '':
            del lineBreaks[-1]
        #print("lnbrks",lineBreaks)
        #print(len(lineBreaks))
        #breaking up the words to fit under 2000 chars
        #setting up variables
        outputString = ""
        for x in range(2,len(lineBreaks)):

            remainderCase = True

            sentences = lineBreaks[x].split('.')
            if sentences[-1] == ' ' or sentences[-1] == '':
                del sentences[-1]

            while remainderCase:
                remainderCase = False
                count = 1
                #print(sentences)

                if len(outputString) + len(lineBreaks[x]) + 6 > 1994 and x>2:
                    await message.channel.send("```"+outputString.strip()+"```")
                    outputString = remainder

                if x>2 and len(outputString) > 0:
                    outputString += '\n'

                while (count <= len(sentences)) and (len(outputString)+len(sentences[count-1])+1 < 1994):
                    outputString += sentences[count-1] + "."
                    count += 1

                if count != len(sentences):
                    remainderLength = len(".".join(sentences[count-1:]))
                    if remainderLength > 1994:
                        await message.channel.send("```"+outputString.strip()+"```")
                        remainderCase = True
                        sentences = sentences[count-1:]
                        outputString = ""
                    else:
                        remainder = ".".join(sentences[count-1:])
                    #print("REMAINDER:",remainder)
                else:
                    remainder = ""
                #print(x,outputString)

        await message.channel.send("```"+outputString.strip()+"```")
        if remainder != "":
            await message.channel.send("```"+remainder.strip()+"```")
        await message.channel.send("-"+sender[:-5])


client.run('xxxxxxx')
