"""
Module pour créer des icônes personnalisées avec des polygones colorés
en utilisant PIL et PyQt5.
"""

from math import cos, pi, sin
from PIL import Image, ImageDraw
from PyQt5.QtGui import QIcon, QPixmap


def draw_polygon(draw, n, radius, position, fill_color):
    """
    Dessine un polygone régulier avec `n` côtés.

    Paramètres :
        draw (ImageDraw.Draw) : L'objet de dessin PIL sur lequel le polygone
        sera dessiné.
        n (int) : Le nombre de côtés du polygone.
        radius (float) : Le rayon du polygone.
        position (tuple) : Les coordonnées (x, y) du centre du polygone.
        fill_color (str ou tuple) : La couleur de remplissage du polygone.
    """
    angle = pi * 2 / n
    points = [
        (position[0] + radius * sin(angle * i),
         position[1] + radius * cos(angle * i))
        for i in range(n)
    ]
    draw.polygon(points, fill=fill_color)


def create_icon_image(color='red'):
    """
    Crée une icône avec un polygone coloré et la retourne sous forme de QIcon.

    Paramètres :
        color (str ou tuple) :
        La couleur du polygone à dessiner. Par défaut 'red'.

    Retourne :
        QIcon : Une icône PyQt5 contenant l'image générée.
    """
    image = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(image)
    center = (32, 32)
    radius = 20
    draw_polygon(draw, 9, radius, center, fill_color=color)

    # Convertir l'image PIL en QIcon
    image = image.convert("RGBA")
    data = image.tobytes("raw", "RGBA")
    qimage = QPixmap()
    qimage.loadFromData(data)
    return QIcon(qimage)
