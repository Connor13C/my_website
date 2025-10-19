from django.shortcuts import render
from django.http import JsonResponse

from interviews.helpers import get_all_available_time_blocks
from interviews.models import InterviewTemplate
# Create your views here.

def interviews_availability(request, id:int):
    """
    Gets the InterviewTemplate table from the database adds all possible time blocks for a given interview duration
    and returns it as a JsonResponse.
    :param id: interviewId of InterviewTemplate
    :returns: json response of interview Ex:
    {
        "interviewId": 1,
        "name": "Technical Interview",
        "durationMinutes": 60,
        "interviewers": [
            { "id": 1, "name": "Alice Johnson" },
            { "id": 2, "name": "Bob Smith" }
        ],
        "availableSlots": [
            {
                "start": "2025-01-22T10:00:00Z",
                "end": "2025-01-22T11:00:00Z"
            },
            {
            "start": "2025-01-22T11:00:00Z",
            "end": "2025-01-22T12:00:00Z"
            }
        ]
    }
    """
    interview = InterviewTemplate.get_json_by_id(id)
    #TODO change interviewers to match expected
    # interviewer_ids = [interviewer['id'] for interviewer in interview.get('interviewers', [])]
    # interview['availableSlots'] = get_all_available_time_blocks(interviewer_ids, interview['durationMinutes'])
    interview['availableSlots'] = get_all_available_time_blocks(interview.get('interviewers'), interview['durationMinutes'])
    return JsonResponse(interview)
