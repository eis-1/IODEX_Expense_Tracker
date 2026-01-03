"""
GUI tests for preferences and timestamp display. Uses headless Tkinter.
"""
import os
import tempfile
import tkinter as tk
import pytest
from gui import ExpenseTrackerGUI
import storage
import config


def test_preferences_persist_and_affect_display(tmp_path):
    # Setup a temp file and temp config
    temp_file = os.path.join(tmp_path, 'test.txt')
    cfg_path = os.path.join(tmp_path, 'config.json')

    # Ensure clean config path
    cfg = {'timestamp_mode': 'utc', 'custom_format': '%Y-%m-%d %H:%M:%S %Z', 'show_relative': False}
    config.save_config(cfg, path=cfg_path)

    # Append an expense with known timestamp
    timestamp = '2026-01-03T12:00:00+00:00'
    storage.append_expense('Food', 10.0, 'Lunch', path=temp_file, timestamp=timestamp)

    # Launch GUI headless
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tkinter not available in this environment")
    app = ExpenseTrackerGUI(root, filepath=temp_file)
    # Override config to use our temp config file
    app.config = config.load_config(path=cfg_path)

    # Call view_expenses and inspect the tree content
    app.view_expenses()
    # Find the Treeview widget
    tree = None
    for w in root.winfo_children():
        if hasattr(w, 'get_children'):
            tree = w
            break
    assert tree is not None
    items = tree.get_children()
    assert len(items) == 1
    vals = tree.item(items[0])['values']
    # Since we set UTC and no relative time, expect 'UTC' in the string
    assert 'UTC' in vals[3] or '+00:00' in vals[3]
    root.destroy()


def test_preferences_preview_updates(tmp_path):
    # Use temp config and open preferences
    cfg_path = os.path.join(tmp_path, 'config.json')
    config.save_config({'timestamp_mode': 'local', 'custom_format': '%Y-%m-%d %H:%M:%S %Z', 'show_relative': True}, path=cfg_path)

    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError:
        pytest.skip("Tkinter not available in this environment")
    app = ExpenseTrackerGUI(root)
    app.config = config.load_config(path=cfg_path)

    # Use the compute_preview_text helper to avoid needing a real Tk in the test
    preview = ExpenseTrackerGUI.compute_preview_text('2026-01-03T12:00:00+00:00', 'utc', '%Y-%m-%d %H:%M:%S %Z', False, tz_name='UTC')
    assert 'UTC' in preview or '+00:00' in preview
