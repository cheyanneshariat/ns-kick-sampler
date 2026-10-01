# NS kick sampler

A minimal NumPy function for sampling scalar neutron-star natal-kick speeds from the global, all-NS-birth distribution inferred in *A concordance model of neutron star kicks* by Cheyanne Shariat, Kareem El-Badry, and Smadar Naoz.

## Use

```bash
git clone https://github.com/cheyanneshariat/ns-kick-sampler.git
cd ns-kick-sampler
python -m pip install numpy
```

```python
from ns_kick_sampler import sample_kick_speeds

speeds_kms = sample_kick_speeds(10_000, seed=7)
```

`seed` is passed to `numpy.random.default_rng`. The function returns a one-dimensional NumPy array; `n=0` returns an empty array.

## Conventions and provenance

The model first chooses a component with global all-NS-birth low-kick fraction

```text
f_low = 0.126
```

and then samples a scalar speed from

```text
low:  ln(v / (km/s)) ~ Normal(1.87, 0.55)
high: ln(v / (km/s)) ~ Normal(5.62, 0.71)
```

Each component is separately normalized and truncated to `0.05 < v / (km/s) < 1000`; rejection occurs within the already chosen component, so truncation does not change `f_low`. These are natural-log parameters for scalar speeds, not Cartesian-component dispersions or Maxwellian parameters. The model has no mass dependence.

The defaults are the marginal posterior central values reported in Table `tab:joint_fit_params` of the manuscript. In particular, `(5.62, 0.71)` are the fitted high-component summaries; `(5.60, 0.68)` are the young-pulsar prior centers. Combining fixed marginal summaries gives a convenient approximation, not a posterior-marginalized distribution or a representative joint-posterior draw. Full uncertainty propagation requires correlated joint-posterior draws, which are outside this small repository.

No kick direction is sampled. A vector implementation would additionally need to assume a direction distribution, commonly isotropic.

## License

MIT
