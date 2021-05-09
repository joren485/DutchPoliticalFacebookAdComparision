from datetime import date, timedelta
from typing import Tuple

from peewee import (
    CharField,
    DateField,
    FixedCharField,
    FloatField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

from constants import AGE_RANGES, FIRST_DATE, GENDERS, LOCAL_AD_ARCHIVE_PATH, REGIONS

database_handler = SqliteDatabase(LOCAL_AD_ARCHIVE_PATH)


class Ad(Model):
    """Model representing an Ad."""

    class Meta:
        """Meta class for Ad model."""

        database = database_handler

    ad_id = CharField()
    page_id = CharField()
    party = CharField()

    creation_date = DateField()
    start_date = DateField()
    end_date = DateField(null=True)

    creative_body = TextField(null=True)
    creative_link_caption = CharField(null=True)
    creative_link_description = TextField(null=True)
    creative_link_title = CharField(null=True)

    currency = FixedCharField(max_length=3)
    spending_lower = IntegerField()
    spending_upper = IntegerField()

    impressions_lower = IntegerField()
    impressions_upper = IntegerField()

    potential_reach_lower = IntegerField()
    potential_reach_upper = IntegerField()

    @property
    def days_active(self):
        """Return the amount of days this ad is/was active."""
        end_date = self.end_date or date.today()
        return 1 + (end_date - self.start_date).days

    @property
    def has_potential_reach(self):
        """Return whether potential reach data is available for this ad."""
        return self.potential_reach_lower is not None

    @property
    def spending_average(self):
        """Return the average of the spending range given for this ad."""
        return (self.spending_lower + self.spending_upper) / 2

    @property
    def impressions_average(self):
        """Return the average of the impressions range given for this ad."""
        return (self.impressions_lower + self.impressions_upper) / 2

    @property
    def average_potential_reach(self):
        """Return the average of the potential reach range given for this ad."""
        return (self.potential_reach_lower + self.potential_reach_upper) / 2

    @property
    def average_spending_per_day(self):
        """Return the average spending for every day this ad is/was active."""
        return self.spending_average / self.days_active

    @property
    def average_impressions_per_day(self):
        """Return the average impressions for every day this ad is/was active."""
        return self.impressions_average / self.days_active

    @property
    def average_potential_reach_per_day(self) -> float:
        """Return the average potential reach for every day this ad is/was active."""
        return self.average_potential_reach / self.days_active

    def dates_active(self) -> Tuple[int, date]:
        """Yield dates and indexes that this ad is/was active."""
        start_date_index = (self.start_date - FIRST_DATE).days
        for date_offset in range(self.days_active):
            yield (
                start_date_index + date_offset,
                self.start_date + timedelta(days=date_offset),
            )

    @staticmethod
    def distribution_type_to_field_name(distribution_type: str) -> str:
        """
        Map distribution types (male or 65+) to field names of the Ad model.

        :param distribution_type: A string (e.g. male or 65+).
        :return: A field name.
        """
        slug = distribution_type.lower().replace("-", "_").replace("+", "")
        if distribution_type in GENDERS:
            return f"gender_distribution_{slug}"
        elif distribution_type in AGE_RANGES:
            return f"age_distribution_{slug}"
        elif distribution_type in REGIONS:
            return f"region_distribution_{slug}"

        raise ValueError(f"Unknown type: {distribution_type}")


for dt in GENDERS + REGIONS + AGE_RANGES:
    Ad._meta.add_field(Ad.distribution_type_to_field_name(dt), FloatField(default=0))

database_handler.create_tables([Ad])
