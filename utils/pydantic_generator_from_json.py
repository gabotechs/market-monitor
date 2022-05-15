import json


def generate(raw: str):
    decoded = json.loads(raw)
    print('class Model(pydantic.BaseMode):')
    for k, v in decoded.items():
        print(f'    {k}: Optional[{type(v).__name__}]')


if __name__ == '__main__':
    generate(input('>>>'))