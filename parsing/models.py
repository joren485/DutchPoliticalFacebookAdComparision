import re
import typing
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
    LAST_DATE,
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

    audience_size_lower = IntegerField()
    audience_size_upper = IntegerField()

    @classmethod
    def ads_in_time_range(cls, first_date=FIRST_DATE, last_date=LAST_DATE):
        """
        Return a query that contains all ads that were active in a certain time period (i.e. between first_date and last_date).

        Ads that are considered active between first_date and last_date meet at least one of the following constraints:
        - The start_date falls between first_date and last_date.
        - The end_end falls between first_date and last_date.
        """
        return Ad.select().where(
            (first_date <= Ad.start_date) & (Ad.start_date <= last_date)
            | (first_date <= Ad.end_date) & (Ad.end_date <= last_date)
        )

    @cached_property
    def days_active(self) -> int:
        """
        Return the amount of days this ad is/was active.

        This does not take FIRST_DATE and LAST_DATE into account.
        """
        if self.end_date is None:
            end_date = date.today()
        else:
            end_date = self.end_date

        return 1 + (end_date - self.start_date).days

    @cached_property
    def has_audience_size(self) -> bool:
        """Return whether estimated audience size data is available for this ad."""
        return self.audience_size_lower > 0

    @cached_property
    def average_spending(self) -> float:
        """Return the average of the spending range given for this ad."""
        return (self.spending_lower + self.spending_upper) / 2

    @cached_property
    def average_impressions(self) -> float:
        """Return the average of the impressions range given for this ad."""
        return (self.impressions_lower + self.impressions_upper) / 2

    @cached_property
    def average_audience_size(self) -> float:
        """Return the average of the estimated audience size range given for this ad."""
        return (self.audience_size_lower + self.audience_size_upper) / 2

    @cached_property
    def average_spending_per_day(self) -> float:
        """Return the average spending for every day this ad is/was active."""
        return self.average_spending / self.days_active

    @cached_property
    def average_impressions_per_day(self) -> float:
        """Return the average impressions for every day this ad is/was active."""
        return self.average_impressions / self.days_active

    @cached_property
    def average_audience_size_per_day(self) -> float:
        """Return the average estimated audience size for every day this ad is/was active."""
        return self.average_audience_size / self.days_active

    def active_date_indices(
        self, time_range_start_date=FIRST_DATE, time_range_end_date=LAST_DATE
    ) -> typing.Generator[int, None, None]:
        """Yield the indices of dates that this ad was active during a time range."""
        ad_end_date = self.end_date or date.today()
        if (time_range_start_date <= self.start_date <= time_range_end_date) or (
            time_range_start_date <= ad_end_date <= time_range_end_date
        ):

            if self.start_date < time_range_start_date:
                ad_start_date = time_range_start_date
            else:
                ad_start_date = self.start_date

            if ad_end_date > time_range_end_date:
                ad_end_date = time_range_end_date

            days_active_in_range = 1 + (ad_end_date - ad_start_date).days
            start_date_index = (ad_start_date - time_range_start_date).days
            for date_offset in range(days_active_in_range):
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

    def rank_to_data(
        self, data_type: str, demographic: str, per_day: bool = False
    ) -> float:
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

        elif data_type == "estimated-audience-size" and per_day:
            amount = self.average_audience_size_per_day
        elif data_type == "estimated-audience-size" and not per_day:
            amount = self.average_audience_size

        else:
            raise ValueError(f"Unknown data type: {data_type}")

        if demographic == "total":
            return amount

        return amount * getattr(self, Ad.demographic_to_field_name(demographic))


for dt in GENDERS + REGIONS + AGE_RANGES:
    Ad._meta.add_field(Ad.demographic_to_field_name(dt), FloatField(default=0))

database_handler.create_tables([Ad])
