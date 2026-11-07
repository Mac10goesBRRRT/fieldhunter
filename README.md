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
python src/fh-relaxed.py input/maxdiff-fromOrig/dns_ictf2010-new_maxdiff-100.pcap
```

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



