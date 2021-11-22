from functools import cached_property

from enum import Flag, auto


class Theme(Flag):
    """Enum implementing themes."""

    NONE = 0

    BUITENLANDSE_ZAKEN = auto()
    BURGERRECHTEN = auto()
    DEFENSIE = auto()
    ECONOMIE = auto()
    GEZONDHEIDSZORG = auto()
    HUISVESTING = auto()
    JUSTITIE = auto()
    KLIMAAT = auto()
    LANDBOUW = auto()
    MIGRATIE = auto()
    ONDERWIJS_CULTUUR = auto()
    OVERHEID = auto()
    SOCIALE_ZAKEN = auto()
    TRANSPORT = auto()

    @classmethod
    def all(cls):
        return [t for t in cls if t != Theme.NONE]

    @property
    def slug(self):
        if self == Theme.ONDERWIJS_CULTUUR:
            return "Onderwijs & Cultuur"

        slug = self.name.title().replace("_", " ")
        return slug

    @classmethod
    def slugs(cls):
        return [t.slug for t in cls.all()]

    @cached_property
    def wordlist(self):
        """Return the (cached) wordlist corresponding to the theme."""
        filename = self.name.lower().replace("_", " ")
        path = f"../data/wordlists/{filename}"

        with open(path) as h_file:
            return [line.strip() for line in h_file if line.strip()]

    @classmethod
    def intersections(cls, words):
        """Calculate the amount of common words between a given list and every theme."""
        return {
            t: sum(1 for word in words if word in t.wordlist)
            for t in cls
            if t != Theme.NONE
        }
