# SRE Agent LLM Judge

This project provides an automated evaluation framework for AI-generated operational insights using a Large Language Model (LLM) as a critical judge. It is designed to assess the quality of system operation insights, specifically for the hashlify platform, by leveraging a custom LLM endpoint and a set of rigorous, domain-specific evaluation criteria.

## Overview

The core of this project is the `main.py` script, which:
- Connects to a custom LLM API endpoint (e.g., Llama3-70b) via a secure HTTP interface.
- Evaluates AI-generated JSON insights related to system operations, focusing on two main fields: `investigation_summary` and `remediation_steps`.
- Uses detailed, context-rich prompts to guide the LLM in classifying and justifying the quality of these insights.
- Returns structured, machine-readable feedback for further automation or human review.

## Approach: GEval (LLM as a Judge with Chain of Thought)

This project implements the **GEval** approach:
- **LLM as a Judge**: The LLM is positioned as a critical, professional evaluator, not just a generator. It is given explicit, detailed instructions and domain rules to judge the quality of operational insights.
- **Chain of Thought (CoT)**: The prompts are designed to encourage the LLM to reason step-by-step, referencing evidence, following evaluation criteria, and providing clear justifications for its classifications. This improves reliability and transparency in the evaluation process.

The combination of these techniques ensures that the LLM's judgments are both rigorous and explainable, making the system suitable for high-stakes operational environments.

## Features
- **Custom LLM Endpoint Integration**: Easily connect to any LLM API that follows the OpenAI-compatible chat completions format.
- **Domain-Specific Prompts**: Prompts are tailored for hashlify's operational context, with strict rules for what constitutes a good or bad insight.
- **Structured Output**: Uses LangChain's `StructuredOutputParser` to enforce JSON output with `classification` and `justification` fields.
- **Extensible Evaluation Types**: Supports both remediation steps and investigation summary evaluations.
- **Environment Variable Configuration**: API URLs and access keys are managed via environment variables for security and flexibility.

## How It Works
1. **Initialization**: The script loads environment variables for the LLM API endpoint and access key.
2. **Prompt Construction**: Depending on the evaluation type, it builds a detailed prompt with instructions and criteria.
3. **LLM Call**: The prompt and the AI-generated insight are sent to the LLM endpoint.
4. **Parsing**: The LLM's response is parsed into structured JSON, extracting the classification and justification.
5. **Output**: The result is printed or can be integrated into further automation.

## Example Usage

Run the script with:
```bash
python main.py
```

The script contains a sample `insight` JSON and will print the parsed evaluation result.

## Setup
1. **Install Dependencies**
   - Install Python 3.8+ and pip.
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```
2. **Set Environment Variables**
   - `AGENT_URL`: Base URL of your LLM API endpoint (e.g., `https://your-llm-api.com`).
   - `ACCESS_KEY`: Your API access key/token.
   - Example:
     ```bash
     export AGENT_URL="https://your-llm-api.com"
     export ACCESS_KEY="your_api_key_here"
     ```
3. **Run the Script**
   - Execute:
     ```bash
     python main.py
     ```

## File Structure
- `main.py`: Main script containing the LLM evaluation logic, prompt templates, and entry point.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## Customization
- **Prompts**: You can modify the evaluation criteria and instructions in `main.py` to fit other operational domains.
- **LLM Endpoint**: Swap in any OpenAI-compatible LLM endpoint by changing the environment variables.

## Why GEval?
- **Reliability**: By using an LLM as a judge with explicit, stepwise reasoning, the system produces more consistent and trustworthy evaluations.
- **Transparency**: The Chain of Thought approach ensures that every classification is accompanied by a clear, evidence-based justification.
- **Automation-Ready**: Structured outputs make it easy to integrate with CI/CD pipelines, dashboards, or alerting systems.

## References
- [G-EVAL: NLG Evaluation using GPT-4 with Better Human Alignment](https://arxiv.org/pdf/2303.16634)  
  (This paper introduces the GEval approach: using LLMs with Chain-of-Thought for better human-aligned evaluation)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)

## License
This project is provided under the MIT License. 