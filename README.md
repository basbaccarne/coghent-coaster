# Coghent coaster
A self-updating coffee coaster that shows random museum collection items when you pick up your mug.

*By: Bas Baccarne & Ben Robaeyst*

## Status
* Prototyping subchallenges

## Components
* "fetch_unsplash.py" downloads a random Unsplash image
* "crop_image.py" takes an image from the program dir and crops & rescales it with a circular mask
* "coaster_withbutton.py" is the main script. When the coffee mug is lifted, a new image is shown
