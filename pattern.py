import re

# Define bot-related keywords
# check if name or email contains "bot" not a single word
ex_pattern = re.compile(r"\b.*bot.*\b", re.IGNORECASE)
bot_names_pattern = ["bot", "build", "deploy", "jenkins", "travis", "circleci", "github", "gitlab"]
bot_emails_pattern = ["noreply@github.com", "noreply@github.com.invalid"]
bot_message_patterns = [re.compile(r"\[skip ci]", re.IGNORECASE),
                        re.compile(r"\[ci skip]", re.IGNORECASE),
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
                        re.compile(r"merge", re.IGNORECASE),
                        re.compile(r"gitlab-ci\.yml", re.IGNORECASE)]

added_pattern = [re.compile(r"feat", re.IGNORECASE),
                 re.compile(r"add", re.IGNORECASE),
                 re.compile(r"feature", re.IGNORECASE)]

fixed_pattern = [re.compile(r"fix", re.IGNORECASE),
                 re.compile(r"bug", re.IGNORECASE)]

changed_pattern = [re.compile(r"change", re.IGNORECASE),
                   re.compile(r"changed", re.IGNORECASE),
                   re.compile(r"refactor", re.IGNORECASE),
                   re.compile(r"optimiz", re.IGNORECASE),
                   re.compile(r"update", re.IGNORECASE)]

removed_pattern = [re.compile(r"remove", re.IGNORECASE),
                   re.compile(r"delete", re.IGNORECASE)]

security_pattern = [re.compile(r"auth", re.IGNORECASE),
                    re.compile(r"security", re.IGNORECASE),
                    re.compile(r"password", re.IGNORECASE)]
