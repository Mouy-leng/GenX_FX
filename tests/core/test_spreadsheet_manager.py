import asyncio
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from unittest.mock import MagicMock, patch, mock_open

# Make sure the core module is in the path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.spreadsheet_manager import SpreadsheetManager

@pytest.fixture
def mock_config():
    """Provides a mock configuration for the SpreadsheetManager."""
    return {
        "output_directory": "test_signal_output",
        "update_interval": 60,
        "max_signals": 10,
        "formats": {
            "excel": True,
            "csv": True,
            "json": True,
            "mt4_csv": True,
            "mt5_csv": True,
        },
        "include_account_info": True,
        "include_market_data": True,
        "backup_enabled": True,
    }

@pytest.fixture
def manager(mock_config, tmp_path):
    """Initializes a SpreadsheetManager instance in a temporary directory."""
    # Patch the output directory to use a temporary path
    mock_config["output_directory"] = tmp_path / "signal_output"
    return SpreadsheetManager(mock_config)

@pytest.mark.asyncio
async def test_initialization(manager):
    """Tests that the SpreadsheetManager initializes correctly."""
    assert manager.output_dir.exists()
    assert manager.backup_dir.exists()
    await manager.initialize()
    # Check that initial files are created
    assert manager.excel_file.exists()
    assert manager.csv_file.exists()
    assert manager.json_file.exists()

@pytest.mark.asyncio
async def test_update_signals(manager):
    """Tests that signals are updated correctly."""
    await manager.initialize()
    signals = [
        {
            "Magic": 1, "Symbol": "EURUSD", "Signal": "BUY", "EntryPrice": 1.1,
            "StopLoss": 1.0, "TakeProfit": 1.2, "Timestamp": datetime.now().isoformat()
        }
    ]
    await manager.update_signals(signals)
    assert len(manager.active_signals) == 1
    assert 1 in manager.active_signals

@pytest.mark.asyncio
async def test_excel_file_update(manager):
    """Tests that the Excel file is updated with new signals."""
    with patch("openpyxl.load_workbook") as mock_load_workbook:
        mock_workbook = MagicMock()
        mock_load_workbook.return_value = mock_workbook
        await manager.initialize()
        signals = [{"Magic": 1, "Symbol": "EURUSD", "Signal": "BUY"}]
        await manager.update_signals(signals)
        mock_workbook.save.assert_called_with(manager.excel_file)

@pytest.mark.asyncio
async def test_csv_file_update(manager):
    """Tests that CSV files are updated correctly."""
    m_open = mock_open()
    with patch("builtins.open", m_open):
        await manager.initialize()
        signals = [{"Magic": 1, "Symbol": "EURUSD", "Signal": "BUY"}]
        await manager.update_signals(signals)
        # Check that the main CSV and MT4/5 CSVs were written to
        m_open.assert_any_call(manager.csv_file, "w", newline="")
        m_open.assert_any_call(manager.mt4_file, "w", newline="")
        m_open.assert_any_call(manager.mt5_file, "w", newline="")


@pytest.mark.asyncio
async def test_json_file_update(manager):
    """Tests that the JSON file is updated with new signals."""
    m_open = mock_open()
    with patch("builtins.open", m_open):
        await manager.initialize()
        signals = [{"Magic": 1, "Symbol": "EURUSD", "Signal": "BUY"}]
        await manager.update_signals(signals)
        m_open.assert_any_call(manager.json_file, "w")

@pytest.mark.asyncio
async def test_signal_cleanup(manager):
    """Tests that old signals are cleaned up correctly."""
    await manager.initialize()
    # Add an old signal
    old_time = (datetime.now() - timedelta(hours=25)).strftime('%Y-%m-%d %H:%M:%S')
    manager.active_signals[1] = {"CreatedTime": old_time, "ID": 1}
    await manager._cleanup_old_signals()
    assert 1 not in manager.active_signals

@pytest.mark.asyncio
async def test_get_signal_summary(manager):
    """Tests that the signal summary is generated correctly."""
    await manager.initialize()
    signals = [
        {"Magic": 1, "Symbol": "EURUSD", "Signal": "BUY", "Confidence": 0.8},
        {"Magic": 2, "Symbol": "GBPUSD", "Signal": "SELL", "Confidence": 0.7},
    ]
    await manager.update_signals(signals)
    summary = manager.get_signal_summary()
    assert summary["total_signals"] == 2
    assert summary["buy_signals"] == 1
    assert summary["sell_signals"] == 1
    assert summary["average_confidence"] == 0.75