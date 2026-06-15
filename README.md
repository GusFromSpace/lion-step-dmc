# lion-step-dmc

A [demoniC](https://github.com/GusFromSpace/demoniC) port of
[**Lion optimizer (EvoLved Sign Momentum)**](https://arxiv.org/abs/2302.06675 (Chen et al., 2023)).

## Files

- `lion_step.dmc` — the demoniC port
- `lion_step.py` — Python reference (the same algorithm, for verification)

## Verification

The port is checked out-of-band so the `.dmc` stays a pure translation. `verify/run.sh`
runs `lion_step.py` and the `.dmc` on the same fixed inputs and confirms every
emitted number agrees (rtol 1e-5):

```
DMC=/path/to/dmc verify/run.sh
```

## License & attribution

**Unlicensed.** This is a clean-room reimplementation of a *published algorithm*, not a copy of any source code, so no upstream code license applies. For the original work, defer to the original author. ¯\_(ツ)_/¯  See [NOTICE](NOTICE).

Credit for the original goes to the original authors. See [NOTICE](NOTICE).
