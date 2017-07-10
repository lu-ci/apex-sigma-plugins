import yaml
import secrets

responses = {}


def load_responses(file):
    with open(file) as resp_file:
        response_data = yaml.safe_load(resp_file)
        return response_data


def grab_response(file, trigger):
    global responses
    if not responses:
        responses = load_responses(file)
    if trigger not in responses:
        resp_data = load_responses(file)
        responses.update({trigger: resp_data[trigger]})
    if not responses[trigger]:
        resp_data = load_responses(file)
        responses.update({trigger: resp_data[trigger]})
    trigger_responses = responses[trigger]
    pop_number = secrets.randbelow(len(trigger_responses))
    resp = trigger_responses.pop(pop_number)
    responses.update({trigger: trigger_responses})
    return resp
