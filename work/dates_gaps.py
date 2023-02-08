from datetime import datetime, timedelta


def function(data_list, from_date, to_date):
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

    sorted_days = sorted([d['posting_date'] for d in data_list])
    result_as_dict = {row["posting_date"].strftime("%Y-%m-%d"): row for row in data_list}

    mapping = {(from_date + timedelta(days=x)).strftime("%Y-%m-%d"): [] for x in range((sorted_days[0] - from_date).days)}

    for i, day in enumerate(sorted_days):
        next_day = day + timedelta(days=len(range((to_date - day).days))) if (i + 1) == len(sorted_days) else sorted_days[i + 1]

        missing_days = [(day + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((next_day - day).days)]
        mapping[day.strftime("%Y-%m-%d")] = missing_days

    result = []
    for k in mapping:
        for v in mapping[k]:
            _dict = {**result_as_dict[k], "posting_date": v}
            result.append(_dict)

    return data_list

