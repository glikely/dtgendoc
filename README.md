# dtgendoc

A quick and dirty proof-of-concept script that generates markdown
text markup from YAML DT Binding documentation source files. This
generates something roughly web presentable from the DT bindings
docs.

dtgendoc makes no attempt to resolve reference fields into proper
URLs. This is left as an exercise for a production doc generator
that resolves id tags in YAML DT bindings and builds proper URL
references to those bindings.

## usage

```
dtgendoc.py abinding.yaml > abinding.md
```

## viewing

Try [grip](https://github.com/joeyespo/grip.git) to view the result
locally.

## license

GPLv2. See the *LICENSE* file.
