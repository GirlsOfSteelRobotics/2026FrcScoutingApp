import requests


def __make_request(url: str, org_key: str, event_key: str) -> bytes:
    cookies = {
        "org_key": org_key,
        "event_key": event_key,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
    }
    response = requests.get(url, cookies=cookies, headers=headers)
    print(url)
    return response.content


def request_scout_radioz_match_scouting(org_key, event_key):
          # "https://scoutradioz.com/reports/exportdata?type=matchscouting&span=all"
    url = "https://scoutradioz.com/reports/exportdata?type=matchscouting?span=all"
    return __make_request(url, org_key, event_key)


def download_scout_radioz_match_scouting(org_key, event_key, output_file):
    content = request_scout_radioz_match_scouting(org_key, event_key)

    if len(content) == 0:
        import pandas as pd
        columns = [
            'Scouter Initials', 'Match Number', 'Team Number', 'No Show',
            'Auto Fuel', 'Auto Climbing Status', 'Auto Human Player Score',
            'Teleop Fuel', 'Teleop Fuel Passed', 'Endgame Climbing Level'
        ]
        content = bytes(",".join(columns), "utf-8")
        content += b"\n,,,,,,,frc0000"

    with open(output_file, "wb") as f:
        f.write(content)


def request_scout_radioz_pit_scouting(org_key, event_key):
    url = "https://scoutradioz.com/reports/exportdata?type=pitscouting?span=all"
    return __make_request(url, org_key, event_key)


def download_scout_radioz_pit_scouting(org_key, event_key, output_file):
    content = request_scout_radioz_pit_scouting(org_key, event_key)
    with open(output_file, "wb") as f:
        f.write(content)