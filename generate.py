import json

from src.outpainting import Outpainting
from src.utils import zip_folder, clean_prompt

with open('input/prompts.json', 'r') as json_file:
    data = json.load(json_file)

if data is None:
    print("No data found")
    exit()

parsed_data = []

for entry in data:
    prompt = entry['prompt']
    headline = entry['headline']
    source = entry['source']
    date = entry['date']

    parsed_entry = {
        'prompt': prompt,
        'headline': headline,
        'source': source,
        'date': date
    }
    parsed_data.append(parsed_entry)

if parsed_data is None:
    print("No entry found")
    exit()

outpainting = Outpainting()
for entry in parsed_data:
    outpainting.generate_image(clean_prompt(entry['prompt']), entry['headline'], entry['source'], entry['date'])

folder_path = 'outpainting'
zip_path = 'export/export.zip'

zip_folder(folder_path, zip_path)

print("Done")
