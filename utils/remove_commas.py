def remove_commas_from_file(source_file, destination_file):
    with open(source_file, 'r') as src, open(destination_file, 'w') as dest:
        for line in src:
            dest.write(line.replace(',', ' '))

# Call the function with your file paths
remove_commas_from_file('cloud.xyz', './pcd/point_cloud.xyz')
