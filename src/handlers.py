import io
import logging

import discord
import numpy as np
import requests
import pytesseract
from cv2 import cv2
from PIL import Image
from discord.ext import commands


@commands.command()
async def ping(ctx: commands.context.Context):
    await ctx.send('pong')


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(
        np.asarray(image),
        cv2.MORPH_OPEN,
        kernel
    )


def new_opening(image):
    im2 = image.copy()

    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    res = ''

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(
            cropped
        )

        res += f'{text}\n'

    return res


def canny(image):
    return cv2.Canny(image, 100, 200)


def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


@commands.command()
async def rate(ctx: commands.Context):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        await ctx.send(
            content='Нету изображения',
            reference=ctx.message
        )
        return

    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    image = np.asarray(image)

    # image = opening(image)
    #
    # text = pytesseract.image_to_string(
    #     image,
    #     config=r'--oem 3 --psm 12',
    #     lang='rus'
    # )
    #
    # cv2.imwrite('res.png', image)

    await ctx.send(
        content=new_opening(image),
        delete_after=30.0,
        reference=ctx.message
    )
