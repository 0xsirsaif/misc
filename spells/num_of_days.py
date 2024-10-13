from datetime import datetime, timedelta

days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

# def count_weekdays_in_date_range(start_date, end_date):
#     """
#     Count the number of each weekday in the specified date range.
#     """
#     total_days = (end_date - start_date).days + 1
#     days_per_weekday = total_days // 7
#     remaining_days = total_days % 7

#     print(">>>", total_days, days_per_weekday, remaining_days)
#     weekday_count = {
#         "sunday": days_per_weekday,
#         "monday": days_per_weekday,
#         "tuesday": days_per_weekday,
#         "wednesday": days_per_weekday,
#         "thursday": days_per_weekday,
#         "friday": days_per_weekday,
#         "saturday": days_per_weekday,
#     }

#     # Distribute any remaining days as evenly as possible
#     current_date = start_date
#     delta = timedelta(days=1)

#     while remaining_days > 0:
#         day_name = current_date.strftime("%A").lower()
#         weekday_count[day_name] += 1
#         current_date += delta
#         remaining_days -= 1

#     return weekday_count


# start_date = datetime(2023, 1, 1)
# end_date = datetime(2023, 1, 31)

# result = count_weekdays_in_date_range(start_date, end_date)
# print(result)


# def count_weeks_in_date_range(start_date, end_date):
#     """
#     Count the number of weeks in the specified date range.
#     """
#     delta = end_date - start_date
#     weeks = round(delta.days / 7)
#     return weeks


# result = count_weeks_in_date_range(start_date, end_date)
# print(result)


# def count_weeks_in_date_range(start_date, end_date):
#     week_duration = timedelta(days=6)
#     weeks_count = 0

#     while start_date <= end_date:
#         if start_date + week_duration <= end_date:
#             weeks_count += 1
#         start_date += week_duration
#     return weeks_count

# Example usage:
start_date = datetime(2023, 10, 28)
end_date = datetime(2023, 11, 4)
print(f"{start_date} > {end_date}")
# weeks = count_weeks_in_date_range(start_date, end_date)
# print(f"{weeks}")

print("===================")


# def count_weekdays_in_date_range(start_date, end_date):
#     weeks_count = count_weeks_in_date_range(start_date, end_date)
#     weekdays_count = {day: weeks_count for day in days}
#     return weekdays_count


# # Example usage:
# result = count_weekdays_in_date_range(start_date, end_date)
# print(result)



def count_weeks_and_remaining_range(start_date, end_date):
    week_duration = timedelta(days=7)
    weeks_count = 0
    remaining_range = None

    while start_date <= end_date:
        if start_date + week_duration <= end_date:
            weeks_count += 1
        else:
            remaining_range = (start_date, end_date)
            break
        start_date += week_duration

    return weeks_count, remaining_range


def count_weekdays_in_date_range(start_date, end_date):
    weeks_count, remaining_range = count_weeks_and_remaining_range(start_date, end_date)
    weekdays_count = {day: weeks_count for day in days}

    if remaining_range:
        current_date = remaining_range[0]
        end_date = remaining_range[1]
        delta = timedelta(days=1)

        while current_date <= end_date:
            day_name = current_date.strftime("%A").lower()
            weekdays_count[day_name] += 1
            current_date += delta

    return weekdays_count


# Example usage:
result = count_weeks_and_remaining_range(start_date, end_date)
print(result)

print("===================")

result = count_weekdays_in_date_range(start_date, end_date)
print(result)