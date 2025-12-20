# Configuration Guide

This guide explains how to configure the Strands Agents SDK with Open Web UI, including all required and optional environment variables.

## Quick Start

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials**:
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Verify your configuration**:
   ```bash
   python -m pytest tests/ -v
   ```

## Required Configuration

### AWS Bedrock

AWS Bedrock is required for all agents to function. You have two options:

#### Option 1: Bedrock API Key (Recommended for Development)

This is the simplest option for getting started:

1. **Get your API key**:
   - Open [AWS Bedrock Console](https://console.aws.amazon.com/bedrock)
   - Navigate to "API keys" in the left sidebar
   - Click "Generate long-term API key"
   - Copy the key (it's shown only once!)

2. **Set the environment variable**:
   ```bash
   export AWS_BEDROCK_API_KEY=your_bedrock_api_key_here
   ```
   
   Or add to your `.env` file:
   ```
   AWS_BEDROCK_API_KEY=your_bedrock_api_key_here
   ```

3. **Enable model access**:
   - In Bedrock Console, go to "Model access"
   - Click "Manage model access"
   - Enable "Amazon Nova Pro" (or your preferred model)
   - Wait a few minutes for access to be granted

**Note**: Bedrock API keys expire after 30 days. For production, use Option 2.

#### Option 2: AWS Credentials (Recommended for Production)

For production environments, use standard AWS credentials:

1. **Configure AWS credentials**:
   ```bash
   aws configure
   ```
   
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-west-2
   ```
   
   Or add to your `.env` file:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=us-west-2
   ```

2. **Ensure IAM permissions**:
   Your AWS user/role needs the following permissions:
   - `bedrock:InvokeModel`
   - `bedrock:InvokeModelWithResponseStream`

3. **Enable model access** (same as Option 1, step 3)

## Optional Configuration

### Tavily API (For Web Search Agent)

The Tavily Search Agent requires a Tavily API key for real-time web search capabilities.

1. **Get your API key**:
   - Visit [https://tavily.com/](https://tavily.com/)
   - Sign up for a free account
   - Navigate to your dashboard
   - Copy your API key

2. **Set the environment variable**:
   ```bash
   export TAVILY_API_KEY=your_tavily_api_key
   ```
   
   Or add to your `.env` file:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   ```

**Note**: Without this key, the Tavily Search Agent will not be available, but all other agents will work normally.

### Other Optional Services

These services are not currently used but may be needed for future agents:

#### OpenAI API
```bash
export OPENAI_API_KEY=your_openai_api_key
```
Get from: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

#### Anthropic API
```bash
export ANTHROPIC_API_KEY=your_anthropic_api_key
```
Get from: [https://console.anthropic.com/](https://console.anthropic.com/)

#### Stability AI API
```bash
export STABILITY_API_KEY=your_stability_api_key
```
Get from: [https://platform.stability.ai/](https://platform.stability.ai/)

#### Slack Bot Token
```bash
export SLACK_BOT_TOKEN=your_slack_bot_token
```
Get from: [https://api.slack.com/apps](https://api.slack.com/apps)

## Environment File Structure

Your `.env` file should look like this:

```bash
# AWS Credentials for Bedrock (Required - choose one option)

# Option 1: Bedrock API Key (for development)
AWS_BEDROCK_API_KEY=your_bedrock_api_key_here

# Option 2: AWS Credentials (for production)
# AWS_ACCESS_KEY_ID=your_aws_access_key_here
# AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
# AWS_DEFAULT_REGION=us-west-2

# API Keys for external services

# Tavily API (Optional - for web search)
TAVILY_API_KEY=your_tavily_api_key

# OpenAI API Key (Optional - for future use)
# OPENAI_API_KEY=your_openai_api_key

# Anthropic API Key (Optional - for future use)
# ANTHROPIC_API_KEY=your_anthropic_api_key

# Stability AI API Key (Optional - for future use)
# STABILITY_API_KEY=your_stability_api_key

# Slack Bot Token (Optional - for future use)
# SLACK_BOT_TOKEN=your_slack_bot_token

# PostgreSQL Configuration (for Open Web UI)
POSTGRES_DB=openwebui
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Open Web UI Configuration
WEBUI_SECRET_KEY=change-me-in-production-to-a-random-string

# Logging
LOG_LEVEL=INFO
```

## Verification

After configuring your environment variables, verify your setup:

```bash
python -m pytest tests/ -v
```

This script will:
- ✅ Check if required credentials are set
- ⚠️  Warn about missing optional credentials
- 🤖 List available agents based on your configuration
- 📝 Provide next steps

### Expected Output (Fully Configured)

```
🚀 Strands Agents Configuration Checker
========================================

🔧 AWS Bedrock Configuration (Required)
========================================
  ✅ AWS_BEDROCK_API_KEY is set

🔧 Tavily API Configuration (Optional)
=======================================
  ✅ TAVILY_API_KEY is set

📊 Configuration Summary
=========================
✅ AWS Bedrock: Ready
✅ Tavily Search: Ready

🤖 Agent Availability
====================
✅ 7 agents available:
   • alfred-butler (Default conversational agent)
   • calculator (Mathematical computations)
   • python-repl (Python code execution)
   • http-request (Web API interactions)
   • file-read (File reading and analysis)
   • file-write (File creation and writing)
   • tavily-search (Real-time web search)

📝 Next Steps
============
1. ✅ AWS configuration is ready
2. ✅ All configurations are ready
3. 🚀 Start the server: python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### "AWS credentials not found"

**Problem**: The application can't find your AWS credentials.

**Solutions**:
1. Check that your `.env` file exists and contains the credentials
2. Verify the credentials are not commented out (no `#` at the start)
3. Ensure there are no extra spaces around the `=` sign
4. Try setting the environment variable directly in your shell
5. Restart your terminal/IDE after setting environment variables

### "TAVILY_API_KEY appears to be the example placeholder"

**Problem**: You haven't replaced the example API key with your actual key.

**Solution**:
1. Get your API key from [https://tavily.com/](https://tavily.com/)
2. Replace the placeholder in `.env` with your actual key
3. The key should start with `tvly-` followed by your unique identifier

### "Access denied to model"

**Problem**: Your AWS account doesn't have access to the Bedrock model.

**Solutions**:
1. Open [AWS Bedrock Console](https://console.aws.amazon.com/bedrock)
2. Navigate to "Model access" in the left sidebar
3. Click "Manage model access"
4. Enable the model you want to use (e.g., Amazon Nova Pro)
5. Wait a few minutes for access to be granted
6. Try again

### "Invalid API key" or "Authentication failed"

**Problem**: Your API key is incorrect or expired.

**Solutions**:
1. Verify the API key is correct (no typos)
2. Check if the key has expired (Bedrock API keys last 30 days)
3. Generate a new key if needed
4. Ensure there are no extra spaces or newlines in the key

### Environment variables not loading

**Problem**: The application isn't reading your `.env` file.

**Solutions**:
1. Ensure the `.env` file is in the correct directory (repo2/)
2. Check file permissions: `chmod 600 .env`
3. Verify the file is named exactly `.env` (not `.env.txt`)
4. Try loading the environment manually:
   ```bash
   export $(cat .env | xargs)
   ```

## Security Best Practices

1. **Never commit `.env` files**:
   - The `.env` file is in `.gitignore` by default
   - Always use `.env.example` for templates

2. **Use different credentials for different environments**:
   - Development: Bedrock API keys (short-lived)
   - Production: IAM roles or temporary credentials

3. **Rotate credentials regularly**:
   - Bedrock API keys expire after 30 days
   - Rotate other API keys periodically

4. **Use least-privilege access**:
   - Only grant necessary permissions
   - Use separate IAM users/roles for different purposes

5. **Protect your `.env` file**:
   ```bash
   chmod 600 .env  # Only owner can read/write
   ```

## Docker Configuration

When using Docker, pass environment variables using:

1. **Docker Compose** (recommended):
   ```yaml
   services:
     api:
       env_file:
         - .env
   ```

2. **Docker run**:
   ```bash
   docker run --env-file .env your-image
   ```

3. **Individual variables**:
   ```bash
   docker run -e AWS_BEDROCK_API_KEY=your_key your-image
   ```

## Production Considerations

For production deployments:

1. **Use AWS IAM roles** instead of API keys
2. **Use AWS Secrets Manager** or similar for credential management
3. **Enable CloudWatch logging** for monitoring
4. **Set up proper IAM policies** with least-privilege access
5. **Use VPC endpoints** for Bedrock access
6. **Implement rate limiting** and cost controls
7. **Monitor API usage** and costs

## Getting Help

If you're still having issues:

1. Run the test suite: `python -m pytest tests/ -v`
2. Check the logs: `LOG_LEVEL=DEBUG python -m uvicorn src.api:app`
3. Review the [README.md](README.md) for additional information
4. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
5. Open an issue on GitHub with your configuration output (redact sensitive information!)

---

**Remember**: Never share your actual API keys or credentials publicly!