"""
Tests for Plotly integration in analysis module.
"""
import os
import tempfile
from analysis import create_category_chart_plotly


def test_plotly_chart_returns_figure(tmp_path):
    # Create simple CSV
    fp = tmp_path / "data.txt"
    with open(fp, 'w', encoding='utf-8') as f:
        f.write("Food,10.00,Lunch\n")
        f.write("Rent,20.00,Monthly\n")
    fig = create_category_chart_plotly(str(fp))
    # Basic checks
    assert hasattr(fig, 'data')
    assert len(fig.data) > 0
    # Ensure categories present in y axis
    ys = [d['y'] for d in fig.data]
    assert any('Food' in str(y) or 'Rent' in str(y) for y in ys)
