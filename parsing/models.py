from datetime import date, timedelta

from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    TextField,
    DateField,
    FixedCharField,
    IntegerField,
    FloatField,
)

from constants import LOCAL_AD_ARCHIVE_PATH, FIRST_DATE, GENDERS, REGIONS, AGE_RANGES

database_handler = SqliteDatabase(LOCAL_AD_ARCHIVE_PATH)


class Ad(Model):
    class Meta:
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
        end_date = self.end_date or date.today()
        return 1 + (end_date - self.start_date).days

    @property
    def spending_average(self):
        return (self.spending_lower + self.spending_upper) / 2

    @property
    def impressions_average(self):
        return (self.impressions_lower + self.impressions_upper) / 2

    @property
    def average_potential_reach(self):
        return (self.potential_reach_lower + self.potential_reach_upper) / 2

    @property
    def average_spending_per_day(self):
        return self.spending_average / self.days_active

    @property
    def average_impressions_per_day(self):
        return self.impressions_average / self.days_active

    @property
    def average_potential_reach_per_day(self):
        return self.average_potential_reach / self.days_active

    def dates_active(self):
        start_date_index = (self.start_date - FIRST_DATE).days
        for date_offset in range(self.days_active):
            yield (
                start_date_index + date_offset,
                self.start_date + timedelta(days=date_offset),
            )

    @staticmethod
    def distribution_type_to_field_name(distribution_type: str):
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
