## AI Model Footprint & Sustainability

CapMoo performs only API-based inference—there is no local training.

### Inference Energy & Emissions

- **Energy per Caption:**  
  Independent estimates place LLM inference at **0.0017–0.0026 kWh** per request; we use an average of **0.002 kWh** :contentReference[oaicite:0]{index=0}.  
- **Thailand Grid Emission Factor:**  
  The national electricity mix emits **0.442 kg CO₂e/kWh** :contentReference[oaicite:1]{index=1}.  
- **CO₂ per Caption:**  
  0.002 kWh × 0.442 kg CO₂e/kWh = **0.000884 kg CO₂e** per generated caption.  

### Efficiency Measures

- **Edge Filtering:**  
  NVIDIA Jetson Nano filters out ~40% of empty or blurred frames before API calls.  
- **Batching Requests:**  
  We batch captions in groups of 20, reducing per-caption overhead by ~20%.  

### Quarterly & Annual Emissions

- **Monthly Volume:** 10,000 captions  
- **Monthly Emissions:** 10,000 × 0.000884 kg CO₂e ≈ **8.84 kg CO₂e**  
- **Annual Emissions:** ≈ **106 kg CO₂e**

### Offsetting & Future Roadmap

- **Carbon Offsets:** We purchase Renewable Energy Certificates (RECs) equal to **150 kg CO₂e/year**.  
- **Hardware Optimization:** Roadmap to deploy on-device inference via Jetson Xavier NX to eliminate cloud calls—projected to cut emissions by ~90%.