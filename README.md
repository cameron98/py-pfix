# Py-PFIX

Welcome to py-pfix, my implementation of the [RFC 7011](https://datatracker.ietf.org/doc/html/rfc7011) IPFIX spec in python. This project will only act as an IPFIX collector and will not be getting functionality to send IPFIX records.

## Getting Started

This project is written wholy in Python and has been tested on Python 3.12. To get started simply clone the project, move to the src directory and run the main.py file. The server will listen on UDP port 5000 by default and create a file named ipfix_out.json which ipfix records will be written to.
