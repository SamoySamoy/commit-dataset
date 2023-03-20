import re
# Define bot-related keywords
ex_pattern = re.compile(r"\b.*bot.*\b", re.IGNORECASE) # check if name or email contains "bot" not a single word
bot_names_pattern = ["bot", "build", "deploy", "jenkins", "travis", "circleci", "github", "gitlab"]
bot_emails_pattern = ["noreply@github.com", "noreply@github.com.invalid"]
bot_message_patterns = [re.compile(r"\[skip ci\]", re.IGNORECASE),
                re.compile(r"\[ci skip\]", re.IGNORECASE),
                re.compile(r"no\s+tests?", re.IGNORECASE),
                re.compile(r"auto-generated", re.IGNORECASE),
                re.compile(r"automated\s+build", re.IGNORECASE),
                re.compile(r"continuous\s+integration", re.IGNORECASE),
                re.compile(r"test\s+automation", re.IGNORECASE),
                re.compile(r"ci/cd", re.IGNORECASE),
                re.compile(r"pipeline", re.IGNORECASE),
                re.compile(r"dependenc", re.IGNORECASE),
                re.compile(r"jenkinsfile", re.IGNORECASE),
                re.compile(r"travis\.yml", re.IGNORECASE),
                re.compile(r"circle\.yml", re.IGNORECASE),
                re.compile(r"bump", re.IGNORECASE),
                re.compile(r"chore", re.IGNORECASE),
                re.compile(r"gitlab-ci\.yml", re.IGNORECASE)]
