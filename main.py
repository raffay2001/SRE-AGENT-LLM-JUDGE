from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from typing import Any, Dict, List, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
import requests
import os
from typing import Any, Dict, List, Optional

# Endpoint LLM class initialization
class LLMCustomEndpoint(LLM):
    """Custom LLM that interacts with your API endpoint."""
    
    api_url: str = "YOUR_API_ENDPOINT_URL"
    access_key: str = "YOUR_ACCESS_KEY"
    temperature: float = 0.0
    
    @property
    def _llm_type(self) -> str:
        return "endpoint-llm"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_name": "Llama3-70b-API",
            "temperature": self.temperature
        }
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the API endpoint with the given prompt."""
        try:
            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "include_functions_info": False,
                "include_retrieval_info": False,
                "include_guardrails_info": False,
                "temperature": self.temperature
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_key}"
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(e)
            raise ValueError(f"Error calling API endpoint: {str(e)}")

AGENT_URL = os.getenv("AGENT_URL")
ACCESS_KEY = os.getenv("ACCESS_KEY")
API_URL = f"{AGENT_URL}/api/v1/chat/completions"

if ACCESS_KEY is None:
    raise ValueError("ACCESS_KEY environment variable is not set.")

llm = LLMCustomEndpoint(
    api_url=API_URL,
    access_key=ACCESS_KEY,
    temperature=0.0
)

# Insights Classifications Validation Sets 
VALID_CLASSES = {"Excellent", "Good", "Needs Improvement", "Bad"}
# Insights Alert Types Validation Sets
VALID_ALERT_TYPES = {"CBWebstackHealth", "CBDiskHealth", "HostHealth"}

# Defining Response Schemas and Format Instructions
classification_schema = ResponseSchema(name="classification",
                             description="Insights evaluated class must be One of: Good | Needs Improvement | Bad")
justification_schema = ResponseSchema(name="justification",
                                      description="Justification for the classification based on the input insight and evaluation criterias from prompts.")
response_schemas = [classification_schema, justification_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# Load prompt templates from markdown files
with open("prompts/SystemPrompt.md", "r") as f:
    SystemPrompt = f.read().split('```text', 1)[-1].rsplit('```', 1)[0].strip()
with open("prompts/RemediationStepsEvalPrompt.md", "r") as f:
    RemediationStepsEvalPrompt = f.read().split('```text', 1)[-1].rsplit('```', 1)[0].strip()
with open("prompts/InvestigationSummaryEvalPrompt.md", "r") as f:
    InvestigationSummaryEvalPrompt = f.read().split('```text', 1)[-1].rsplit('```', 1)[0].strip()
with open("prompts/RemediationStepsGEvalPrompt.md", "r") as f:
    RemediationStepsGEvalPrompt = f.read().split('```text', 1)[-1].rsplit('```', 1)[0].strip()

# Function that calls Llama3.1:8b locally performing insights evaluation.
def  send_to_llm(insight, prompt_type="remediation_steps") -> Dict[str, Any]:
    """Calls Llama3 70b via API for performing insights evaluation."""
    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SystemPrompt,
                ),
                ("human", RemediationStepsGEvalPrompt if prompt_type == "remediation_steps" else InvestigationSummaryEvalPrompt),
            ]
        )        
        chain = prompt | llm
        output = chain.invoke({
           "insight":insight,
           "format_instructions": format_instructions
        })
        parsed_llm_response = output_parser.parse(output)
        return parsed_llm_response
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return {}

# main entry point function
def main():
    insight = """{
    "investigation_summary": "Investigation of /var/log/syslog and journalctl shows continuous restart loops where \u201c/bin/systemctl restart redis-server.service\u201d times out after 30 s, and systemctl reports redis-server.service as \u201cdeactivating (stop-sigterm)\u201d with Main PID 772967 \u201ccode=killed, signal=KILL\u201d.  The primary Redis log at /var/log/redis/redis-server.log is empty and the unit has been stalled since 2025-05-28, indicating the service never reaches a point where it can write logs.  Evidence points to Redis being force-killed\u2014likely by the kernel\u2019s out-of-memory handler\u2014so the cache layer remains offline until memory limits or configuration are adjusted.",
    "remediation_steps": "To remediate the issue with the Redis service failing to start on your hashlify host, follow these actionable steps:\n\n1. **Check Resource Availability**:\n   - Ensure that your server has sufficient memory and CPU resources available. You may need to upscale your server resources if it\u2019s under heavy load. This can be done by navigating to Server Management > Vertical Scaling in your hashlify dashboard.\n\n2. **Contact Support**:\n   - Given that the Redis service is in a deactivating state and logs are not providing necessary insights, it is crucial to contact hashlify Support for further investigation. Provide them with the following details:\n     - Redis failure to start as indicated by logs, specifically:\n       ```\n       'redis' failed to start (exit status -1) -- Program '/bin/systemctl restart redis-server.service' timed out after 30 s\n       ```\n     - The status output from the command:\n       ```\n       systemctl status redis-server.service\n       ```\n     - Mention that the Redis log file (`/var/log/redis/redis-server.log`) is empty, and there have been no significant entries since May 28, 2025.\n\n3. **Configuration Review** (if applicable):\n   - Although you do not have access to modify core service config files directly, you should ensure that any application using Redis is optimized to work within the set limits. If your application is heavily utilizing Redis, check the configuration settings to ensure they align with your app\u2019s demands, especially the `maxmemory` setting specified in the config file (`/etc/redis/redis.conf`). Notify support if adjustments to this setting are needed.\n\nBy following these steps, you can effectively address the issue with the Redis service on your hashlify host.",
    "links": [
        "https://support.hashlify.com/en/articles/5120718-what-can-i-do-in-the-manage-services-section",
        "https://support.hashlify.com/en/articles/5120681-server-monitoring-alerts"
    ],
    "fixes": [
        {
            "reasoning": "No automated, in-panel fix actions are applicable here.\n\nThe investigation concludes that the core problem is the system-level Redis service being killed (likely by the kernel\u2019s out-of-memory handler). All recommended next steps involve:\n\n\u2022 Checking/expanding server memory or CPU resources  \n\u2022 Reviewing/adjusting Redis configuration (e.g., maxmemory)  \n\u2022 Contacting hashlify Support\n\nNone of the remediation steps map to the available automation tools (which handle PHP-FPM, MySQL, Varnish, Elasticsearch, file deletion, IP blocks, or bot blocks). Consequently, no tool execution is required or appropriate."
        }
    ]
}
"""
    
    ai_response = send_to_llm(insight, prompt_type="remediation_steps")
    print(f"\nThe Parsed Response Is:\n{ai_response}")
            
if __name__ == "__main__":
    main()
