## Initialize and commit
```bash
echo "# deepseek-ocr" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/fatih-keles/deepseek-ocr.git
git push -u origin main
```

## Commit changes
```bash
git remote add origin https://github.com/fatih-keles/deepseek-ocr.git
git add .
git commit -m "added client code, requirements, gitignore"
git push -u origin main
```

# OCI Server Setup for DeepSeek OCR with Ollama

## Step 1: Update Ubuntu & Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl -y
```

## Step 2: Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Step 3: Performance Tuning for OCI A1 (Important)

### Open the Ollama service configuration
```bash
sudo systemctl edit ollama.service
```

```ini
[Service]
# Use all 16 cores for faster image processing
Environment="OLLAMA_NUM_THREADS=16"
# Keep the model in RAM so subsequent OCR tasks are instant
Environment="OLLAMA_KEEP_ALIVE=-1"
```

### Reload and Restart
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

## Step 4: Install DeepSeek OCR Model
```bash
ollama pull deepseek-ocr
``` 
## Step 5: Verify Installation
```bash
ollama run deepseek-ocr "/path/to/image\nFree OCR."
ollama run deepseek-ocr "/path/to/image\nParse the figure."
ollama run deepseek-ocr "/path/to/image\nParse the figure."
ollama run deepseek-ocr "/path/to/image\n<|grounding|>Convert the document to markdown."
```

## Convert PDF to Image
```bash
sudo apt install poppler-utils
pdftoppm -jpeg -r 300 "Claim Experience.pdf" claim_page
```

## SCP 
```bash
scp -i ~/.ssh/your_key.pem your_file ubuntu@your_oci_instance_ip:/home/ubuntu/
``` 

## Run Ollama as a Service
```bash
sudo systemctl edit ollama.service
```

Add the following line to bind to all interfaces:
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
```

## Open Firewall Port
```bash
sudo iptables -L INPUT --line-numbers -n

# open port 11434 as rule number 5 and save state
sudo iptables -I INPUT 5 -m state --state NEW -p tcp --destination-port 11434 -j ACCEPT
sudo netfilter-persistent save

# delete firewall rule $line_number
sudo iptables -D INPUT $line_number

## create server process to listen port 5432
nc -l -p 5432

## find ports listening
sudo ss -tulpn | grep 11434
```

# Client Setup
## Create Python Environment
```bash
python3 -m venv ocr-env
source ocr-env/bin/activate
```

## Install Requirements
```bash
pip install --no-cache-dir -r requirements.txt
```

## Test Python Script
```bash
time python ocr_client.py ./data/claim_page-1.jpg
```
