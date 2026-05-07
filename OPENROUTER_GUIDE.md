# 🚀 Using Different LLMs with LangGraph Agent

Your LangGraph CopilotKit Agent now supports multiple LLM providers! Here's how to use them:

## 📋 Available Providers

| Provider | How to Enable | Example Models | Cost Efficiency |
|----------|---------------|----------------|-----------------|
| **OpenAI** (Default) | `LLM_PROVIDER=openai` | `gpt-4o-mini`, `gpt-4o`, `o1-preview` | 💰 Paid API |
| **OpenRouter** | `LLM_PROVIDER=openrouter` | `meta-llama/llama-3.1-8b-instruct`, `mistralai/mistral-7b`, `qwen/qwen-2.5-coder-32b` | 💵 Pay-per-call, often cheaper |
| **Anthropic** | `LLM_PROVIDER=anthropic` | `claude-3.5-sonnet-20241022`, `claude-3-opus-20240229` | 💰 Paid API |

## 🔧 Configuration

### 1. Set Your Provider (Backend)

In your `.env` file:

```bash
# Choose your provider
LLM_PROVIDER=openrouter  # or "openai" or "anthropic"

# Optional: specify a model
# MODEL_NAME=meta-llama/llama-3.1-70b-instruct

# Add your API key for the chosen provider
OPENAI_API_KEY=sk-xxx
# or
OPENROUTER_API_KEY=sk-xxx
# or
ANTHROPIC_API_KEY=sk-ant-xxx
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the Server

```bash
uvicorn app.main:app --reload --port 8000
```

## 🌟 Popular OpenRouter Models

Here are some excellent free/cheap models available via OpenRouter:

### Small & Fast (< 10B parameters)
- `meta-llama/llama-3.1-8b-instruct` ⭐ (Great balance)
- `mistralai/mistral-7b-instruct-v0.3`
- `qwen/qwen-2.5-7b-instruct`

### Medium (10-30B parameters)
- `meta-llama/llama-3.1-70b-instruct` ⭐ (Very capable)
- `mistralai/mixtral-8x7b-instruct-v0.1`
- `google/gemma-2-27b-it`

### Large (> 30B parameters)
- `meta-llama/llama-3.1-405b-instruct` (State-of-the-art)
- `anthropic/claude-3.5-sonnet`
- `google/gemini-1.5-pro`

## 💡 Examples

### Example 1: Use Llama 3.1 (OpenRouter)

```bash
# .env file
LLM_PROVIDER=openrouter
MODEL_NAME=meta-llama/llama-3.1-8b-instruct
OPENROUTER_API_KEY=your-openrouter-key
```

### Example 2: Use Claude 3.5 Sonnet (Anthropic)

```bash
# .env file
LLM_PROVIDER=anthropic
MODEL_NAME=claude-3.5-sonnet-20241022
ANTHROPIC_API_KEY=your-anthropic-key
```

### Example 3: Use GPT-4o (OpenAI)

```bash
# .env file
LLM_PROVIDER=openai
MODEL_NAME=gpt-4o
OPENAI_API_KEY=your-openai-key
```

## 🎯 How It Works

The agent uses LangGraph to orchestrate a 4-step workflow:

1. **Analyze** → Understand the request
2. **Plan** → Create a step-by-step plan
3. **Execute** → Generate the response
4. **Respond** → Deliver the final answer

All steps use the same LLM you've configured, maintaining consistency.

## 🔍 Testing Different Models

Try the same prompt with different models to compare:

```bash
# Terminal 1: OpenRouter with Llama
LLM_PROVIDER=openrouter MODEL_NAME=meta-llama/llama-3.1-8b-instruct uvicorn app.main:app --reload --port 8000

# Terminal 2: OpenAI with GPT-4o
LLM_PROVIDER=openai MODEL_NAME=gpt-4o uvicorn app.main:app --reload --port 8001

# Terminal 3: Anthropic with Claude
LLM_PROVIDER=anthropic MODEL_NAME=claude-3.5-sonnet-20241022 uvicorn app.main:app --reload --port 8002
```

## 📊 Cost Comparison

**OpenRouter** (approximate, as of 2024):
- Llama 3.1 8B: $0.20 / 1M tokens
- Llama 3.1 70B: $0.59 / 1M tokens

**OpenAI**:
- GPT-4o-mini: $0.15 / 1M tokens
- GPT-4o: $5.00 / 1M tokens

**Anthropic**:
- Claude 3.5 Sonnet: $3.00 / 1M tokens

## 🚨 Important Notes

1. **API Keys**: Each provider requires its own API key
2. **Context Windows**: Different models have different limits (e.g., 8k, 32k, 128k tokens)
3. **Rate Limits**: Free tier models may have usage limits
4. **Performance**: Larger models are slower but more capable

## 🎨 Frontend Configuration

The frontend automatically detects the backend provider. No changes needed!

```bash
# Start frontend (unchanged)
cd frontend
npm install
npm run dev
```

## 📞 Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **OpenRouter**: https://openrouter.ai/keys
- **Anthropic**: https://console.anthropic.com/

## 🎉 That's It!

Switch between providers by changing just one environment variable. Experiment to find the best model for your use case!

---

**Repository**: [github.com/vsc100/langgraph-copilotkit-agent](https://github.com/vsc100/langgraph-copilotkit-agent)
