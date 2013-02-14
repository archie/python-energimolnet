# Python lib for Energimolnet

*Version 1.0*

A library to help develop against Energimolnet.se API.

For more information see http://app.energimolnet.se/api/1.0/Documentation

## Example usage

```
import molnet

emoln = molnet.Energimolnet('user', 'pass', 'company')

print emoln.customer()

print emoln.unit('00000000000000')

print emoln.data('00000000000000', metrics=['energy'], intervals=(1234, 4321), resolution='hour')

print emoln.nordpoolspot('00000000000000', [(1234, 4321)])

```

## Contributors

* [Marcus Ljungblad](mailto:marcus@ljungblad.nu)
