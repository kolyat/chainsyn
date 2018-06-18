# chainsyn

**chainsyn** (from '*chain synthesis*') is a simple simulator for genome
bioinformatics. It supports:
- Replication (DNA to DNA)
- Transcription (DNA to RNA)
- Translation (RNA to protein)

Several front-ends are available: text terminal and web interface.

Input of required data can be done manually or via text file in FASTA
format.

Program can collect some statistics about available data:
- Number of nucleotides
- Number of codons
- GC-content %
- Protein's mass

### Requirements

- Python 3.4 or higher
- Packages listed in ```requirements.txt```. Use

    ```bash
    pip3 install -r requirements.txt
    ```
    
    **Note**: if you're running Windows, use ```unicurses``` instead.
    
### Usage

Run ```term.py``` for usage from command line.

Run ```web.py``` to start web server on port 5555 (by default). If you're
running locally, web interface is accessible by link
```text
localhost:5555
```
