## Date Structure Example

### Starting Point

```json
{
  "reference": "NX-CORTEX-7",
  "family": "NEURAL",
  "label": "Interface corticale NX-7",
  "manufacturer": "NeuroLink Corp",
  "specs": {
    "bandwidth_mbps": 480,
    "power_draw_w": 2.4,
    "expected_lifespan_months": 96
  },
  "compatibility": {
    "min_age": 18,
    "incompatible_with": ["NX-CORTEX-5", "SYN-RELAY-2"]
  },
  "monitored_parameters": [
    { "code": "NEURAL_IMPEDANCE", "unit": "kOhm", "nominal_min": 8.0, "nominal_max": 14.0 },
    { "code": "SYNAPTIC_LATENCY", "unit": "ms", "nominal_min": 0.4, "nominal_max": 2.1 }
  ]
}
```

