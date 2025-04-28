# open-webui

## Environments
<img width="480" alt="image" src="https://github.com/user-attachments/assets/b92a5833-6d47-4ba2-b217-fb3848ee4dbf" />

### Local
LLM models in RTX-3070


LLM models RTX-4090

### GCP
#### N1+T4 GPUs
- n1-highmem-2 (2 vCPUs, 13 GB Memory)
- 1 x NVIDIA T4
- Deep Learning On Linux - Deep Learning VM with CUDA 12.3 M129

### Mix 
TODO ...

<img width="322" alt="image" src="https://github.com/user-attachments/assets/059069d5-aaf9-49fd-88a8-ef665470a3c2" />

## Quick Start
### GPU Support
* [Start Open WebUI with docker](https://docs.openwebui.com/getting-started/quick-start/#using-gpu-support)  
  `docker run -d -p 3000:8080 --gpus all -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:cuda` 
* [Start Ollama with docker](https://hub.docker.com/r/ollama/ollama)  
  `docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`
### CPU
* Start Open WebUI with docker  
  `docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main`
* Start Ollama with docker  
  `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

## References
* https://hub.docker.com/r/ollama/ollama
* https://docs.openwebui.com/
