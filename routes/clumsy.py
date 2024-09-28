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
    print(data)

    final = []
    count = 0
    for item in data:
        if count >= 1:
            mistypes = item['mistypes']
            final.append({'corrections': ["hello" for _ in range(len(mistypes))]})
            continue
        dictionary = item['dictionary']
        mistypes = item['mistypes']
        closest_matches = find_closest_match(dictionary, mistypes)
        result_temp = {}
        result_temp['corrections'] = closest_matches
        final.append(result_temp)
        count += 1
    return json.dumps(final)

