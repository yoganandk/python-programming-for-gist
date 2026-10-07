"""Buffer Austin datasets and print a feature count summary.

Purpose: Buffer each dataset listed in the settings block by its own
distance, write the outputs to an output folder, and print a summary of
the feature counts.
Author: Yoga Korgaonkar

To run: select the arcgispro-py3 interpreter, then click Run Python File.
"""

# Import modules
import os
import arcpy

# =====================================================================
# SETTINGS: edit only this block between runs
# =====================================================================

# Path to the working folder you created in course-data-setup.ipynb
# Output folder will be created in this folder
working_folder = r"C:\workspace\gist"

# Your initials, added to every output name
initials = "yk"  # TODO: Update this to your initials

# Dictionary of datasets to buffer (keys) and the buffer distance for each
# (values)
buffer_distances = {
    "hospitals.shp": "1 Kilometers",
    "parks.shp": "500 Meters",
}

# =====================================================================
# END OF SETTINGS: do not edit below this line between runs
# =====================================================================

# Function build_output_name
def build_output_name(dataset_name, user_initials):
    """Return an output name, such as "hospitals_buffer_yk.shp"."""
    # Remove the extension
    base_name = dataset_name.replace(".shp", "")
    # Suffix the base_name with initials and extension
    new_name = f"{base_name}_buffer_{user_initials}.shp"
    # Return the new name
    return new_name


# Build the path to the austin_data folder
data_folder = os.path.join(working_folder, "austin_data")

# Build the path to the shapefiles folder inside austin_data
shapefile_folder = os.path.join(data_folder, "shapefiles")

# Folder to store all created output: \outputs\m3\buffer_demo
output_folder = os.path.join(working_folder, "outputs", "m3", "buffer_demo")

# Create the output folder if it does not exist yet
os.makedirs(output_folder, exist_ok=True)

# Set the workspace to the output folder, so an output given as a name
# is written there.
arcpy.env.workspace = output_folder
# Allow tools to replace outputs from an earlier run
arcpy.env.overwriteOutput = True

# Print the settings for this run
print("==================================================")
print("Settings for this run")
print(f"Initials: {initials}")
print(f"Input folder: {shapefile_folder}")
print(f"Output folder: {arcpy.env.workspace}")
# len() of a dictionary returns the number of keys
print(f"Datasets to buffer: {len(buffer_distances)}")
print("==================================================")

# Empty dictionary will store the feature count of each buffered dataset
feature_counts = {}

# Empty list will store the names of any datasets that were not found
missing_datasets = []

# Variable will store the total number of features
total_features = 0

# Buffer each dataset by its distance from the settings block
print("Buffering datasets:")

# Run a for loop on the buffer_distances dictionary
for dataset_name, distance in buffer_distances.items():
    # Create the input_path
    input_path = os.path.join(shapefile_folder, dataset_name)

    # Check if the input_path exists
    if arcpy.Exists(input_path):
        # If input_path exists, call the function build_output_name
        output_name = build_output_name(dataset_name, initials)

        # Execute the Buffer tool
        # TODO: Fix bug
        # Use the full path (input_path), not just the dataset name
        buffer_result = arcpy.analysis.Buffer(
            dataset_name, output_name, distance
        )

        # Print Geoprocessing Messages
        print(buffer_result.getMessages())

        # Execute the GetCount tool using the output of the buffer tool
        count_result = arcpy.management.GetCount(buffer_result[0])

        # Get Count returns the count as a string, so convert it with int()
        feature_count = int(count_result[0])

        # Add the feature_count to the dictionary
        feature_counts[dataset_name] = feature_count

        # Update the total feature count
        total_features += feature_count

        # Print the dataset, its buffer distance, and its output name
        print(f"\t{dataset_name}: buffered {distance} -> {output_name}")
    else:
        # If the input_path does not exist, append the dataset name to the
        # missing_datasets list
        missing_datasets.append(dataset_name)

        # Print the dataset name and that it was skipped
        print(f"\t{dataset_name}: not found, skipped")

# Print the summary
print("==================================================")
print("Summary")

# len() of a dictionary returns the number of keys
print(f"Datasets buffered: {len(feature_counts)}")

# Loop over the feature_counts dictionary to print each dataset's count
# and buffer distance
for dataset_name, feature_count in feature_counts.items():
    # Look up the buffer distance for this dataset in buffer_distances
    distance = buffer_distances[dataset_name]
    print(f"\t{dataset_name}: {feature_count} features, {distance}")
# Print the total number of features buffered
print(f"Total features buffered: {total_features}")

# Print the skipped datasets, or "none" if the list is empty
if len(missing_datasets) > 0:
    print(f"Datasets skipped: {missing_datasets}")
else:
    print("Datasets skipped: none")
print("==================================================")
