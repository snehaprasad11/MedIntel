import pandas as pd

def hospital_overload_risk(appointments, beds):

    dept_load = appointments.groupby("department_id").size()
    bed_capacity = beds.set_index("department_id")["total_beds"]

    risk = {}

    for dept in dept_load.index:
        load = dept_load[dept]
        capacity = bed_capacity.get(dept, 1)

        ratio = load / capacity

        if ratio > 0.85:
            risk[dept] = "HIGH RISK"
        elif ratio > 0.6:
            risk[dept] = "MODERATE"
        else:
            risk[dept] = "NORMAL"

    return risk