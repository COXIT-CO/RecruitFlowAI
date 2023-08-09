import json

from context import Resume


if __name__ == '__main__':
    with open('data_examples/parsed_cv_example.json') as cv:
        json_data = json.load(cv)
    res_obj = Resume(**json_data, **json_data['info'])
    print(json.dumps(res_obj.dict(), indent=4))
