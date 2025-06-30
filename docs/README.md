# Open WebUI with LLM services
- Table of Content
  - [Environments](#environments)
    - [Local](#local)
    - [GCP](#gcp)  
  - [Quick Start](#quick-start)
    - [GPU Support](#gpu-support)
    - [CPU](#cpu)
    - [User, Role, Goup and Premissions](#user-role-goup-and-premissions)
    - [API Endpoints](#api-endpoints)
  - [LLMs in Ollama](#llms-in-ollama)
  - [vLLM’s Official Docker Image](#vllms-official-docker-image)
  - [Model Experiments](#model-experiments)
    - [OCR](#ocr)
    - [Speech To Text](#speech-to-text)
  - [Tools](#tools)
    - [ffmpeg](#ffmpeg)
    - [docker](#docker)
  - [References](#references)

## Environments
On-premise and access via VPN

<img width="600" alt="image" src="https://github.com/user-attachments/assets/7706002c-aab6-45cc-9e72-2cb17a6dfb59" />

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

### Mix - GCP with Local
![image](https://github.com/user-attachments/assets/5487aafa-3b57-4f2f-96b8-c9009fd177b5)

## Quick Start
### GPU Support
* [Start Open WebUI with docker](https://docs.openwebui.com/getting-started/quick-start/#using-gpu-support)  
  `docker run -d -p 3000:8080 --gpus all -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:0.6.13-cuda` 

* [Start Ollama with docker](https://hub.docker.com/r/ollama/ollama)
  * [Install NVIDIA Container Toolkit](https://hub.docker.com/r/ollama/ollama)⁠

  * Run Ollama docker  
    `docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama:0.6.8`

### CPU
* Start Open WebUI with docker  
  `docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:0.6.5`
  
* Start Ollama with docker  
  `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

### User, Role, Goup and Premissions
#### Create a User  
Sign in as an Admin > `Admin Panel` > `Users` > `Add User` > change `ROLE` to `USER` 

#### Create a Group and Grant models premission 
- Sign in as an Admin > `Admin Panel` > `Users` > `Groups` > `+ Create Group` > fill group `Name` and click `Create`
  -  `Groups` > `Edit User Group` > select/check the Users to add into the group and `Save`
- Sign in as an Admin > `Admin Panel` > `Settings` > `Models` > select a model
  - Visibility = Private
  - Groups = select the Group that just created

### [API Endpoints](https://docs.openwebui.com/getting-started/api-endpoints)
#### [Using an Individual File in Chat Completions](https://docs.openwebui.com/getting-started/api-endpoints#using-an-individual-file-in-chat-completions)
```
POST http://${HOST}/api/chat/completions
Authorization: Bearer ${KEY}
Content-Type: application/json

{
  "model": "o4-mini",
  "messages": [
    {
      "role": "developer",
      "content": "你是一位創意的影片腳本設計師，請依下列需求，擴寫使用者輸入的腳本: 1.描述依序為：事件描述，地點描述，時間和氣氛，攝影角度與鏡頭類型，腳本不用分段. 2.使用知識庫，置換對應的名詞，不用附加參照連結. 3.分別用中文和英文輸出. 4.不翻譯知識庫置換的名詞."
    },
    {
      "role": "user",
      "content": "一隻台灣黑熊在路思義前跳舞"
    }
  ],
  "files": [
    {
      "type": "file",
      "id": "9a01de4e-bd67-43ea-b92f-da7598b6a13f"
    }
  ]
}
```

#### [Using a Knowledge Collection in Chat Completions](https://docs.openwebui.com/getting-started/api-endpoints#using-a-knowledge-collection-in-chat-completions)
```
{
  "model": "o4-mini",
  "messages": [
    {
      "role": "developer",
      "content": "你是一位創意的影片腳本設計師，請依下列需求，擴寫使用者輸入的腳本: 1.全中文描述. 2.描述依序為：事件描述，地點描述，時間和氣氛，攝影角度與鏡頭類型，腳本不用分段. 3.使用知識庫，置換對應的名詞，不用附加參照連結."
    },
    {
      "role": "user",
      "content": "一隻台灣黑熊在路思義前跳舞"
    }
  ],
  "files": [
    {
      "type": "collection",
      "id": "b358e2d8-7a46-44e3-ad2e-6c7e3e832b4b"
    }
  ]
}
```

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

## Model Experiments
### OCR
#### [reducto/RolmOCR](https://huggingface.co/reducto/RolmOCR) 
  - Better than Gemma3 in terms of Accuracy and Speed, but more hardware resource required 

#### Gemma3 is avaiable to OCR from an image
  - The higher parameters the better recognizing result, i.e., 27b > 12b > 4.3b

### [OpenGVLab/InternVL3-14B](https://huggingface.co/OpenGVLab/InternVL3-14B)
TODO ...

### Speech To Text
#### [Whisper ASR Box](https://github.com/ahmetoner/whisper-asr-webservice)
We apply ahmetoner's https://github.com/ahmetoner/whisper-asr-webservice to deploy [OpenAI/Whisper](https://github.com/openai/whisper) model locally.  
- use [v1.7.1](https://github.com/ahmetoner/whisper-asr-webservice/releases/tag/v1.7.1) for local hardware env.
`docker run -d --gpus all --name whisper-asr-webservice -p 9000:9000 -e ASR_MODEL=medium -e ASR_ENGINE=openai_whisper onerahmet/openai-whisper-asr-webservice:v1.7.1-gpu`

#### [openai/whisper](https://github.com/openai/whisper)
- a local python package  
`whisper test_speech.mp3 --language Chinese --initial_prompt "繁體中文。" --model medium --device cuda`

### Tools
#### [ffmpeg](https://github.com/transitive-bullshit/ffmpeg-cli-flags)
- sampling 60 minutes from begining  
`ffmpeg -i ${filename.aac} -t 3600 -c copy ${filename_60mins.aac}`\

- convert format from AAC to MP#  
`ffmpeg -i ${filename.aac} ${filename.mp3}`

#### [Docker](https://docs.docker.com/reference/cli/docker/)
- [check running containers](https://docs.docker.com/reference/cli/docker/container/ls/)  
`docker ps`

- [check container's log](https://docs.docker.com/reference/cli/docker/container/logs/) (sudo privilege required)  
`docker logs -f open-webui` (Ctrl + C to exit)

- [enter into container's shell](https://docs.docker.com/reference/cli/docker/container/exec/)  
`docker exec -it open-webui /bin/bash`

#### VPN
- Enable VPM Client network Adapter
`vpnclient start`

- [Temporary IP address assignment](https://documentation.ubuntu.com/server/explanation/networking/configuring-networks/#temporary-ip-address-assignment)  
`ip addr add 10.102.66.200/24 dev enp0s25`

- Connect to VPN Server (Virtual Hub)
```
vpncmd # select 2 and Enter
VPN Client>accountlist
VPN Client>AccountConnect ${VPN Connection Setting Name}
VPN Client>accountstatusget ${VPN Connection Setting Name}
```


## References
* https://hub.docker.com/r/ollama/ollama
* https://docs.openwebui.com/
* https://github.com/openai/whisper
* https://github.com/SYSTRAN/faster-whisper
* https://github.com/ahmetoner/whisper-asr-webservice
* [Softether Ad-hoc VPN](https://www.softether.org/4-docs/2-howto/1.VPN_for_On-premise/1.Ad-hoc_VPN) 
* [ComfyUI Tutorial Series: Ep10 - Flux GGUF and Custom Nodes](https://www.youtube.com/watch?v=Ym0oJpRbj4U)


## Legacy 
### Cost estimation of GCP Compute Engine - [GPU Machine type](https://cloud.google.com/compute/docs/gpus) and OS
#### G2 + L4 GPUs
- asia-east1 (Taiwan)
  - 1 x NVIDIA L4
  - g2-standard-4 (4 vCPUs, 16 GB Memory)
- Balanced persistent disk
  - Size 100 GB
  - Deep Learning On Linux - Deep Learning VM with CUDA 12.3 M129
- Cost (2025.Apr)
  - $607.46 USD Monthly
  - $0.83 USD hourly

#### N1 + T4 GPUs (issues during run newly models)
- asia-east1 (Taiwan)
  - 1 x NVIDIA T4
  - n1-highmem-2 (2 vCPUs, 13 GB Memory)
- Balanced persistent disk
  - Size 100 GB
  - Deep Learning On Linux - Deep Learning VM with CUDA 12.3 M129
- Cost (2025.Apr)
  - $258.85 USD Monthly
  - $0.35 USD hourly

![image](https://github.com/user-attachments/assets/baa2d2a9-3429-47d2-92ca-8467957cec01)

![image](https://github.com/user-attachments/assets/42ee96ee-1325-4f78-814a-363117f57360)



