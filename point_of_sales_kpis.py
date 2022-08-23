# Copyright (c) 2013, Axentor, LLC and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import collections
import functools
import operator
from typing import Dict, Tuple, List
from enum import Enum

import frappe
from frappe import _


###############
class Enums(Enum):
    # TODO: not all code depend on the EnumData
    COMPANY = "company"
    POSTING_DATE = "posting_date"
    SALES_PERSON = "sales_person"
    BRANCH = "branch"
    FROM_DATE = "from_date"
    TO_DATE = "to_date"
    GROUP_BY = "group_by"
    CYCLE_COUNT = "cycle_count"

    # Views
    # View (1)
    DAY_SP = "Day > Sales Person"
    # View (2)
    SP_DAY = "Sales Person > Day"
    # View (3)
    CYCLE_DAY_SP = "Cycle > Day > Sales Person"
    # View (4)
    CYCLE_SP_DAY = "Cycle > Sales Person > Day"
    # View (5)
    SP_CYCLE_DAY = "Sales Person > Cycle > Day"

    # GROUP BY Statements for Query
    BR_DAY_SP = "GROUP BY branch, DATE(posting_date), sales_person"
    BR_SP_DAY = "GROUP BY branch, sales_person, DATE(posting_date)"

    def __str__(self):
        return str(self.value)


def execute(filters=None):
    """
    1. Validate Filters
    2. Build Query, and get data (POS and LostSales)
    3. Structure raw data based on the selected view
    4. Make calculations
    6. Order data
    """
    if not filters:
        return [], []

    validate_filters(filters)

    columns = get_columns()
    result = get_result(filters)

    return columns, result


def get_result(filters):
    conditions = get_conditions(filters)
    group_by_value = filters.get(Enums.GROUP_BY.value)

    # default parameters
    grouping = ""
    the_field = ""
    upper_cy = False
    cycle_count = 0
    if group_by_value == Enums.DAY_SP.value:
        grouping = Enums.BR_DAY_SP.value
        the_field = Enums.POSTING_DATE.value
    elif group_by_value == Enums.SP_DAY.value:
        grouping = Enums.BR_SP_DAY.value
        the_field = Enums.SALES_PERSON.value
    elif group_by_value == Enums.CYCLE_DAY_SP.value:
        grouping = Enums.BR_DAY_SP.value
        the_field = Enums.POSTING_DATE.value
        cycle_count = filters.get(Enums.CYCLE_COUNT.value)
    elif group_by_value == Enums.CYCLE_SP_DAY.value:
        grouping = Enums.BR_SP_DAY.value
        the_field = Enums.SALES_PERSON.value
        cycle_count = filters.get(Enums.CYCLE_COUNT.value)
        upper_cy = True
    elif group_by_value == Enums.SP_CYCLE_DAY.value:
        grouping = Enums.BR_SP_DAY.value
        the_field = Enums.SALES_PERSON.value
        cycle_count = filters.get(Enums.CYCLE_COUNT.value)

    _pos_invoices, _lost_sales = _get_raw_data(conditions, grouping)
    result = make_calculations_and_order_data(
        _pos_invoices, _lost_sales, the_field, cycle_count, upper_cy
    )
    return result


def validate_filters(filters: Dict) -> None:
    """Invalid Filters"""
    if not filters.get(Enums.COMPANY.value):
        frappe.throw(_("{0} is mandatory").format(_("Company")))
    if filters.get(Enums.FROM_DATE.value) > filters.get(Enums.TO_DATE.value):
        frappe.throw(_("From Date must be before To Date"))
    if all(
        [
            not filters.get(Enums.POSTING_DATE.value),
            not filters.get(Enums.FROM_DATE.value),
            not filters.get(Enums.TO_DATE.value),
        ]
    ):
        frappe.throw(
            _("Select specific Day or specify {0} and {1}").format(
                _("From Date"), _("To Date")
            )
        )
    if (
        "Cycle" in filters.get(Enums.GROUP_BY.value)
        and filters.get(Enums.CYCLE_COUNT.value) < 1
    ):
        frappe.throw(_("Cycle count must be Greater than 1"))


def get_conditions(filters: Dict) -> str:
    conditions = [
        f"WHERE docstatus = 1 AND company = '{filters.get(Enums.COMPANY.value)}'"
    ]

    if filters.get(Enums.BRANCH.value):
        conditions.append(f" AND branch = '{filters.get(Enums.BRANCH.value)}'")
    if filters.get(Enums.SALES_PERSON.value):
        conditions.append(
            f" AND sales_person = '{filters.get(Enums.SALES_PERSON.value)}'"
        )

    # if posting_day is specified, then negelct (from /to) dates
    if filters.get(Enums.POSTING_DATE.value):
        conditions.append(
            f" AND posting_date = '{filters.get(Enums.POSTING_DATE.value)}'"
        )
    elif filters.get(Enums.FROM_DATE.value) and filters.get(Enums.TO_DATE.value):
        from_date = filters.get(Enums.FROM_DATE.value)
        to_date = filters.get(Enums.TO_DATE.value)
        conditions.append(
            f""" AND posting_date BETWEEN '{from_date}' AND '{to_date}'"""
        )

    return "".join(condition for condition in conditions)


def get_columns() -> List:
    columns = [
        {
            "label": _("Layout"),
            "fieldname": "layout",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Traffic"),
            "fieldname": "traffic_count",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": _("Conversion Rate"),
            "fieldname": "conversion_rate",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": _("Transactions"),
            "fieldname": "transactions_count",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": _("UPT - Unit Per Transactions"),
            "fieldname": "upt",
            "fieldtype": "Float",
            "width": 80,
        },
        {
            "label": _("APU - AVG Price per Unit"),
            "fieldname": "apu",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": _("ATV - AVG per Transaction"),
            "fieldname": "atv",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": _("Volume"),
            "fieldname": "total_qty",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": _("Value"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 120,
        },
    ]

    return columns


#######################
def _get_raw_data(conditions: str, grouping: str) -> Tuple[List, List]:
    """
    Get POS Invoices and Lost invoices from DB
    """
    _pos_invoices_query_str = f"""
        SELECT
            branch,
            posting_date as posting_date,
            sales_person,
            COUNT(name) as transactions_count,
            SUM(grand_total) as grand_total,
            SUM(total_qty) as total_qty,

            SUM(total_qty)/COUNT(name) as 'upt',
            SUM(grand_total)/SUM(total_qty) as 'apu',
            SUM(grand_total)/COUNT(name) as 'atv'
        FROM `tabPOS Invoice`
        {conditions}
        {grouping}
    """
    _lost_sales_query_str = f"""
        SELECT 
            branch, 
            time as posting_date, 
            sales_person, 
            count(*) as num_lost_sales
        FROM `tabBranch Lost Sale`
        WHERE docstatus = 1
        {grouping}
        """

    _pos_invoices = frappe.db.sql(_pos_invoices_query_str, as_dict=True)
    _lost_sales = frappe.db.sql(_lost_sales_query_str, as_dict=True)

    return _pos_invoices, _lost_sales


def structure_data(rows, the_field):
    """
    Dynamically structure data based on the selected view
    """
    structured_data = collections.defaultdict(
        lambda: collections.defaultdict(
            lambda: collections.defaultdict(collections.defaultdict)
        )
    )
    posting_date = Enums.POSTING_DATE.value
    sales_person = Enums.SALES_PERSON.value
    the_other = sales_person if the_field == posting_date else posting_date
    for row in rows:
        structured_data[row["branch"]][str(row[the_field])][
            str(row[the_other])
        ] = collections.defaultdict(None, row)

    return structured_data


def cycled_data(
    structured_data: Dict, cycle_count: int, the_field: str, upper_cy: bool = False
):
    """
    The main function that cycle data
    TODO: Too much shallow coping data
    :upper_cy: if true we are going to upper the cycle layout above person layout (view 4: branch > Cycle > Person)
    """

    def _generate_slices(len_data: int, _cycle_count: int):
        """
        generate the slices based in the len(of the rows) and the cycle_count
        """
        num_rows = len_data
        reminder = num_rows % _cycle_count
        if reminder == 0:
            _slices = [
                slice(start, start + _cycle_count)
                for start in range(0, num_rows, _cycle_count)
            ]
        else:
            _slices = [
                slice(start, start + _cycle_count)
                for start in range(0, num_rows - reminder, _cycle_count)
            ]
            _slices.append(slice(num_rows - reminder, num_rows))

        return _slices

    def _cycle_data(_data: Dict, _cycle_count: int):
        """
        cycle data
        """
        # shallow copy; to not mutate the original one
        _cycling_data = collections.defaultdict(collections.defaultdict, _data.copy())

        for child in _cycling_data:
            list_structure = [
                collections.defaultdict(dict, {k: v})
                for k, v in _cycling_data[child].items()
            ]
            slices = _generate_slices(len(list_structure), _cycle_count)
            branch_data = collections.defaultdict(dict)
            cycle = 1
            for _slice in slices:
                dict_structure = collections.defaultdict(
                    dict, {k: v for i in list_structure[_slice] for k, v in i.items()}
                )
                branch_data[f"{cycle}"] = collections.defaultdict(dict, dict_structure)
                cycle += 1
            _cycling_data[child] = branch_data

        return _cycling_data

    def _uppering_cycles(_data):
        """
        The `branch > cycle > person > days` View is same as the `branch > person > cycle > days` View, but
        It's a matter of reordering data to upper the cycle layout over the person layout without losing the concept of
        WE ARE BREAK DAYS NOT ANYTHING ELSE
        :_data: is actually the data of the TWIN View, that we are going to reordering it.
        :new_cycling_data: the data after ordering
        """
        # data template
        new_cycling_data = collections.defaultdict(
            collections.defaultdict, {k: {} for k, v in _data.items()}
        )
        for br in _data:
            # get the maximum number of cycles over all the branch data.
            num_cycles = max([int(cy) for sp in _data[br] for cy in _data[br][sp]])
            # Iterate comperhinsoly to add the cycle layout after the branch layout, but without removing the inner
            # cycle layout
            all_br_cycles = collections.defaultdict(
                collections.defaultdict,
                {
                    str(cy): collections.defaultdict(
                        collections.defaultdict,
                        {
                            sp: collections.defaultdict(
                                collections.defaultdict,
                                {
                                    k: v
                                    for k, v in _data[br][sp].items()
                                    if str(k) == str(cy)
                                },
                            )
                            for sp in _data[br]
                        },
                    )
                    for cy in range(1, num_cycles + 1)
                },
            )
            # remove the inner cycle layout for all branch data
            for cy in all_br_cycles:
                for sp in all_br_cycles[cy]:
                    for inner_cy in all_br_cycles[cy][sp]:
                        all_br_cycles[cy][sp] = collections.defaultdict(
                            collections.defaultdict,
                            collections.defaultdict(
                                None, all_br_cycles[cy][sp][inner_cy]
                            ),
                        )

            new_cycling_data[br] = all_br_cycles

        return new_cycling_data

    # shallow copy; to not mutate the original one
    cycling_data = collections.defaultdict(
        collections.defaultdict, structured_data.copy()
    )
    # View (3): branch > Cycle > Day
    if the_field == Enums.POSTING_DATE.value:
        cycling_data = _cycle_data(cycling_data, cycle_count)
    else:
        # View (5): branch > Person > Cycle
        for branch in cycling_data:
            cycling_data[branch] = _cycle_data(cycling_data[branch], cycle_count)
        # View (4): branch > Person > Cycle
        if upper_cy:
            cycling_data = _uppering_cycles(cycling_data)

    return cycling_data


#######################
def sum_values_of_same_key(rows: List) -> Dict:
    """
    functional approach to compute the values of the same keys.
    """

    def _exclude_non_computable_keys(_dict):
        _keys = ("transactions_count", "grand_total", "total_qty", "num_lost_sales")
        _computable_keys = {k: v for k, v in _dict.items() if k in _keys}
        return _computable_keys

    if not rows:
        return {
            "transactions_count": 0,
            "grand_total": 0,
            "total_qty": 0,
            "num_lost_sales": 0,
        }

    result = collections.defaultdict(
        collections.defaultdict,
        dict(
            functools.reduce(
                operator.add,
                map(collections.Counter, map(_exclude_non_computable_keys, rows)),
            )
        ),
    )

    return result


def compute_metrics(total_qty=0, transactions_count=1, grand_total=0, lost_sales=0):
    """
    traffic = num_of_invoices: transactions_count + num_of_lost_sales
    conversion = invoices / traffic_count
    upt = total_qty / transactions_count
    apu = grand_total / total_qty
    atv = upt * apu
    Value = grand_total
    Volume = total_qty
    """
    traffic_count = transactions_count + lost_sales
    conversion_rate = transactions_count / traffic_count if traffic_count > 0 else 0
    upt = total_qty / transactions_count if transactions_count > 0 else 0
    apu = grand_total / total_qty if total_qty > 0 else 0
    atv = upt * apu

    result = {
        "traffic": traffic_count,
        "conversion": conversion_rate,
        "upt": upt,
        "apu": apu,
        "atv": atv,
        "value": grand_total,
        "volume": total_qty,
    }

    return result


def prepare_data_to_append(level_name, level, level_data):
    """
    Prepare record
    """
    total_qty = level_data.get("total_qty", 0)
    transactions_count = level_data.get("transactions_count", 0)
    grand_total = level_data.get("grand_total", 0)
    lost_sales = level_data.get("num_lost_sales", 0)
    metrics = compute_metrics(total_qty, transactions_count, grand_total, lost_sales)

    record = {
        "layout": level_name,
        "indent": level,
        "traffic_count": metrics.get("traffic", 0),
        "conversion_rate": metrics.get("conversion", 0),
        "transactions_count": transactions_count,
        "upt": metrics.get("upt", 0),
        "apu": metrics.get("apu", 0),
        "atv": metrics.get("atv", 0),
        "grand_total": metrics.get("value", 0),
        "total_qty": metrics.get("volume", 0),
    }
    return record


def recur_calculate_totals(structured_data):
    """
    recursively calculate all level calculations.
    """
    # shallow copy; to not mutate the original one
    totals_data = collections.defaultdict(
        collections.defaultdict, structured_data.copy()
    )

    parent = []
    for child in totals_data:
        if isinstance(totals_data[child], (collections.defaultdict, dict)):
            child_calculations = recur_calculate_totals(totals_data[child])
            totals_data[child] = collections.defaultdict(
                collections.defaultdict, dict(totals_data[child], **child_calculations)
            )

            parent.append(
                collections.defaultdict(collections.defaultdict, totals_data[child])
            )
        else:
            return collections.defaultdict(collections.defaultdict)

    parent_calcs = sum_values_of_same_key(parent)
    totals_data = collections.defaultdict(
        collections.defaultdict, dict(totals_data, **parent_calcs)
    )

    return totals_data


def recur_order_data(pos_data, pos_totals, lost_totals, level, container):
    """
    recursively order data
    """
    # shallow copy; to not mutate the original one
    pos_data = collections.defaultdict(collections.defaultdict, pos_data.copy())
    pos_totals = collections.defaultdict(collections.defaultdict, pos_totals.copy())
    lost_totals = collections.defaultdict(collections.defaultdict, lost_totals.copy())

    for child in pos_data:
        if isinstance(pos_data[child], (collections.defaultdict, dict)):
            pos_data[str(child)]["num_lost_sales"] = lost_totals[str(child)].get(
                "num_lost_sales", 0
            )
            record = prepare_data_to_append(child, level, pos_totals[str(child)])
            container.append(record)

            recur_order_data(
                pos_data[str(child)],
                pos_totals[str(child)],
                lost_totals[str(child)],
                level + 1,
                container,
            )
        else:
            return collections.defaultdict(collections.defaultdict)

    return container


def make_calculations_and_order_data(
    _pos_invoices, _lost_sales, the_field, cycle_count=0, upper_cy=False
):
    """
    the main function that do the following for all the views:
        1. prepare the data structure
        2. calculate totals, recursively
        3. order data, recursively
    """
    classified_pos_data = structure_data(_pos_invoices, the_field)
    classified_lost_sales = structure_data(_lost_sales, the_field)

    if cycle_count > 0:
        classified_pos_data = cycled_data(
            classified_pos_data, cycle_count, the_field, upper_cy
        )
        classified_lost_sales = cycled_data(
            classified_lost_sales, cycle_count, the_field, upper_cy
        )

    pos_totals = recur_calculate_totals(classified_pos_data)
    lost_totals = recur_calculate_totals(classified_lost_sales)

    return recur_order_data(classified_pos_data, pos_totals, lost_totals, 0, list())
