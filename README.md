# Niko Home Control

## Usage

```python
niko = NikoHomeControl({
	'ip': '192.168.22.105',
	'port': 8000,
	'timeout': 20000,
	'events': True
})
```

## Examples

Get system information:

`print(niko.system_info())`


List defined locations:

`print(niko.list_locations())`


List energy information:

`print(niko.list_energy())`


List all defined actions:

`print(niko.list_actions())`


Get the information about a single item:

`print(niko.item_state(<id>))` where `<id>` is the id of the item you want to
retrieve information for.
