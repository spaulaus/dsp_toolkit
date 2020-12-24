# ROOT CERN Pileup Macros

Oscar Naviliat-Cuncic authored these macros.

## Usage

1. Start root: `root`
1. load the macro with the model functions: `.L pileUpModels.C`
2. Then load the macro with the pile-up generator: `.L pileUpGenerator.C`
3. Then run this macro: `.x PileUpDrivGauss.C`

## Files

### PileupDrivGauss.C

Driver to generate the pile-up response of the Pixie module from a gaussian distrubution

### pileUpGenerator.C

Generates a pile-up spectrum from a pdf given by histogram hexp. This macro has to be loaded before
running any driver.

### pileUpModels.C

Define functions for models describing the response of Pixie16 modules to pile-up. The functions are
called by the pileup drivers.

### sample-results.png
Results of executing the scripts.