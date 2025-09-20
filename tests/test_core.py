import subprocess, sys, pathlib, os

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT/ "src"
ENV =  dict(os.environ, PYTHONPATH=str(SRC))

def run_cli(input_rel, mode):
    env = dict(os.environ, PYTHONPATH=str(SRC))
    cmd = [sys.executable, "-m", "pnl_calculator.cli", str(ROOT / input_rel), mode]
    res = subprocess.run(cmd,capture_output=True, text=True, check=True, env=ENV)
    return res.stdout.strip()

def test_fifo_sample_matches_expected():
    out = run_cli("sample_data/trades.csv", "fifo")
    expected = (ROOT / "expected_outputs" / "fifo.csv").read_text().strip()
    assert out == expected

def test_lifo_sample_matches_expected():
    out = run_cli("sample_data/trades.csv", "lifo")
    expected = (ROOT / "expected_outputs" / "lifo.csv").read_text().strip()
    assert out == expected

def test_multiple_symbols_interleaved():
    csv_text = """TIMESTAMP,SYMBOL,BUY_OR_SELL,PRICE,QUANTITY
1,AAA,B,10.00,10
2,BBB,B,20.00,5
3,AAA,S,12.00,10
4,BBB,S,21.00,5
"""
    p = ROOT / "sample_data" / "tmp.csv"
    p.write_text(csv_text)
    out = run_cli("sample_data/tmp.csv", "fifo")
    lines = out.splitlines()
    assert lines[0] == "TIMESTAMP,SYMBOL,PNL"
    assert lines[1] == "3,AAA,20.00"
    assert lines[2] == "4,BBB,5.00"
