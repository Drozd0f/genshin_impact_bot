from io import BytesIO

import pyocr
import pytesseract
import requests
from discord.ext import commands
from pyocr import builders
from PIL import Image, ImageFilter, ImageDraw

bot = commands.Bot(command_prefix='!')
TOKEN = os.environ['TOKEN']
BLACK_COLOR = 0
WHITE_COLOR = 255


@bot.command()
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')


@bot.command()
async def rate(ctx: commands.Context):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        await ctx.send(
            content='Нету изображения',
            reference=ctx.message
        )
        return None
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    # gray = image.convert('L')
    image = image.filter(ImageFilter.DETAIL)
    # width = gray.size[0]
    # height = gray.size[1] // 100
    image.save('text.png')

    tools = pyocr.get_available_tools()
    tool = tools[0]

    text = tool.image_to_string(
        image=image,
        lang='rus',
        builder=builders.TextBuilder()
    )

    # text = pytesseract.image_to_string(gray, lang='rus')

    await ctx.send(
        content=text,
        reference=ctx.message
    )


if __name__ == '__main__':
    bot.run(TOKEN)
