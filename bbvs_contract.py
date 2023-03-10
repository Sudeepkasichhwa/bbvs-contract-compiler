import click
from datetime import datetime, timedelta
import json


def load_json():
    with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json") as f:
        return json.load(f)


def write_json(new_data, key, file_name=r"C:\Users\acer\PycharmProjects\CLI\contract_data.json"):
    with open(file_name, 'r+') as file:
        file_data = json.load(file)
        file_data[key].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.close()


# initialize votecount of each candidate
def initialize_votecount():
    with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json", 'r+') as file:
        file_data = json.load(file)

        for i in range(len(file_data['candidates'])):
            cand_id = file_data['candidates'][i]['candidate_id']
            votes_count = {cand_id: 0}                      # in dict form
            # file_data['votes_count'][cand_id] = 0
            file_data['votes_count'].update(votes_count)

        file_data["total_votes"] = 0
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def set_voter_status():
    with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json", 'r+') as file:
        file_data = json.load(file)

        for i in range(len(file_data["voters"])):
            file_data["voters"][i]["has_voted"] = False
            file_data["total_votes"] = 0
            file_data["voters"][i]["voted_to"] = []

        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def is_voter_available(voter_id):
    status = False
    file_data = load_json()
    for i in range(len(file_data["voters"])):
        if (file_data["voters"][i]["voter_id"] == voter_id):
            status = True
            break
    if status:
        return True
    else:
        print(f"Voter_id: {voter_id} not available")

def is_candidate_available(candidate_ids):
    list_candidate_ids = candidate_ids.strip('][').split(',' or ', ')
    print(type(list_candidate_ids),list_candidate_ids)
    status = False
    file_data = load_json()
    for cand_id in list_candidate_ids:
        for i in range(len(file_data["candidates"])):
            if (file_data["candidates"][i]["candidate_id"] == cand_id):
                status = True
                break
            else:
                status = False
            print(f"{cand_id}: {status}")

        if status == False:
            print(f"Candidate_id: {cand_id} not available")
            break

    if status:
        return True


def has_already_voted(voter_id):
    status = False
    file_data = load_json()
    for i in range(len(file_data["voters"])):
        if (file_data["voters"][i]["voter_id"] == voter_id):
            if (file_data["voters"][i]["has_voted"] == False):
                status = True
                break
    if status == True:
        return True
    else:
        print("Voter has already voted")


# check to start election
def are_members_available():
    file_data =load_json()
    if (len(file_data['candidates'])!= 0 and len(file_data['voters'])!= 0):
        return True
    else:
        if len(file_data['candidates'])==0:
            print("Candidates are not available")
        elif len(file_data['voters'])==0:
            print("Voters are not available")

def voting_line_open():
    file_data = load_json()
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    voting_end_time = datetime.strptime(file_data["voting_end_time"], date_format)
    if datetime.now() < voting_end_time:
        return True
    else:
        print("Voting session is closed")
        return False

@click.group()
def cli():
    pass


@cli.command()
@click.option('--election', nargs=2, help="Provide Election name, End time")
def start_election(election):
    election_name, end_time = election
    voting_start_time = datetime.now()  # current time
    voting_end_time = voting_start_time + timedelta(minutes=int(end_time))

    initialize_votecount()
    set_voter_status()
    if are_members_available():
        with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json", 'r+') as file:
            file_data = json.load(file)
            file_data["results"] = []           # reset result

            file_data['voting_start_time'] = str(voting_start_time)
            file_data['voting_end_time'] = str(voting_end_time)
            file_data['election_name'] = str(election_name)
            file.truncate(0)
            file.seek(0)
            json.dump(file_data, file, indent=4)

        print(voting_start_time)
        print(voting_end_time)

    # timestamp = datetime.timestamp(voting_end_time)
    # print("\ntimestamp :", timestamp + 5)
    # print("current : ", datetime.fromtimestamp(timestamp + 5))


@cli.command()
def reset():
    with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json", 'r+') as file:
        file_data = json.load(file)
        # print(file_data.keys())
        file_data['candidates'].clear()
        file_data["voters"].clear()
        file_data["results"].clear()
        file_data["votes_count"].clear()
        file_data["election_name"] = " "
        file_data["total_votes"] = " "
        file_data["voting_start_time"] = " "
        file_data["voting_end_time"] = " "
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


@cli.command()
def get_remaining_time():
    file_data = load_json()
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    # datetime_obj = datetime.strptime(file_data["voting_end_time"], date_format)
    remaining_time = datetime.strptime(file_data["voting_end_time"], date_format) - datetime.now()
    if (remaining_time.days >= 0):
        print(remaining_time)
        return remaining_time
    else:
        print("Voting session is closed")


@cli.command()
def get_candidate_list():
    file_data = load_json()
    candidate_list = file_data["candidates"]
    print(candidate_list)
    return candidate_list


@cli.command()
def get_voter_list():
    file_data = load_json()
    voter_list = file_data["voters"]
    print(voter_list)
    return voter_list



@cli.command()
@click.option('--details', nargs=5, help=' candidate_id, name, image_url, post, logo')
def initialize_candidates(details):
    candidate_id, name, image_url, post, logo = details
    candidate_detail = {"candidate_id": candidate_id, "name": name, "image_url": image_url, "post": post,"logo":logo}
    write_json(candidate_detail, 'candidates')
    print("Candidate added.")


@cli.command()
@click.option('--details', nargs=4, help='voter_id, name, voted_to, has_voted')
# key = {"voter_id": "020","name": "nabin","voted_to": [ candidates list ],"has_voted": ""}
def initialize_voters(details):
    voter_id, name, voted_to, has_voted = details

    list_voted_to = voted_to.strip('][').split(',' or ', ')  # converting to list
    # print("final list", list_voted_to)
    print(list_voted_to)
    voter_detail = {"voter_id": voter_id, "name": name, "voted_to": list_voted_to, "has_voted": has_voted}
    write_json(voter_detail, 'voters')


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


@cli.command()
@click.option('--vote', nargs=2, help="provide: voter_id, candidate_ids[]")
def do_vote(vote):
    voter_id, candidate_ids = vote
    # voting lines open
    # is eligible vote
    if (is_voter_available(voter_id) and is_candidate_available(candidate_ids) and has_already_voted(voter_id) and voting_line_open()):
        with open(r"C:\Users\acer\PycharmProjects\CLI\contract_data.json", 'r+') as file:
            file_data = json.load(file)

            list_candidate_ids = candidate_ids.strip('][').split(',' or ', ')  # converting to list
            # write voted candidates list
            for i in range(len(file_data['voters'])):
                if file_data['voters'][i]['voter_id'] == voter_id:
                    file_data['voters'][i]['voted_to'] = list_candidate_ids
                    file_data['voters'][i]['has_voted'] = True

            # write votes count of each candidate
            for i in list_candidate_ids:
                vote_count = file_data['votes_count'][i]
                file_data['votes_count'][i] = vote_count + 1

            file_data["total_votes"] = file_data["total_votes"] + 1
            file.truncate(0)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            print("vote done !!")

@cli.command()
def get_results():
    if (voting_line_open()):
        print("Voting session is going on. Wait !!")
    else:
        file_data = load_json()

        for i in range(len(file_data["candidates"])):
            cand_id = file_data["candidates"][i]["candidate_id"]
            result = {
                "name" : file_data["candidates"][i]["name"],
                "candidate_id" : file_data["candidates"][i]["candidate_id"],
                "image_url": file_data["candidates"][i]["image_url"],
                "post": file_data["candidates"][i]["post"],
                "votecount": file_data["votes_count"][cand_id],
                "logo": file_data["candidates"][i]["logo"]
            }
            print(result)
            write_json(result,"results")

        return file_data["results"]


cli()
