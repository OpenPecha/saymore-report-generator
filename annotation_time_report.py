from pathlib import Path

from copy_elan_file import copy_eaf_files
from elan_parser.annotation_time import calculate_total_time_blank_segment, calculate_total_time_annotated
from elan_parser.syllable_counter import get_syllable_count_from_eaf

import csv

def save_dict_to_csv(dictionary, file_path):

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Repo', 'Blank segment time', 'Syllable count', 'With speech segment time', 'Cost blank segment', 'Cost syllable annotated', 'Total cost'])
        for repo, repo_info in dictionary.items():
            try:
                repo_entry = [repo]+list(repo_info.values())
                writer.writerow(repo_entry)
            except:
                repo_entry = [repo]+[repo_info]
                writer.writerow(repo_entry)

    print(f"Dictionary saved as CSV file: {file_path}")

def parse_eaf(eaf_file):
    delimeters = ['་', '།',]
    blank_segment_time = calculate_total_time_blank_segment(eaf_file)
    with_speech_segment_time = calculate_total_time_annotated(eaf_file)
    syllable_count = get_syllable_count_from_eaf(eaf_file, delimeters)
    cost_of_blank_segment = int(blank_segment_time*5)
    cost_of_syllable_annotated = int((with_speech_segment_time)*67)
    total_cost = cost_of_syllable_annotated+cost_of_blank_segment
    return {
            'blank_segment_time': blank_segment_time, 
            'syllable_count': syllable_count, 
            'with_speech_segment_time': with_speech_segment_time,
            'cost_blank_segment': f'Rs{cost_of_blank_segment}',
            'cost_syllable_annotated': f'Rs{cost_of_syllable_annotated}',
            'total_cost': f'Rs{total_cost}'
            }

def get_annotation_time_report(repo_list, repo_path):
    total_number_of_syllables = 0
    total_time_annotated = 0
    avg_syllable_per_minute = 0
    annotation_report = {}
    destination_folder = f"./data/eaf"
    repo_owner = 'MonlamAI'
    for repo in repo_list:
        repo_path = f"{repo_path}/{repo}/"
        destination_file_path = f'{destination_folder}/{repo}.eaf'
        if not Path(destination_file_path).exists():
            copy_eaf_files(repo_path, destination_file_path)
        if Path(destination_file_path).exists():
            eaf_report= parse_eaf(destination_file_path)
            total_time_annotated += eaf_report['with_speech_segment_time']
            total_number_of_syllables += eaf_report['syllable_count']
            annotation_report[repo] = eaf_report
        else:
            annotation_report[repo] = 'file not found'
    annotation_report['Summary'] = {
            'total_number_of_syllables': total_number_of_syllables, 
            'total_time_annotated': total_time_annotated, 
            'avg_syllable_per_minute': total_number_of_syllables/total_time_annotated if total_time_annotated else 0
            }
    return annotation_report
    

if __name__ == "__main__":
    team_names = ['team_a']
    for team_name in team_names:
        repo_list = Path(f'./data/repo_list/{team_name}.txt').read_text().split('\n')
        repo_list = list(set(repo_list))
        annotation_report = get_annotation_time_report(repo_list, repo_path="/home/ec2-user/SageMaker/STT_NW")
        save_dict_to_csv(annotation_report, Path(f'./data/annotation_report/{team_name}.csv'))
