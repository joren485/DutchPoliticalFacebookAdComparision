from functools import cached_property

from enum import Flag, auto


class Theme(Flag):
    """Enum implementing themes."""

    NONE = 0

    AGRICULTURE = auto()
    CIVIL_RIGHTS = auto()
    CLIMATE = auto()
    DEFENSE = auto()
    ECONOMY = auto()
    EDUCATION_CULTURE = auto()
    FOREIGN_AFFAIRS = auto()
    GOVERNMENT = auto()
    HEALTHCARE = auto()
    HOUSING = auto()
    LAW_ORDER = auto()
    MIGRATION = auto()
    SOCIAL_WELFARE = auto()
    TRANSPORTATION = auto()

    @classmethod
    def all(cls):
        """Return a list of themes."""
        return [t for t in cls if t != Theme.NONE]

    @property
    def title(self):
        """Return the name of a theme in a format that can be used in a title."""
        if self == Theme.EDUCATION_CULTURE:
            return "Education & Culture"

        elif self == Theme.LAW_ORDER:
            return "Law & Order"

        slug = self.name.title().replace("_", " ")
        return slug

    @classmethod
    def titles(cls):
        """Return list of title properties."""
        return [t.title for t in cls.all()]

    @cached_property
    def wordlist(self):
        """Return the (cached) wordlist corresponding to the theme."""
        filename = self.name.lower()
        path = f"../data/wordlists/{filename}"

        with open(path) as h_file:
            return [line.strip() for line in h_file if line.strip()]

    @classmethod
    def intersections(cls, words):
        """Calculate the amount of common words between a given list and every theme."""
        return {t: sum(1 for word in words if word in t.wordlist) for t in cls if t != Theme.NONE}
