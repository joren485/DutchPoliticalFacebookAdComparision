import re
from datetime import date
from functools import cached_property

from peewee import (
    CharField,
    DateField,
    FloatField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

from constants import (
    AGE_RANGES,
    FIRST_DATE,
    GENDERS,
    LOCAL_AD_ARCHIVE_PATH,
    REGIONS,
)

PATTERN_NON_WORD_CHARS = re.compile(r"[^a-zA-Z0-9-' #]")

database_handler = SqliteDatabase(LOCAL_AD_ARCHIVE_PATH)


class Ad(Model):
    """Model representing an Ad."""

    class Meta:
        """Meta class for Ad model."""

        database = database_handler

    ad_id = CharField(unique=True)
    page_id = CharField()
    party = CharField()

    themes = IntegerField()

    creation_date = DateField()
    start_date = DateField()
    end_date = DateField(null=True)

    creative_bodies = TextField()
    creative_link_captions = CharField()
    creative_link_descriptions = TextField()
    creative_link_titles = CharField()

    spending_lower = IntegerField()
    spending_upper = IntegerField()

    impressions_lower = IntegerField()
    impressions_upper = IntegerField()

    potential_reach_lower = IntegerField()
    potential_reach_upper = IntegerField()

    @cached_property
    def days_active(self) -> int:
        """Return the amount of days this ad is/was active."""
        end_date = self.end_date or date.today()
        return 1 + (end_date - self.start_date).days

    @cached_property
    def has_potential_reach(self) -> bool:
        """Return whether potential reach data is available for this ad."""
        return self.potential_reach_lower > 0

    @cached_property
    def average_spending(self) -> float:
        """Return the average of the spending range given for this ad."""
        return (self.spending_lower + self.spending_upper) / 2

    @cached_property
    def average_impressions(self) -> float:
        """Return the average of the impressions range given for this ad."""
        return (self.impressions_lower + self.impressions_upper) / 2

    @cached_property
    def average_potential_reach(self) -> float:
        """Return the average of the potential reach range given for this ad."""
        return (self.potential_reach_lower + self.potential_reach_upper) / 2

    @cached_property
    def average_spending_per_day(self) -> float:
        """Return the average spending for every day this ad is/was active."""
        return self.average_spending / self.days_active

    @cached_property
    def average_impressions_per_day(self) -> float:
        """Return the average impressions for every day this ad is/was active."""
        return self.average_impressions / self.days_active

    @cached_property
    def average_potential_reach_per_day(self) -> float:
        """Return the average potential reach for every day this ad is/was active."""
        return self.average_potential_reach / self.days_active

    def active_date_indices(self) -> int:
        """Yield dates and indexes that this ad is/was active."""
        start_date_index = (self.start_date - FIRST_DATE).days
        for date_offset in range(self.days_active):
            yield start_date_index + date_offset

    @staticmethod
    def demographic_to_field_name(demographic: str) -> str:
        """
        Map demographics (e.g. male or 65+) to field names of the Ad model.

        :param demographic: A string (e.g. male or 65+).
        :return: A field name.
        """
        slug = demographic.lower().replace("-", "_").replace("+", "")
        if demographic in GENDERS:
            return f"gender_demographic_{slug}"
        elif demographic in AGE_RANGES:
            return f"age_demographic_{slug}"
        elif demographic in REGIONS:
            return f"region_demographic_{slug}"

        raise ValueError(f"Unknown type: {demographic}")

    def rank_to_data(self, data_type: str, demographic: str, per_day: bool = False):
        """Return the amount of data type per demographic for this ad."""
        if data_type == "number-of-ads":
            return 1

        elif data_type == "spending" and per_day:
            amount = self.average_spending_per_day
        elif data_type == "spending" and not per_day:
            amount = self.average_spending

        elif data_type == "impressions" and per_day:
            amount = self.average_impressions_per_day
        elif data_type == "impressions" and not per_day:
            amount = self.average_impressions

        elif data_type == "potential-reach" and per_day:
            amount = self.average_potential_reach_per_day
        elif data_type == "potential-reach" and not per_day:
            amount = self.average_potential_reach

        else:
            raise ValueError(f"Unknown data type: {data_type}")

        if demographic == "total":
            return amount

        return amount * getattr(self, Ad.demographic_to_field_name(demographic))


for dt in GENDERS + REGIONS + AGE_RANGES:
    Ad._meta.add_field(Ad.demographic_to_field_name(dt), FloatField(default=0))

database_handler.create_tables([Ad])
