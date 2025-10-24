from datetime import datetime, timedelta, UTC, time

from interviews.mock_availability import get_free_busy_data

def set_time_to_nearest_half_hour(dt_time) -> time:
    """
    Rounds up datetime time to nearest half hour with exception that rolling over to next day sets time to last half
    hour of the day.
    :param time dt_time: datetime time to replace
    :returns: datetime time set to the nearest half hour
    """
    hour = dt_time.hour
    minute = dt_time.minute
    ms = dt_time.microsecond
    if ms > 0:
        minute += 1

    if 0 < minute <= 30:
        minute = 30
    elif 30 < minute <= 60:
        minute = 0
        hour += 1

    if hour > 23:
        hour = 23
        minute = 30
    return time(hour=hour, minute=minute, second=0)


def get_all_possible_time_blocks(duration, dt=None) -> list[dict[str, datetime]]:
    """
    Gets all possible time blocks for a given interview duration for the next week excluding Saturdays and Sundays.
    :param int duration: duration in minutes of interview
    :param datetime dt: start date and time of interview week
    :returns: blocks of available times for the interview [{'start': start_datetime, 'end': end_datetime}, ...]
    Requirements:
        Slots must be exactly the duration minutes of the template
        Slots must begin on hour or half-hour marks (e.g., 10:00, 10:30)
        No slot may begin less than 24 hours in the future
        All times must be in UTC in ISO 8601 format
        Must exclude Saturday and Sunday.
        Must start and end between 9AM-5PM (9-17) UTC based on mock_availability
        Must match date range of 7 days based on mock_availability
    """
    if not dt:
        dt = datetime.now(UTC)
    start_datetime = dt + timedelta(days=1)
    start_date = start_datetime.date()
    start_time = set_time_to_nearest_half_hour(start_datetime.time())
    min_datetime = max(datetime.combine(start_date, start_time, tzinfo=UTC), datetime.combine(start_date, time(9), tzinfo=UTC))
    max_datetime = datetime.combine(start_date, time(17), tzinfo=UTC)
    time_blocks = []
    for day in range(6):
        if start_date.weekday() < 5:
            while min_datetime < max_datetime:
                end = min_datetime + timedelta(minutes=duration)
                if end <= max_datetime:
                    time_blocks.append({'start': min_datetime, 'end': end})
                min_datetime += timedelta(minutes=30)
        start_date += timedelta(days=1)
        min_datetime = datetime.combine(start_date, time(9), tzinfo=UTC)
        max_datetime += timedelta(days=1)
    return time_blocks


def get_time_blocks_from_busy_data(interviewers) -> list[list[dict[str, datetime]]]:
    """
    Gets all unavailable time blocks for the given interviewers.
    :param list[int] interviewers: list of interviewer ids
    :returns: unavailable time blocks for the interview [{'start': start_datetime, 'end': end_datetime}, ...]
    """
    busy_data = get_free_busy_data(interviewers)
    unavailable_time_blocks = []
    for data in busy_data:
        slots = []
        for slot in data.get('busy', []):
            slots.append({'start': datetime.fromisoformat(slot['start']), 'end': datetime.fromisoformat(slot['end'])})
        unavailable_time_blocks.append(sorted(slots, key=lambda x: (x['start'], x['end'])))
    return unavailable_time_blocks


def get_available_from_unavailable_time_block(possible_time_blocks, unavailable_time_blocks) -> list[dict[str, datetime]]:
    """
    Removes unavailable time ranges from possible time blocks and returns that as a list of dicts
    :param list[dict[str, datetime]] possible_time_blocks: list of available time blocks [{'start': start_datetime, 'end': end_datetime}, ...]
    :param list[dict[str, datetime]] unavailable_time_blocks: list of unavailable time blocks [{'start': start_datetime, 'end': end_datetime}, ...]
    :returns: list of available time blocks [{'start': start_datetime, 'end': end_datetime}, ...]
    """
    possible_index = 0
    possible_length = len(possible_time_blocks)
    unavailable_index = 0
    unavailable_length = len(unavailable_time_blocks)
    available_time_blocks = []
    while possible_index < possible_length:
        if unavailable_index >= unavailable_length:
            available_time_blocks.append(possible_time_blocks[possible_index])
            possible_index += 1
        elif possible_time_blocks[possible_index]['end'] <= unavailable_time_blocks[unavailable_index]['start']:
            available_time_blocks.append(possible_time_blocks[possible_index])
            possible_index += 1
        elif possible_time_blocks[possible_index]['start'] >= unavailable_time_blocks[unavailable_index]['end']:
            unavailable_index += 1
        else:
            possible_index += 1
    return available_time_blocks


def get_all_available_time_blocks(interviewers, duration, dt=None, unavailable_time_blocks_list=None) -> list[dict[str, datetime]]:
    """
    Gets all possible time blocks for a given interview duration for the next week for the given interviewers.
    :param list[dict] interviewers: dict of interviewers
    :param int duration: duration in minutes of interview
    :param datetime dt: start date and time of interview week
    :param list[list[dict[str, datetime]]] unavailable_time_blocks_list: list of lists of unavailable time blocks
    :returns: available time blocks for the interview [{'start': start_datetime, 'end': end_datetime}, ...]
    Requirements:
        All interviewers must be available for the full slot duration
        All times must be in UTC in ISO 8601 format
    """
    interviewer_ids = [interviewer['id'] for interviewer in interviewers]
    if not unavailable_time_blocks_list:
        unavailable_time_blocks_list = get_time_blocks_from_busy_data(interviewer_ids)
    all_possible_time_blocks = get_all_possible_time_blocks(duration, dt=dt)
    for unavailable_time_block in unavailable_time_blocks_list:
        all_possible_time_blocks = get_available_from_unavailable_time_block(all_possible_time_blocks, unavailable_time_block)
    return all_possible_time_blocks
