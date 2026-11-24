import csv
import math
import random
from pathlib import Path


def generate_millikan_results(num_runs=100, variance=True):
    density_of_drop = 900  # kg/m^3
    plate_separation_m = 0.003  # 3 mm (3 / 1000)
    g = 9.8
    e = 1.602e-19

    simulation_data = []

    for run in range(1, num_runs + 1):
        # Generate voltage matching the JS: Math.floor(Math.random()*100 + 100)/10
        voltage = math.floor(random.random() * 100 + 100) / 10.0
        electric_field = voltage / plate_separation_m

        # Pick a random charge number (1 to 8)
        charge_number = math.floor(random.random() * 8) + 1
        q = charge_number * e

        # Formula copied from the website's JS
        r_cubed = (3 * q * electric_field) / (4 * math.pi * density_of_drop * g)
        radius_m = math.pow(r_cubed, 1/3)

        # Apply the same scaling from the JS code (Radius * 1e6 * 100)
        final_radius = radius_m * 1e6 * 100

        # Add variance to fake that this data was manually collected
        if variance:
            final_radius += random.choice(-0.3, 0.3)

        simulation_data.append({
            "Run": run,
            "Oil_Density": density_of_drop,
            "Plate_Separation_m": plate_separation_m,
            "Voltage": voltage,
            "Radius": final_radius
        })

    return simulation_data

# Execute
data = generate_millikan_results(100)


def get_unique_filepath(folder: str, base_name: str, extension: str) -> Path:
    """
    Generates a unique filename for a file in a folder. Appends _n to the file, where n is the unique identifier.
    """
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
    
    counter = 0
    while True:
        filepath = folder_path / f"{base_name}_{counter}.{extension}"
        if not filepath.exists():
            return filepath
        counter += 1


# Create a filename
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "results"
csv_filename = get_unique_filepath(OUTPUT_DIR, "mlkn_results", "csv")

# Save the data to a file in a folder called 'results/'
with open(csv_filename, mode='w', newline='') as f:
    fieldnames = ["Run", "Oil_Density", "Plate_Separation_m", "Voltage", "Radius"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

# Print a clickable link to the newly saved data
file_uri = Path(csv_filename).resolve().as_uri()
print(f"Simulation data saved successfully to '{file_uri}'!")