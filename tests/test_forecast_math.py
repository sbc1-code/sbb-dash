import unittest

import scraper_v2 as forecast


def make_day(day_of_week):
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {
        "date": "2026-06-06",
        "day_name": names[day_of_week],
        "day_short": names[day_of_week][:3].upper(),
        "day_of_week": day_of_week,
        "is_weekend": day_of_week >= 5,
        "month_day": "06/06",
    }


class ForecastMathTests(unittest.TestCase):
    def test_rejects_bad_zip(self):
        with self.assertRaises(ValueError):
            forecast.validate_zip("9310")
        with self.assertRaises(ValueError):
            forecast.validate_zip("abcde")

    def test_detects_santa_barbara_zip_scope(self):
        location = {"zip": "93101", "city": "Santa Barbara", "state_code": "CA"}
        self.assertTrue(forecast.is_santa_barbara_location(location))
        self.assertFalse(forecast.is_santa_barbara_location({"zip": "10001", "city": "New York", "state_code": "NY"}))

    def test_weekend_ideal_weather_scores_high(self):
        weather = {
            "time": ["2026-06-06"],
            "temperature_2m_max": [74],
            "temperature_2m_min": [60],
            "precipitation_probability_max": [5],
        }
        score = forecast.calculate_demand_score(make_day(5), weather, [], 0)
        self.assertEqual(score["level"], "HIGH")
        self.assertEqual(score["score"], 87)

    def test_rain_and_cold_push_score_down(self):
        weather = {
            "time": ["2026-06-06"],
            "temperature_2m_max": [42],
            "temperature_2m_min": [32],
            "precipitation_probability_max": [80],
        }
        score = forecast.calculate_demand_score(make_day(0), weather, [], 0)
        self.assertEqual(score["level"], "LOW")
        self.assertEqual(score["score"], 20)

    def test_event_boost_is_capped_at_one_hundred(self):
        weather = {
            "time": ["2026-06-06"],
            "temperature_2m_max": [76],
            "temperature_2m_min": [61],
            "precipitation_probability_max": [0],
        }
        events = [{"date": "2026-06-06", "name": "Major Event", "type": "concert", "impact": "high"}]
        score = forecast.calculate_demand_score(make_day(5), weather, events, 0)
        self.assertEqual(score["score"], 100)
        self.assertEqual(len(score["events"]), 1)

    def test_weather_dates_drive_forecast_dates(self):
        days = forecast.get_next_7_days({"time": ["2026-06-05", "2026-06-06", "2026-06-07", "2026-06-08", "2026-06-09", "2026-06-10", "2026-06-11"]})
        self.assertEqual(days[0]["date"], "2026-06-05")
        self.assertEqual(days[0]["day_name"], "Friday")


if __name__ == "__main__":
    unittest.main()
