from datetime import datetime

from constants import DATETIME_FORMAT, FIRST_DATE, CURRENCY_TO_EUR_MAP, GENDERS, AGE_GROUPS, REGIONS


class Ad:
    def __init__(self, party, ad_data):
        self.start_date = datetime.strptime(ad_data["ad_delivery_start_time"], DATETIME_FORMAT)
        if self.start_date < FIRST_DATE:
            raise ValueError

        if "ad_delivery_stop_time" in ad_data:
            self.end_date = datetime.strptime(ad_data["ad_delivery_stop_time"], DATETIME_FORMAT)
        else:
            self.end_date = datetime.today()
        self.active_days = (self.end_date - self.start_date).days + 1

        self.id = ad_data["id"]
        self.party = party

        self.impressions_lower, self.impressions_average, self.impressions_upper = Ad._parse_estimated_value(
            ad_data["impressions"]
        )

        self.spending_lower, self.spending_average, self.spending_upper = Ad._parse_estimated_value(
            ad_data["spend"], lambda x: x * CURRENCY_TO_EUR_MAP[ad_data["currency"]]
        )
        self.spending_average_per_day = self.spending_average / self.active_days

        self.has_potential_reach = "potential_reach" in ad_data.keys()
        if self.has_potential_reach:
            (
                self.potential_reach_lower,
                self.potential_reach_average,
                self.potential_reach_upper,
            ) = Ad._parse_estimated_value(ad_data["potential_reach"])

        self.gender_distribution, self.age_distribution = self._parse_demographic_distribution(
            ad_data["demographic_distribution"]
        )

        self.region_distribution = self._parse_region_distribution(ad_data["region_distribution"])

    def __str__(self):
        return f"{self.party} on {self.start_date.strftime(DATETIME_FORMAT)}"

    @staticmethod
    def max_expensive(ad1, ad2):
        if ad1 is None and ad2 is None:
            return None
        elif ad1 is None:
            return ad2
        elif ad2 is None:
            return ad1
        elif ad1.spending_average / ad1.active_days >= ad2.spending_average / ad2.active_days:
            return ad1
        return ad2

    @staticmethod
    def _parse_estimated_value(data, f=lambda x: x):
        lower = f(int(data["lower_bound"]))
        upper = f(int(data["upper_bound"])) if "upper_bound" in data else lower
        average = (lower + upper) / 2
        return lower, average, upper

    @staticmethod
    def _parse_demographic_distribution(demographic_distribution_data):

        gender_distribution = {g: 0 for g in GENDERS}
        age_distribution = {a: 0 for a in AGE_GROUPS}

        for demographic_group in demographic_distribution_data:
            percentage = float(demographic_group["percentage"])
            gender = demographic_group["gender"]
            age_group = demographic_group["age"]

            if gender in GENDERS:
                gender_distribution[gender] += percentage

            if age_group in AGE_GROUPS:
                age_distribution[age_group] += percentage

        return gender_distribution, age_distribution

    @staticmethod
    def _parse_region_distribution(region_distribution_data):
        region_distribution = {r: 0 for r in REGIONS}

        for region_group in region_distribution_data:
            region = region_group["region"]

            if region in REGIONS:
                region_distribution[region] += float(region_group["percentage"])

        return region_distribution

    @staticmethod
    def parse_ads(ads_data, id_to_party_map, statistics):
        for ad_data in ads_data:
            try:
                ad = Ad(id_to_party_map[ad_data["page_id"]], ad_data)
            except ValueError:
                pass
            else:
                statistics.ads_total += 1
                statistics.ads_without_potential_reach += 0 if ad.has_potential_reach else 1

                statistics.spending_total += ad.spending_average
                statistics.spending_total_lower += ad.spending_lower
                statistics.spending_total_upper += ad.spending_upper
                statistics.most_expensive_ad = Ad.max_expensive(statistics.most_expensive_ad, ad)

                statistics.ads_per_party[ad.party] += 1
                statistics.spending_per_party[ad.party] += ad.spending_average
                statistics.impressions_per_party[ad.party] += ad.impressions_average

                for region in REGIONS:
                    statistics.spending_per_party_per_region[ad.party][region] += (
                        ad.region_distribution[region] * ad.spending_average
                    )
                    statistics.impressions_per_party_per_region[ad.party][region] += (
                        ad.region_distribution[region] * ad.impressions_average
                    )

                for gender in GENDERS:
                    statistics.spending_per_party_per_gender[ad.party][gender] += (
                        ad.gender_distribution[gender] * ad.spending_average
                    )
                    statistics.impressions_per_party_per_gender[ad.party][gender] += (
                        ad.gender_distribution[gender] * ad.impressions_average
                    )

                for age_group in AGE_GROUPS:
                    statistics.spending_per_party_per_age[ad.party][age_group] += (
                        ad.age_distribution[age_group] * ad.spending_average
                    )
                    statistics.impressions_per_party_per_age[ad.party][age_group] += (
                        ad.age_distribution[age_group] * ad.impressions_average
                    )

                date_index_first_day = (ad.start_date - FIRST_DATE).days
                for date_index_offset in range(ad.active_days):
                    date_index = date_index_first_day + date_index_offset

                    statistics.ads_per_party_per_date[ad.party][date_index] += 1
                    statistics.spending_per_party_per_date[ad.party][date_index] += ad.spending_average / ad.active_days
                    statistics.impressions_per_party_per_date[ad.party][date_index] += (
                        ad.impressions_average / ad.active_days
                    )

                    if ad.has_potential_reach:
                        statistics.potential_reach_per_party_per_date[ad.party][date_index] += (
                            ad.potential_reach_average / ad.active_days
                        )

                    for region in REGIONS:
                        statistics.spending_per_party_per_region_per_date[ad.party][region][date_index] += (
                            ad.region_distribution[region] * ad.spending_average / ad.active_days
                        )
                        statistics.impressions_per_party_per_region_per_date[ad.party][region][date_index] += (
                            ad.region_distribution[region] * ad.impressions_average / ad.active_days
                        )

                    for gender in GENDERS:
                        statistics.spending_per_party_per_gender_per_date[ad.party][gender][date_index] += (
                            ad.gender_distribution[gender] * ad.spending_average / ad.active_days
                        )
                        statistics.impressions_per_party_per_gender_per_date[ad.party][gender][date_index] += (
                            ad.gender_distribution[gender] * ad.impressions_average / ad.active_days
                        )

                    for age_group in AGE_GROUPS:
                        statistics.spending_per_party_per_age_per_date[ad.party][age_group][date_index] += (
                            ad.age_distribution[age_group] * ad.spending_average / ad.active_days
                        )
                        statistics.impressions_per_party_per_age_per_date[ad.party][age_group][date_index] += (
                            ad.age_distribution[age_group] * ad.impressions_average / ad.active_days
                        )
