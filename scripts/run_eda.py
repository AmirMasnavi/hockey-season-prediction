"""Execute and verify the introductory notebook, or check its saved outputs."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='Verify saved outputs without execution')
args = parser.parse_args()
for folder in [ROOT / '.mplconfig', ROOT / '.jupyter' / 'ipython', ROOT / '.jupyter' / 'runtime']:
    folder.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.mplconfig'))
os.environ.setdefault('IPYTHONDIR', str(ROOT / '.jupyter' / 'ipython'))
os.environ.setdefault('JUPYTER_RUNTIME_DIR', str(ROOT / '.jupyter' / 'runtime'))

import nbformat

manifest = json.loads((ROOT / 'reports/eda/source_sha256.json').read_text())
for filename, expected in manifest.items():
    actual = hashlib.sha256((ROOT / 'hockey_development_data' / filename).read_bytes()).hexdigest()
    assert actual == expected, f'Source data differs from baseline: {filename}'
path = ROOT / 'notebooks/01_data_understanding.ipynb'
notebook = nbformat.read(path, as_version=4)
if not args.check:
    from jupyter_client import KernelManager
    from nbclient import NotebookClient

    manager = KernelManager(kernel_name='python3')
    manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    try:
        NotebookClient(notebook, km=manager, timeout=120,
                       resources={'metadata': {'path': str(ROOT)}}).execute()
    finally:
        manager.shutdown_kernel(now=True)
        nbformat.write(notebook, path)

nbformat.validate(notebook)
code_count = 0
figure_count = 0
for index, cell in enumerate(notebook.cells):
    if cell.cell_type != 'code':
        continue
    code_count += 1
    assert 0 < index < len(notebook.cells) - 1
    assert notebook.cells[index - 1].cell_type == 'markdown'
    assert notebook.cells[index + 1].cell_type == 'markdown'
    assert cell.execution_count is not None, f'Unexecuted cell: {index}'
    assert not any(output.output_type == 'error' for output in cell.outputs), f'Cell error: {index}'
    figure_count += sum('image/png' in output.get('data', {}) for output in cell.outputs)
assert notebook.cells[-1].source.startswith('## Final conclusion')
assert all(hashlib.sha256((ROOT / 'hockey_development_data' / name).read_bytes()).hexdigest() == expected
           for name, expected in manifest.items())
print(f'Verified {code_count} executed code cells, {figure_count} figures, markdown sandwiches, '
      f'final conclusion, and {len(manifest)} unchanged source files.')
