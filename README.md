# Niko Home Control

```python
niko = NikoHomeControl({
	'ip': '192.168.22.105',
	'port': 8000,
	'timeout': 20000,
	'events': True
})

print(niko.system_info())
print(niko.list_locations())
print(niko.list_energy())
print(niko.list_actions())
```
