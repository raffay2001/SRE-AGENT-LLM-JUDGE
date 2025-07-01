# Investigation Summary Evaluation Prompt

```text
You will be shown an AI-generated JSON insight object enclosed in the <insight></insight> tags containing two major fields: `insight` and `commands` along with some other metadata fields. 
The `insight` object will be having two fields:
    - investigation_summary (The summary of the investigation)
    - remediation_steps (The proposed steps user can apply to fix the issue)

Each `command` object contains three fields: 
    - command (The command the agent ran)
    - response (the response of the command)
    - created_at (timestamp on which the agent ran the command.)

- The commands array will be sorted by time i.e the sequence of the commands are preserved in the array.

Your task is to evaluate the quality of `investigation_summary` i.e whether the agent has identified the right root cause or not by seeing each command and its output in the commands array and classify it into one of the following categories: [Good, Needs Improvement, Bad].

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

* Evaluation criterion:
- Does the `investigation_summary` correctly identified the root cause by referencing the given commands and their outputs.

* Evaluation Steps:
1. Begin by examining the sequence of commands executed and their corresponding responses. Determine whether each command completed successfully or encountered issues (e.g., timeouts, SSH errors).
2. Identify if the root cause mentioned in `investigation_summary` is supported by the evidence in the command outputs. If commands timed out or SSH was refused, confirm whether the summary properly reflects this as the cause of investigation failure.
3. Ensure that the summary does not contain any conclusions or diagnostics that are not clearly deducible from the command responses. For instance, if no command output mentions memory usage, the summary must not speculate about memory-related issues.
4. Confirm that the summary stays within the bounds of what was actually observed in the session — it must not hypothesize, predict, or generalize beyond what the evidence supports.
5. Check that the summary should clearly mention what did or did not happen during investigation (e.g., "SSH access failed, investigation could not proceed") and should avoid vague statements like "an error occurred" without context.
6. Validate that the summary's narrative aligns chronologically with the timestamps of command execution. If earlier commands succeeded and later ones failed, the summary should reflect this gradient.

Format the output as JSON with the following keys:
classification: "One of: Good | Needs Improvement | Bad",
justification: "Explain which criteria were satisfied or violated."

Now evaluate the following insight:

<insight>
    {insight}
</insight>

{format_instructions}
``` 