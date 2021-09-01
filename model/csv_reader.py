import csv


def get_timezones():
    timezones = []
    with open("csv/timezones.csv", newline='') as csv_file:
        for row in csv_file:
            timezones.append(row.split(",")[0])
    return timezones
