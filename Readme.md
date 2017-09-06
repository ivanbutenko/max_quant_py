# MaxQuant scripts

# Installation

```bash
cp -r /home/nprian/software/MaxQuant.16013.wiff_fix.cmd <software directory>

git clone http://git.ripcm.com/Prianichnikov/max_quant_py.git
cd max_quant_py
pip3 install --user -U .

cd ..
git clone https://github.com/lpenguin/simple_drmaa_scheduler
cd simple_drmaa_scheduler
pip3 install --user -U .
```

# Updating 
```bash
cd max_quant_py
pip3 install --user -U .
cd ..

cd simple_drmaa_scheduler
pip3 install --user -U .

```
### Add $HOME/.local/bin to $PATH
```bash
# Add line to the bottom of ~/.bash_profile
export PATH=$HOME/.local/bin:$PATH
```
# Usage

## Directory structure
```bash
$ ls -1
data/  # directory with .wiff and .wiff.scan files 
database.fasta@  # link to database (<your software dir>/MaxQuant.16013.wiff_fix.cmd/database.fasta)
MaxQuant@  # link to MaxQuant distribution (<your software dir>/MaxQuant.16013.wiff_fix.cmd)
mqpar.base.xml@  # Link to mqpar base template (<your software dir>/MaxQuant.16013.wiff_fix.cmd/mqpar.base.xml)
```
## Generating `mqpar.gen.xml `with `maxquant-mqpar`
### Getting help
```bash
$ maxquant-mqpar -h
usage: maxquant-mqpar [-h] [-T MQPAR_TEMPLATE] [-d DATABASE] [-t THREADS]
                      [-o OUTPUT]
                      files [files ...]

positional arguments:
  files                 *.wiff files

optional arguments:
  -h, --help            show this help message and exit
  -T MQPAR_TEMPLATE, --mqpar-template MQPAR_TEMPLATE
                        Template mqpar (default: mqpar.base.xml)
  -d DATABASE, --database DATABASE
                        FASTA Database (default: database.fasta)
  -t THREADS, --threads THREADS
                        Num of threads (default: 1)
  -o OUTPUT, --output OUTPUT
                        Output mqpar file (default: mqpar.gen.xml)

```
### Generating `mqpar.gen.xml` file
```bash
maxquant-mqpar -t 20 data/*.wiff 
```

## Generating `batch.json` with `maxquant-batch`
### Getting help
```bash
$ maxquant-batch -h                                                                                                                                                                     13:04:57
usage: maxquant-batch [-h] [-c MQPAR] [-C MAX_QUANT_CMD] [-p CUSTOM_PARAMS]
                      [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -c MQPAR, --mqpar MQPAR
                        mqpar.xml path (default: mqpar.gen.xml)
  -C MAX_QUANT_CMD, --max-quant-cmd MAX_QUANT_CMD
                        MaxQuant Commandline.exe binary (default:
                        MaxQuant/bin/CommandLine.exe)
  -p CUSTOM_PARAMS, --custom-params CUSTOM_PARAMS
  -o OUTPUT, --output OUTPUT
                        Output file, default is stdout (default: None)
```
### Generating `batch.json`
```bash
maxquant-batch -o batch.json                                                                                                  13:08:06
Patching threads=20 for job ...
Patching threads=20 for job ...
```


## Sending jobs to cluster
```bash
# Print list of batches
$ scheduler -d batch.json

# Send to cluster
$ scheduler -S -j <num of simultanious jobs on cluster> batch.json
```

