import pandas as pd
import os

def extract_and_save_data(file_path, localTime):
    with open(file_path, 'r') as file:
        content = file.read()

    # Initialize a list to hold DataFrames for each dataset
    dataset_blocks = content.split('MCD_v6.1 with climatology average solar scenario.')
    # Iterate over the dataset blocks
    for block in dataset_blocks[1:]:
        # Clean any extra whitespace or empty lines
        block = block.strip()
        # Extract the variable name from the first block (this will be in the metadata)
        for lines in block.splitlines():
            if 'Columns 2+ are ' in lines:
                variable_name = ''.join([a.capitalize() for a in lines[lines.find('Columns 2+ are ')+15:].strip().split(' ')]) if "(" not in lines else ''.join([a.capitalize() for a in lines[lines.find('Columns 2+ are ')+15:lines.find("(")].strip().split(' ')])
        
        # Split the dataset into lines
        lines = block.splitlines()[9:]
        # Process the data lines
        data = []
        longitude = []
        column_names = lines[0].split()[2:]
        for line in lines[2:]:
            # Skip the separator lines
            if '----' in line or '||' not in line:
                continue
            # Split each line by spaces
            parts = line.split()
            longitude.append(parts[0])
            values = parts[2:] if '#' not in parts else parts[2:parts.find('#')]
            data.append(values)

        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=column_names, index=longitude)

        #Make directory
        os.makedirs(f'{variable_name}', exist_ok=True)

        df.to_csv(os.path.join(variable_name,f"{variable_name}-{localTime}.csv"), index=True)
        print(f"{variable_name}-{localTime}.csv created")

# Example usage
for localTime in range(0,25):
    file_path = f'mars data.txt {localTime}'
    extract_and_save_data(file_path,localTime)