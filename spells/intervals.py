from datetime import datetime


def reorder_intervals(intervals):
    # Sort the intervals by their start date
    sorted_intervals = sorted(intervals, key=lambda interval: interval["start"])

    result = []

    for i in range(len(sorted_intervals)):
        if i < len(sorted_intervals) - 1:
            result.append(
                {
                    "start": sorted_intervals[i]["start"],
                    "end": sorted_intervals[i + 1]["start"],
                }
            )
        else:
            result.append(
                {
                    "start": sorted_intervals[i]["start"],
                    "end": sorted_intervals[i]["end"],
                }
            )
    return result


intervals = [
    {"start": datetime(2023, 10, 1), "end": datetime(2023, 10, 15)},
    {"start": datetime(2023, 10, 10), "end": datetime(2023, 10, 24)},
    {"start": datetime(2023, 10, 15), "end": datetime(2023, 10, 29)},
]

reordered_intervals = reorder_intervals(intervals)
print(reordered_intervals)
