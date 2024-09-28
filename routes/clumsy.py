import json
import difflib
def find_closest_match(dictionary, mistypes):
    closest_matches = []
    for mistype in mistypes:
        closest_match = difflib.get_close_matches(mistype, dictionary, n=1)
        if closest_match:
            closest_matches.append(closest_match[0])
        else:
            closest_matches.append(None)
    return closest_matches


def solution(data):

    final = []
    for item in data:
        dictionary = item['dictionary']
        mistypes = item['mistypes']
        closest_matches = find_closest_match(dictionary, mistypes)
        result_temp = {}
        result_temp['corrections'] = closest_matches
        final.append(result_temp)
    return json.dumps(final)
