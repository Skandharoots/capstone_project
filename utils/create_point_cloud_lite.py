def remove_commas_from_file(source_file, destination_file, max_lines=100000):
    line_count = 0
    with open(source_file, 'r') as src, open(destination_file, 'w') as dest:
        for line in src:
            dest.write(line)
            line_count += 1
            if line_count >= max_lines:
                break

# Call the function with your file paths
remove_commas_from_file('cloud.xyz', 'cloud_lite.xyz')
