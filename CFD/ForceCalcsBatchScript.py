import os
import pandas as pd
import subprocess
import datetime

main_folder = "C:/Users/Alexis/Documents/CFD/CFDAutomation"
mesh_folder = os.path.join(main_folder, "Mesh_Files_Drag_Calcs")
results_folder = os.path.join(main_folder, 'Results Folder')
#results_folder = "C:/Users/ChemeGrad2021/OneDrive - Massachusetts Institute of Technology/Documents/Olsen Lab/Small Format Recycling/CFD projects/CFDAutomation/Results Folder"
journal_file = os.path.join(main_folder, 'ForceCalc_09112024.jou')
#journal_file = "C:/Users/ChemeGrad2021/OneDrive - Massachusetts Institute of Technology/Documents/Olsen Lab/Small Format Recycling/CFD projects/CFDAutomation/DragCalc_test3.jou"

# Ensure the results folder exists
os.makedirs(results_folder, exist_ok=True)

force_data = pd.DataFrame(columns=['File Name', 'Convergence Iter', 'Drag Force', 'Drag Coeff', 'Lift Force', 'Lift Coeff'])

timestamp = '{:%Y%m%d_%H%M}'.format(datetime.datetime.now())

# Loop over all .msh files in the mesh folder
for mesh_file in os.listdir(mesh_folder):
    print(f'File in Folder: {mesh_file}')
    if mesh_file.endswith(".msh"):
        print(f'Msh File in Folder: {mesh_file}')
        # Construct the full file path
        mesh_path = os.path.join(mesh_folder, mesh_file)
        output_path = os.path.join(results_folder, f"{os.path.splitext(mesh_file)[0]}_results.cas.h5")
        # case_folder = ''
        case_folder = os.path.join(main_folder, mesh_file[:-4])

        # Update the journal file with the specific mesh and output paths
        with open(journal_file, 'r') as file:
            journal_content = file.read()

        journal_content = journal_content.replace("path/to/mesh.msh", mesh_path)
        journal_content = journal_content.replace("path/to/results.cas.h5", output_path)
        journal_content = journal_content.replace('report-file-i', f'report-file-{mesh_file[:-4]}')

        # Write the updated journal file
        updated_journal_file = "updated.jou"
        with open(updated_journal_file, 'w') as file:
            file.write(journal_content)

        # Run Fluent in batch mode
        subprocess.run([
            "C:/Program Files/ANSYS Inc/ANSYS Student/v242/fluent/ntbin/win64/fluent", "3d", "-g", "-i", updated_journal_file,
            "-t", "4",  # Number of processors, adjust as needed
        ])

        # Read the file into a list of lines; extract last line which holds the solution from the last iteration
        with open(f'report-file-{mesh_file[:-4]}.out', 'r') as file:
            lines = file.readlines()
            last_line = [mesh_file[:-4]] + lines[-1].split()

        force_data.loc[len(force_data)] = last_line
        force_data.to_csv(f'Calculated_Force_{timestamp}.csv', index=False)
        
