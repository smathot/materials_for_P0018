# Analysis recipe

## Usage note

This analysis recipe is provided so that the original analysis can be replicated, and so that further analyses can be performed by third parties with the required expertise. However, there is some fairly heavy scripting involved, which has been written for personal use, relies on custom libraries, and is not extensively documented. Therefore, this analysis recipe is provided *as is*.

## Dependencies

- python
- numpy
- scipy
- matplotlib
- exparser
- R

## Folder structure

- `analyze.py` is the main analysis script.
- `analysis/*.py` is the Python package that contains the actual analysis scripts.
- `edf/*.edf` contains the original `.edf` per-participant data files as recorded by the EyeLink.
- `data/ratings.csv` contains the participants' subjective ratings.

The following folders are filled with intermediate files by the analysis scripts, but are not necessary to run the analysis from scratch (and therefore not included in the repository).

- `data/events/` will contain the converted data files in `.asc` format with events only.
- `data/samples+events/` will contain the converted data files in `.asc` format with events and samples.
- `output/` will contain data summaries in `.csv` format.
- `plots/` will contain data plots.
- `traces/` will contain the eye-movement sample traces in `.npy` format.

## Analysis recipe

### Convert `.edf` data to `.asc` data

The EyeLink provides `.edf` files as output. These are not easily readable, but can be converted to a text-based `.asc` format, with the utility `edf2asc`.

Command:

	edf2asc edf/*.edf
	mv edf/*.asc data/samples+events
	edf2asc -e edf/*.edf
	mv edf/*.asc data/events


### Perform full analysis

The actual analysis is performed by the script `analyze.py`, which takes various optional parameters. The commands below correspond to the analysis as reported in the manuscript. For further details, please refer to the source code of the analysis scripts.

Command:

	python analyze.py @full

During the analysis, intermediate results are cached and saved in the hidden subfolder `.cache`. To run a clean analysis (i.e. without using the cache) either delete the `.cache` folder or run:

Command:

	python analyze.py @full --no-cache
