# open-webui

## Environments
<img width="480" alt="image" src="https://github.com/user-attachments/assets/b92a5833-6d47-4ba2-b217-fb3848ee4dbf" />

### Local

RTX-3070

RTX-4090

### GCP

### Mix 
TODO ...

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
