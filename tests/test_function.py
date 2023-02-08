import pytest
import datetime
from work.dates_gaps import function


def dict_parametrize(data, **kwargs):
    args = list(list(data.values())[0].keys())
    formatted_data = [[item[a] for a in args] for item in data.values()]
    ids = list(data.keys())
    return pytest.mark.parametrize(args, formatted_data, ids=ids, **kwargs)


a = {'2022-04-01': {'warehouse': 'MBRHB - POS - BFG', 'item_code': '3600542064934',
                    'posting_date': datetime.date(2022, 4, 1), 'qty_after_transaction': 5.0}}


@dict_parametrize({
    # "from < first": {},
    # "from = first": {},
    # "to = last": {},
    # "to > last": {},
    "all": {
        "data": [
            {"posting_date": "2022-04-10"},
            {"posting_date": "2022-04-12"},
            {"posting_date": "2022-04-14"},
            {"posting_date": "2022-04-15"}
        ],
        "from_date": "2022-04-01",
        "to_date": "2022-04-20"
    },
})
def test_function(data, from_date, to_date):
    result = function(data, from_date, to_date)
    print(result)
