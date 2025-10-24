from datetime import datetime, time, UTC, date
from django.test import TestCase
from faker import Faker

from interviews.models import InterviewTemplate, Interviewer
from interviews.helpers import (
    set_time_to_nearest_half_hour,
    get_all_possible_time_blocks,
    get_time_blocks_from_busy_data,
    get_all_available_time_blocks
)


interviewer_name_1 = Faker().name()
interviewer_name_2 = Faker().name()
# Create your tests here.
class InterviewsModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        interviewer_1 = Interviewer.objects.create(name=interviewer_name_1)
        interviewer_2 = Interviewer.objects.create(name=interviewer_name_2)
        interview = InterviewTemplate.objects.create(name='technical', durationMinutes=60)
        interview.interviewers.add(interviewer_1)
        interview.interviewers.add(interviewer_2)

    def test_interview_created(self):
        interview = InterviewTemplate.objects.get(interviewId=1)
        self.assertIsInstance(interview, InterviewTemplate)
        self.assertEqual(interview.name, 'technical')
        self.assertEqual(interview.durationMinutes, 60)

    def test_interviewers_created(self):
        interviewer_1 = Interviewer.objects.get(id=1)
        self.assertIsInstance(interviewer_1, Interviewer)
        self.assertEqual(interviewer_1.name, interviewer_name_1)
        interviewer_2 = Interviewer.objects.get(id=2)
        self.assertIsInstance(interviewer_2, Interviewer)
        self.assertEqual(interviewer_2.name, interviewer_name_2)

    def test_interview_get_json_by_id(self):
        interview = InterviewTemplate.get_json_by_id(1)
        self.assertEqual(interview['interviewId'], 1)
        self.assertIsInstance(interview, dict)


class InterviewsHelpersTestCase(TestCase):
    def test_set_time_to_nearest_half_hour(self):
        self.assertEqual(
            set_time_to_nearest_half_hour(time(hour=0, minute=0, microsecond=0)),
            time(hour=0, minute=0, microsecond=0)
        )
        self.assertEqual(
            set_time_to_nearest_half_hour(time(hour=0, minute=0, microsecond=1)),
            time(hour=0, minute=30, microsecond=0)
        )
        self.assertEqual(
            set_time_to_nearest_half_hour(time(hour=0, minute=31)),
            time(hour=1, minute=0, microsecond=0)
        )
        self.assertEqual(
            set_time_to_nearest_half_hour(time(hour=0, minute=59, microsecond=1)),
            time(hour=1, minute=0, microsecond=0)
        )
        self.assertEqual(
            set_time_to_nearest_half_hour(time(hour=23, minute=59, microsecond=1)),
            time(hour=23, minute=30, microsecond=0)
        )

    def test_get_all_possible_time_blocks(self):
        self.assertEqual(
            len(get_all_possible_time_blocks(60*8, datetime(year=2025, month=1, day=1, hour=9, minute=0, tzinfo=UTC))),
            4
        )
        self.assertEqual(
            len(get_all_possible_time_blocks(60 * 8 - 30,
                                             datetime(year=2025, month=1, day=1, hour=9, minute=0, tzinfo=UTC))),
            8
        )
        self.assertEqual(
            len(get_all_possible_time_blocks(60 * 8,
                                             datetime(year=2025, month=1, day=1, hour=0, minute=0, tzinfo=UTC))),
            4
        )
        self.assertEqual(
            len(get_all_possible_time_blocks(60 * 8,
                                             datetime(year=2025, month=1, day=1, hour=10, minute=0, tzinfo=UTC))),
            3
        )
        time_blocks = get_all_possible_time_blocks(45)
        self.assertTrue(
            all([time_block['start'].minute == 30 or time_block['start'].minute == 0 for time_block in time_blocks])
        )
        self.assertTrue(
            all([time_block['start'].time() >= time(hour=9) for time_block in time_blocks])
        )
        self.assertTrue(
            all([time_block['end'].time() <= time(hour=17) for time_block in time_blocks])
        )

    def test_get_time_blocks_from_busy_data(self):
        list_of_time_blocks = get_time_blocks_from_busy_data([1, 2])
        for time_blocks in list_of_time_blocks:
            for index in range(1, len(time_blocks)):
                self.assertGreaterEqual(time_blocks[index]['start'], time_blocks[index - 1]['start'])
                self.assertGreaterEqual(time_blocks[index]['end'], time_blocks[index - 1]['end'])

    def test_get_all_available_time_blocks(self):
        unavailable_time_blocks = [[{
            'start': datetime(year=2025, month=1, day=2, hour=9, tzinfo=UTC),
            'end': datetime(year=2025, month=1, day=2, hour=17, tzinfo=UTC)
        }]]
        self.assertEqual(
            len(get_all_available_time_blocks(
                [dict(id=1)], 60*8, dt=datetime(year=2025, month=1, day=1, hour=9, tzinfo=UTC), unavailable_time_blocks_list=unavailable_time_blocks
            )),
            3
        )
