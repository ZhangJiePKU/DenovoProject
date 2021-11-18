# Author: AnNi/LuanXuke
# Update time: 20211117 pm

# Usage: python CalculateISOR.py -g XX.gpe -b XX.bam

import sys
import argparse
import pysam
import time


def main(g, b, o):
    samfile = pysam.AlignmentFile(b, "rb")
    regiondp = {}
    regiondn = {}
    strand = {}
    startd = {}
    endd = {}
    chromd = {}
    startda = {}
    endda = {}

    for line in g:
        name = line.split()[11]
        chrom = line.split()[1]
        stran = line.split()[2]
        star = int(line.split()[3])
        en = int(line.split()[4])
        startda.setdefault(name, []).append(star)
        endda.setdefault(name, []).append(en)
        strand[name] = stran
        chromd[name] = chrom

    for key in startda:
        startd[key] = sorted(startda[key])[0]
    for key in endda:
        endd[key] = sorted(endda[key])[-1]
    for key in startd:
        if strand[key] == "+":
            regiondp[key] = chromd[key] + ':' + str(startd[key]) + '-' + str(endd[key])
        else:
            regiondn[key] = chromd[key] + ':' + str(startd[key]) + '-' + str(endd[key])
    isor_ratio = {}
    covl = {}
    for key in regiondp:
        skiplen = 0
        covlen = 0
        for read in samfile.fetch(region=regiondp[key]):
            if read.flag == 83 or read.flag == 163:
                covlen += read.get_overlap(startd[key], endd[key])
        covl[key] = covlen
    for key in regiondn:
        skiplen = 0
        covlen = 0
        for read in samfile.fetch(region=regiondn[key]):
            if read.flag == 99 or read.flag == 147:
                covlen += read.get_overlap(startd[key], endd[key])   
        covl[key] = covlen

    for key in covl:
        try:
            pline = key + '\t' + str(covl[key]) + '\n'
            o.write(pline)
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('-g', type=argparse.FileType('r'), help="The gpe file.")
    parser.add_argument('-b', help="The bam file.")
    parser.add_argument('-o', nargs="?", type=argparse.FileType('w'), default=sys.stdout, help="The output ratio.")
    args = parser.parse_args()
    main(g=args.g, b=args.b, o=args.o)

