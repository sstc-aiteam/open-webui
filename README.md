# open-webui

## Environments
<img width="360" alt="image" src="https://github.com/user-attachments/assets/b92a5833-6d47-4ba2-b217-fb3848ee4dbf" />

### Local
LLM models in RTX-3070 (.42)
| Models | Num. of Parameters |
| ------ | ------------- |
| deepseek-r1 | 7.6b |
| gemma3 | 4.3b |
| gemma3 | 12b |
| llama3 | 8b |
| phi4 | 14.7b |
| TwinkleAI/Llama-3.2-3B-F1-Resoning-Instruct | 3.6b |

LLM models RTX-4090 (.41)
| Models | Num. of Parameters |
| ------ | ------------- |
| deepseek-r1 | 14b |
| gemma3 | 27b |
| llama3.3 | 70b |
| qwen2.5 | 14b |


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

## LLMs in Ollama
* List models  
`docker exec ollama ollama list`

* Show a model information  
`docker exec ollama ollama show llama3`

* Run a model  
`docker exec ollama ollama run llama3`

* Check usage
`docker exec ollama ollama`

## Model Experiments
### OCR
- Gemma3 is avaiable to OCR from an image
  - The higher parameters the better recognizing result, i.e., 27b > 12b > 4.3b

### RolmOCR 
TODO ...

## References
* https://hub.docker.com/r/ollama/ollama
* https://docs.openwebui.com/
