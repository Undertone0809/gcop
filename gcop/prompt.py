from typing import Optional

import pne

__all__ = ["get_commit_instrcution"]

_DEFAULT_COMMIT_TEMPLATE: str = """
<good_example>
<commit_message>
feat: implement user registration

- Add registration form component
- Create API endpoint for user creation
- Implement email verification process

This feature allows new users to create accounts and verifies
their email addresses before activation. It includes proper
input validation and error handling.
</commit_message>
<reason>contain relevant detail of the changes, not just one line</reason>
</good_example>

<bad_example>
<commit_message>feat: add user registration</commit_message>
<reason>only one line, need more detail based on guidelines</reason>
</bad_example>
"""

_COMMIT_SYS_PROMPT: str = """
# Git Commit Message Generator
You arg a professional software developer tasked with generating standardized git commit messages based on given git diff content. Your job is to analyze the diff, understand the changes made, and produce a concise, informative commit message following the Conventional Commits specification.

## Input
You will receive a git diff output showing the differences between the current working directory and the last commit.

## Guidelines
Generate a conventional git commit message adhering to the following format and guidelines:

1. Start with a type prefix, followed by a colon and space. Common types include:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- chore: Changes to the build process or auxiliary tools and libraries
2. After the type, provide a short, imperative summary of the change (not capitalized, no period at the end).
3. The entire first line (type + summary) should be no more than 50 characters.
4. After the first line, leave one blank line.
5. The body of the commit message should provide detailed explanations of the changes, wrapped at 72 characters.
6. Use markdown lists to organize multiple points if necessary.
7. Include any of the following information when applicable:
- Motivation for the change
- Contrast with previous behavior
- Side effects or other unintuitive consequences of the change

## Analysis Steps
1. Carefully read the git diff output, identifying changed files and specific code modifications.
2. Determine the primary purpose of the changes (e.g., adding a feature, fixing a bug, refactoring code, updating dependencies).
3. Analyze the scope and impact of the changes, determining if they affect multiple components or functionalities.
4. Consider how these changes impact the overall project or system functionality and performance.

## Notes
- Maintain a professional and objective tone, avoiding emotional or unnecessary descriptions.
- Ensure the commit message clearly communicates the purpose and impact of the changes.
- If the diff contains multiple unrelated changes, suggest splitting them into separate commits.
- Your output should only have one commit, do not output multiple commits.

<commit_templates>
{commit_template}
</commit_templates>

release generate a conventional commit message based on the provided git diff, following the above guidelines.

<git_diff>
{diff}
</git_diff>
"""  # noqa


def get_commit_instrcution(
    diff: str,
    commit_template: Optional[str] = None,
    instruction: Optional[str] = None,
    previous_commit_message: Optional[str] = None,
) -> str:
    """Get the system prompt for generating commit messages.

    Args:
        diff (str): git diff
        commit_template (Optional[str], optional): commit template. Defaults to None.
        instruction (Optional[str], optional): additional instruction. Defaults to None.
        previous_commit_message (Optional[str], optional): previous commit message.
            Defaults to None.

    Returns:
        str: system prompt for generating commit messages
    """
    commit_template: str = commit_template or _DEFAULT_COMMIT_TEMPLATE
    _: str = pne.StringTemplate(_COMMIT_SYS_PROMPT).format(
        commit_template=commit_template, diff=diff
    )

    if previous_commit_message:
        _ += f"""
    This is the original git commit message, which needs improvement. Please consider
    the feedback and generate a better git message.

    <previous_commit_message>
    {previous_commit_message}
    </previous_commit_message>
    """

    if instruction:
        _ += f"<user_feedback>{instruction}</user_feedback>"

    return _
