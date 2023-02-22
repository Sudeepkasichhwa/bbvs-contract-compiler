import click
from datetime import datetime
import json


def load_json():
    f = open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json")
    return json.load(f)
    f.close()


def write_json(new_data, key, file_name=r"C:\Users\acer\PycharmProjects\CLI\contract_data.json"):
    with open(file_name, 'r+') as file:
        file_data = json.load(file)
        file_data[key].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.close()


@click.group()
def cli():
    pass


@cli.command()
def start_election():
    current_time = datetime.now()
    print(current_time)
    timestamp = datetime.timestamp(current_time)
    print("timestamp :", timestamp + 5)
    print("current : ", datetime.fromtimestamp(timestamp + 5))


@cli.command()
def reset():
    with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json", 'r+') as file:
        file_data = json.load(file)
        # print(file_data.keys())
        file_data['candidates'].clear()
        file_data["voters"].clear()
        file_data["results"].clear()
        file_data["election_name"] = " "
        file_data["total_votes"] = " "
        file_data["voting_start_time"] = " "
        file_data["voting_end_time"] = " "

        print(file_data)
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=5)


@cli.command()
def get_remaining_time():
    pass


@cli.command()
def get_candidate_list():
    file_data = load_json()
    candidate_list = file_data["candidates"]
    print(candidate_list)


@cli.command()
def get_voter_list():
    file_data = load_json()
    voter_list = file_data["voters"]
    print(voter_list)
    print(len(voter_list))


@cli.command()
@click.option('--details', nargs=4, type=(int, str, str, str), help=' candidate_id, name, image_url, post')
def initialize_candidates(details):
    candidate_id, name, image_url, post = details
    candidate_detail = {"candidate_id": candidate_id, "name": name, "image_url": image_url, "post": post}
    write_json(candidate_detail, 'candidates')
    print("Candidate added.")


@cli.command()
@click.option('--details', nargs=4, type=(int, str, str, bool), help='voter_id, name, voted_to, is_voted')
# key = {"voter_id": "020","name": "nabin","voted_to": "","is_voted": ""}
def initialize_voters(details):
    voter_id, name, voted_to, is_voted = details
    candidate_detail = {"voter_id": voter_id, "name": name, "voted_to": voted_to, "is_voted": is_voted}
    write_json(candidate_detail, 'voters')


@cli.command()
def get_voters_count():
    file_data = load_json()
    voter_list = file_data['voter']
    print(len(voter_list))
    return len(voter_list)


@cli.command()
def get_candidates_count():
    file_data = load_json()
    candidate_list = file_data['candidate']
    print(len(candidate_list))
    return len(candidate_list)


cli()
