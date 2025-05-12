![image](https://github.com/user-attachments/assets/1ee1279f-2147-4bf0-baad-731127488b3b)![image](https://github.com/user-attachments/assets/6ab19fb4-e130-435b-ae4b-4d10f412fcf6)# open-webui

## Environments
On-premise and access via VPN

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
#### [Compute Engine - Machine type](https://cloud.google.com/compute/docs/gpus) and OS
##### Standard
- asia-east1 (Taiwan)
- G2 + L4 GPUs
  - 1 x NVIDIA L4
  - g2-standard-4 (4 vCPUs, 16 GB Memory)
- Balanced persistent disk
  - Size 100 GB
  - Deep Learning On Linux - Deep Learning VM with CUDA 12.3 M129
- Cost (2025.Apr)
  - $607.46 USD Monthly
  - $0.83 USD hourly

##### Legacy (issues during run newly models)
- asia-east1 (Taiwan)
- N1 + T4 GPUs
  - 1 x NVIDIA T4
  - n1-highmem-2 (2 vCPUs, 13 GB Memory)
- Balanced persistent disk
  - Size 100 GB
  - Deep Learning On Linux - Deep Learning VM with CUDA 12.3 M129
- Cost (2025.Apr)
  - $258.85 USD Monthly
  - $0.35 USD hourly

#### Cloud Run
TODO ... cost reduction

### Mix 
TODO ...

<img width="322" alt="image" src="https://github.com/user-attachments/assets/059069d5-aaf9-49fd-88a8-ef665470a3c2" />

## Quick Start
### GPU Support
* [Start Open WebUI with docker](https://docs.openwebui.com/getting-started/quick-start/#using-gpu-support)  
  `docker run -d -p 3000:8080 --gpus all -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:cuda` 

* [Start Ollama with docker](https://hub.docker.com/r/ollama/ollama)
  * [Install NVIDIA Container Toolkit](https://hub.docker.com/r/ollama/ollama)⁠

  * Run Ollama docker  
    `docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:0.6.8`

### CPU
* Start Open WebUI with docker  
  `docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main`
  
* Start Ollama with docker  
  `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

### User, Role, Goup and Premissions
TODO...


## LLMs in Ollama
* List models  
`docker exec ollama ollama list`

* Show a model information  
`docker exec ollama ollama show llama3`

* Run a model  
`docker exec ollama ollama run llama3`

* Check usage
`docker exec ollama ollama`

## [vLLM’s Official Docker Image](https://docs.vllm.ai/en/stable/deployment/docker.html)
### [reducto/RolmOCR](https://huggingface.co/reducto/RolmOCR)  
  Note. +30G GPU Memory is required during loading and running the RolmOCR model 
```
docker run -d --name vllm --gpus all -v ~/.cache/huggingface:/root/.cache/huggingface --env "HUGGING_FACE_HUB_TOKEN=<secret>" -p 8000:8000 --ipc=host vllm/vllm-openai:latest --model reducto/RolmOCR
```

### [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B)  
```
docker run -d --name vllm --gpus all -v ~/.cache/huggingface:/root/.cache/huggingface --env "HUGGING_FACE_HUB_TOKEN=<secret>" -p 8000:8000 --ipc=host vllm/vllm-openai:latest --model Qwen/Qwen3-1.7B
```

## LMDeploy 
TODO...

## Model Experiments
### OCR
#### Gemma3 is avaiable to OCR from an image
  - The higher parameters the better recognizing result, i.e., 27b > 12b > 4.3b

#### [RolmOCR](#reductorolmocr) 

### Speech To Text
#### [Whisper ASR Box](https://github.com/ahmetoner/whisper-asr-webservice)
We apply ahmetoner's https://github.com/ahmetoner/whisper-asr-webservice to deploy [OpenAI/Whisper](https://github.com/openai/whisper) model locally.  

## References
* https://hub.docker.com/r/ollama/ollama
* https://docs.openwebui.com/
* 

