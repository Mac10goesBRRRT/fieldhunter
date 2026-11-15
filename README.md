# FieldHunter

Docker-Packaged version of Fieldhunter to be able to reliably run it on different machines. The Code itself wasnt changed.

## Setup

```sh
docker run --rm -it -e HOME=/tmp \
    -v "$PWD/input":/app/input \
    -v "$PWD/reports":/app/reports \
    cuacuac/fieldhunter:master
# then run the python scripts with whatever input you want
python src/fh.py input/maxdiff-fromOrig/dns_ictf2010-new_maxdiff-100.pcap
# or with the newer, improved heuristics
python src/fh_relaxed.py input/maxdiff-fromOrig/dns_ictf2010-new_maxdiff-100.pcap
```

## Raw inferred fields per message

Both scripts support exporting inference results independently of ground truth:

```sh
python src/fh_relaxed.py input/capture.pcap --export-raw reports/raw-fields.json --no-evaluation
# The same options work with src/fh.py.
```

The JSON contains the input PCAP path and a `messages` array. Each imported
message includes its ID, timestamp (Unix seconds), source/destination IP and port,
transport protocol, complete `payload_hex`, and a `fields` array. Each field has
`type`, `offset`, `length`, `end`, and `hex`. Offsets are zero-based byte offsets
into the TCP/UDP payload, and `end` is exclusive.

All inferred candidates are retained, including overlapping fields of different
types. Messages without inferred fields have an empty `fields` array. No
ground-truth labels or correctness filtering are applied.

`message_index` is the 1-based position in the imported message list, **not** a
PCAP frame number: packets ignored by the loader (e.g. those without payload)
are not exported. Identical payloads in distinct imported messages remain separate.

`--no-evaluation` skips ground-truth comparison and all evaluation reports;
omit it to export raw fields and also run the usual evaluation. Existing behavior
is unchanged when neither option is supplied.

## Original Text

Re-implementation of parts of the protocol reverse engineering approach FieldHunter (FH) as proposed in 

> Bermudez, Ignacio, Alok Tongaonkar, Marios Iliofotou, Marco Mellia, und Maurizio M. Munafò. 
> „Towards Automatic Protocol Field Inference“. Computer Communications 84 (15. Juni 2016). 
> https://doi.org/10.1016/j.comcom.2016.02.015.

Written by Stephan Kleber <stephan.kleber@uni-ulm.de>
who also proposed some improvements for the field heuristics in 
`inference/fieldtypesRelaxed.py`
used by
`src/fh_relaxed.py`
for evaluation to be run by
`eval-fh-relaxed.sh`.

The original FieldHunter heuristics are run via
`eval-fh.sh`.

It only implements FH's binary message handling using n-grams (not textual using delimiters!)


Statistics about traces can be gained by
`eval-traces.sh`.

Not sure about a licence right now.

## Installation

Clone the repository including the nemere submodule:
```git clone --recurse-submodules git@github.com:vs-uulm/nemesys.git```

## Building
Local building of the container
```docker build -t fieldhunter .```


## Running
```sudo docker run --rm -it -v "$PWD":/app fieldhunter```


