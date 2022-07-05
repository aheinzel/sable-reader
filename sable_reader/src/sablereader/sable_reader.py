#!/usr/bin/env python

import sys
import re
from collections import namedtuple


SableResult = namedtuple("SableResult", "header seq ss sa")


def _strip(s):
    return s.strip("\n").strip("\r")


def _strip_leading_ws(s):
    return re.sub(r" +", "", s)


def _read_section(f):
    seq = ""
    annot = ""
    conf = ""
    in_seq = False
    for l in f:
        l = _strip(l)
        if l.startswith(">"):
            in_seq = True
            seq += _strip_leading_ws(_strip(next(f)))
            annot += _strip_leading_ws(_strip(next(f)))
            conf += _strip_leading_ws(_strip(next(f)))
        elif l.startswith("END_SECTION"):
            return seq, annot, conf
        elif in_seq:
            assert(l == "")

    assert(False)


def read_sable(f):
    header = None
    seq = None
    ss = None
    sa = None
    for l in f:
        l = _strip(l)
        if l.startswith("Query:"):
            if header != None:
                yield SableResult(header, seq, ss, sa)

            header = l.replace("Query: ", "")
            seq = None
            ss = None
            sa = None

        if l == "SECTION_SS":
            assert(header != None)
            assert(ss == None)
            ss_seq, ss_annot, ss_conf = _read_section(f)
            assert(seq == None or seq == ss_seq)
            seq = ss_seq
            ss = ss_annot

        if l == "SECTION_SA":
            assert(header != None)
            assert(sa == None)
            sa_seq, sa_annot, sa_conf = _read_section(f)
            assert(seq == None or seq == sa_seq)
            seq = sa_seq
            sa = sa_annot

    if header != None:
        yield SableResult(header, seq, ss, sa)
