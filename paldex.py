from pathlib import Path
import json
import argparse

class Paldex():
    """Manages a list of completed capture bonuses of pals. Loads and saves to file"""

    def __init__(self, save_name='paldex.json'):
        """"""
        self.save_path = Path.home().joinpath('Documents', 'Programs', 'Paldex')
        self.save_path.mkdir(parents=True, exist_ok=True)
        self.save_path = self.save_path.joinpath(save_name)
        self.save_path.touch(exist_ok=True)
        contents = self.save_path.read_text()
        try:
            list_of_pals = json.loads(contents)
        except json.decoder.JSONDecodeError:
            list_of_pals = []

        self.completed_pals = [s.lower() for s in list_of_pals]

    def check_for_completion(self, name):
        """Check if name or partial name is in the completed list. returns a list of partial matches"""
        matches = []
        name = name.lower()
        for entry in self.completed_pals:
            if entry.startswith(name):
                matches.append(entry)
        if len(matches) != 0:
            return matches
        else:
            return None
        
    def add_entry(self, name):
        """add entry to list and save to file"""
        name = name.lower()
        if name not in self.completed_pals:
            self.completed_pals.append(name)
            # Write to file
            content = json.dumps(self.completed_pals)
            self.save_path.write_text(content)
            print(f'\tAdded {name.title()}\n')
        else:
            print(f'\t{name} already in list\n')
    
    def print_pals(self):
        """Print out the list of completed pals"""
        print("\t-------Completed Pals-------")
        for pal in self.completed_pals:
            print(f'\t{pal.title()}')
        print("\t----------------------------")
        
    def _text_in_green(self, string):
        """Returns the string in the color green"""
        return f'\033[92m {string}\033[00m'
    def _text_in_red(self, string):
        """Returns the string in the color red"""
        return f'\033[91m {string}\033[00m'

    def run(self):
        """run the paldex"""
        print('Welcome to the completed paldex.\nEnter a full or partial pal name to check for completion.')
        while True:
            user_input = input("Enter a name to search, '@palName' to add, '/show' to show, '/quit' to exit:\n  ")
            # Check input
            if user_input.startswith('/'):
                if user_input.lower().endswith('show'):
                    self.print_pals()
                elif user_input.lower().endswith('quit'):
                    break
            elif user_input.startswith('@'):
                self.add_entry(user_input.strip('@'))
            else:
                # Find any matches
                matches = self.check_for_completion(user_input)
                if matches:
                    for match in matches:
                        print(f'\t{self._text_in_green('COMPLETED')}: {match.title()}')
                else:
                    print(f'\t{self._text_in_red('CATCH')}: {user_input.title()}')
                print()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', help='Stores and loads data from provided JSON file.', default='paldex.json')
    args = parser.parse_args()
    if args.file_name.lower().endswith('.json'):
        paldex = Paldex(args.file_name)
        paldex.run()
    else:
        print('Invalid file format. Please supply a JSON file')
    