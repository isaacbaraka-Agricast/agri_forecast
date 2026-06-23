with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        peak_date         = start_date + timedelta(weeks=peak_week)
        plant_by_date     = peak_date - timedelta(weeks=grow_weeks)
        # Use next season date if plant_by_date already passed
        today = datetime.today().date()
        plant_by_date = plant_by_date.date() if hasattr(plant_by_date, 'date') else plant_by_date
        if plant_by_date < today:
            next_plant = today.replace(month=9, day=1) if today.month < 9 else today.replace(year=today.year+1, month=3, day=1)
            weeks_until_plant = max(0, (next_plant - today).days // 7)
            plant_by_date = next_plant"""

new = """        # Step 1: figure out the REAL next planting opportunity first
        today = datetime.today().date()
        naive_peak_date     = start_date + timedelta(weeks=peak_week)
        naive_plant_by_date = (naive_peak_date - timedelta(weeks=grow_weeks))
        naive_plant_by_date = naive_plant_by_date.date() if hasattr(naive_plant_by_date, 'date') else naive_plant_by_date

        if naive_plant_by_date >= today:
            # The naive plan still works: plant now, ready in time for this near-term peak
            plant_by_date     = naive_plant_by_date
            weeks_until_plant = max(0, (plant_by_date - today).days // 7)
        else:
            # Naive window already passed -> push planting to the next real season
            next_plant = today.replace(month=9, day=1) if today.month < 9 else today.replace(year=today.year+1, month=3, day=1)
            plant_by_date     = next_plant
            weeks_until_plant = max(0, (next_plant - today).days // 7)

        # Step 2: NOW recompute the best-sell week relative to when the crop will
        # actually be ready to sell (plant_by_date + grow_weeks), not from today.
        harvest_ready_date = plant_by_date + timedelta(weeks=grow_weeks)
        weeks_to_harvest    = max(0, (harvest_ready_date - today).days // 7)
        # Search for the peak demand week starting from the harvest-ready point,
        # within the forecast horizon we generated (re-using the same demands list,
        # offset so we don't recommend selling before the crop even exists).
        searchable = [(i, d) for i, d in enumerate(demands) if i >= weeks_to_harvest]
        if searchable:
            peak_idx, _   = max(searchable, key=lambda t: t[1])
            peak_week     = peak_idx + 1
        else:
            # Harvest is beyond our forecast horizon -- best estimate is the
            # harvest-ready week itself (first realistic sell opportunity).
            peak_week = weeks_to_harvest + 1
        peak_date = start_date + timedelta(weeks=peak_week - 1)"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
