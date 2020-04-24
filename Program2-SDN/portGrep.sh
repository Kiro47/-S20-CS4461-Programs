#!/bin/sh
ss -plunt | grep -i -E 'controller|routing|switch'
