def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w", encoding="utf-8")

    file.write("Company, Position, Location, Link\n")

    for job in jobs:
        file.write(f"{job['Company']}, {job['Position']}, {job['Location']}, {job['Link']}\n")

    file.close()
    return file
