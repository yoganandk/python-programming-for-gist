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
working_folder = r"C:\workspace\gist"

# Your initials, added to every output name
initials = "yk"

# Datasets to buffer (keys) and the buffer distance for each (values)
buffer_distances = {
    "hospitals.shp": "1 Kilometers",
    "parks.shp": "500 Meters",
}

# =====================================================================
# END OF SETTINGS: do not edit below this line between runs
# =====================================================================


def build_output_name(dataset_name, user_initials):
    """Return an output name, such as "hospitals_buffer_yk.shp"."""
    base_name = dataset_name.replace(".shp", "")
    new_name = f"{base_name}_buffer_{user_initials}.shp"
    return new_name


# Build the paths to the input and output folders
data_folder = os.path.join(working_folder, "austin_data")
shapefile_folder = os.path.join(data_folder, "shapefiles")
output_folder = os.path.join(working_folder, "outputs", "m3", "buffer_demo")

# Create the output folder if it does not exist yet
os.makedirs(output_folder, exist_ok=True)

# Set the workspace to the output folder, so an output given as a name
# is written there. Allow tools to replace outputs from an earlier run
arcpy.env.workspace = output_folder
arcpy.env.overwriteOutput = True

# Print the settings for this run
print("==================================================")
print("Settings for this run")
print(f"Initials: {initials}")
print(f"Input folder: {shapefile_folder}")
print(f"Output folder: {arcpy.env.workspace}")
print(f"Datasets to buffer: {len(buffer_distances)}")
print("==================================================")

# Store the feature count of each buffered dataset, the names of any
# datasets that were not found, and the total number of features
feature_counts = {}
missing_datasets = []
total_features = 0

# Buffer each dataset by its distance from the settings block
print("Buffering datasets:")
for dataset_name, distance in buffer_distances.items():
    input_path = os.path.join(shapefile_folder, dataset_name)

    if arcpy.Exists(input_path):
        output_name = build_output_name(dataset_name, initials)
        arcpy.analysis.Buffer(dataset_name, output_name, distance)

        # Get Count returns the count as a string, so convert it with int()
        count_result = arcpy.management.GetCount(input_path)
        feature_count = int(count_result[0])
        feature_counts[dataset_name] = feature_count
        total_features += feature_count
        print(f"\t{dataset_name}: buffered {distance} -> {output_name}")
    else:
        missing_datasets.append(dataset_name)
        print(f"\t{dataset_name}: not found, skipped")

# Print the summary
print("==================================================")
print("Summary")
print(f"Datasets buffered: {len(feature_counts)}")
for dataset_name, feature_count in feature_counts.items():
    distance = buffer_distances[dataset_name]
    print(f"\t{dataset_name}: {feature_count} features, {distance}")
print(f"Total features buffered: {total_features}")

if len(missing_datasets) > 0:
    print(f"Datasets skipped: {missing_datasets}")
else:
    print("Datasets skipped: none")
print("==================================================")
