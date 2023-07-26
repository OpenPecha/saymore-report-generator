import yaml
from pathlib import Path


from elan_file_downloader import download_files_by_extension
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


def dump_yaml(data,output_fn) -> Path:
    with output_fn.open("w", encoding="utf-8") as fn:
        yaml.dump(
            data,
            fn,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            Dumper=yaml.SafeDumper,
        )
    return output_fn

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
    


def get_annotation_time_report(repo_list, github_token):
    total_number_of_syllables = 0
    total_time_annotated = 0
    avg_syllable_per_minute = 0
    annotation_report = {}
    destination_folder = f"./data/eaf"
    repo_owner = 'MonlamAI'
    for repo in repo_list:
        repo_url = f"https://api.github.com/repos/{repo_owner}/{repo}/contents/"
        destination_file_path = f'{destination_folder}/{repo}.eaf'
        if not Path(destination_file_path).exists():
            download_files_by_extension(repo_url, '.eaf', destination_file_path, github_token)
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
            'avg_syllable_per_minute': total_number_of_syllables/total_time_annotated
            }
    return annotation_report
    

if __name__ == "__main__":
    team_names = ['team_a', 'team_b', 'team_c', 'team_d',]
    # team_names = ['overall']
    for team_name in team_names:
        # team_name = "team_a"
        repo_list = Path(f'./data/repo_list/{team_name}.txt').read_text().split('\n')
        repo_list = list(set(repo_list))
        github_token = "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"
        annotation_report = get_annotation_time_report(repo_list, github_token)
        # dump_yaml(annotation_report, Path(f'./data/annotation_report/{team_name}.yaml'))
        save_dict_to_csv(annotation_report, Path(f'./data/annotation_report/{team_name}.csv'))
