# Run a script that takes an image from the program dir and crops & rescales it with a circular mask
# Note: Pillow module needs to be installed (https://pillow.readthedocs.io/)

from PIL import Image, ImageOps, ImageTk, ImageDraw


def fix_image(image="image.jpg"):
    # set dimensions
    width = 320
    height = 240

    # generate circular mask
    size = (height, height)
    mask = Image.new('L', size, 255)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=0)

    img = Image.open(image)
    output = ImageOps.fit(img,
                          mask.size,
                          centering=(0.5, 0.5))
    output.paste(0, mask=mask)
    output.convert('P', palette=Image.ADAPTIVE)
    output.save("image_cropped.jpg", transparency=0)
    print("Image cropped at " + str(width) + " x " + str(height) + " pixels and stored as image_cropped.jpg")


fix_image()
