#!/bin/bash -e
#
# Copyright (c) 2024. Christopher Queen Consulting LLC (http://www.ChristopherQueenConsulting.com/)
#

#############################################

poetry export --without-hashes --format=requirements.txt > requirements.txt