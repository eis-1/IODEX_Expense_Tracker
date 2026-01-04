import csv
import os
from matplotlib.figure import Figure

import matplotlib
matplotlib.use('Agg')

import pytest

from analysis import get_category_totals, get_category_totals_db, create_category_chart, get_summary_stats
from database import ExpenseDatabase


def write_csv_rows(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for r in rows:
            writer.writerow(r)


def test_get_category_totals_csv_and_db(tmp_path):
    rows = [
        ('Food', '10.0', 'Lunch', '2026-01-01T10:00:00+00:00'),
        ('Rent', '500.0', 'January rent', '2026-01-01T00:00:00+00:00'),
        ('Food', '5.5', 'Snack', '2026-01-02T12:00:00+00:00'),
    ]

    csv_path = str(tmp_path / 'expenses.txt')
    write_csv_rows(csv_path, rows)

    totals_csv = get_category_totals(csv_path)
    assert isinstance(totals_csv, dict)
    assert totals_csv == {'Food': 15.5, 'Rent': 500.0}

    db_path = str(tmp_path / 'expenses.db')
    db = ExpenseDatabase(db_path)
    for cat, amt, desc, ts in rows:
        db.append_expense(cat, float(amt), desc, timestamp=ts)

    totals_db = get_category_totals_db(db)
    assert isinstance(totals_db, dict)
    assert totals_db == {'Food': 15.5, 'Rent': 500.0}


def test_create_category_chart_csv_and_db_return_figure(tmp_path):
    rows = [
        ('Food', '10.0', 'Lunch', '2026-01-01T10:00:00+00:00'),
        ('Rent', '500.0', 'January rent', '2026-01-01T00:00:00+00:00'),
    ]

    csv_path = str(tmp_path / 'expenses.txt')
    write_csv_rows(csv_path, rows)

    fig = create_category_chart(csv_path)
    assert isinstance(fig, Figure)

    db_path = str(tmp_path / 'expenses.db')
    db = ExpenseDatabase(db_path)
    for cat, amt, desc, ts in rows:
        db.append_expense(cat, float(amt), desc, timestamp=ts)

    fig_db = create_category_chart(db_path)
    assert isinstance(fig_db, Figure)


def test_get_summary_stats_csv_and_db(tmp_path):
    rows = [
        ('Food', '10.0', 'Lunch', '2026-01-01T10:00:00+00:00'),
        ('Rent', '500.0', 'January rent', '2026-01-01T00:00:00+00:00'),
        ('Food', '5.0', 'Snack', '2026-01-02T12:00:00+00:00'),
    ]

    csv_path = str(tmp_path / 'expenses.txt')
    write_csv_rows(csv_path, rows)

    stats_csv = get_summary_stats(csv_path)
    assert stats_csv['total'] == pytest.approx(10.0 + 500.0 + 5.0)
    assert stats_csv['count'] == 3
    assert stats_csv['max_category'] == 'Rent'

    db_path = str(tmp_path / 'expenses.db')
    db = ExpenseDatabase(db_path)
    for cat, amt, desc, ts in rows:
        db.append_expense(cat, float(amt), desc, timestamp=ts)

    stats_db = get_summary_stats(db_path)
    assert stats_db['total'] == pytest.approx(10.0 + 500.0 + 5.0)
    assert stats_db['count'] == 3
    assert stats_db['max_category'] == 'Rent'
