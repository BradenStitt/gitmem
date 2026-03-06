"""Default content templates for .gitmem/ workspace files."""

HEAD_DEFAULT = "main"

MAIN_MD_DEFAULT = "# Project Roadmap\n"

COMMIT_MD_DEFAULT = ""

LOG_MD_DEFAULT = ""

METADATA_YAML_TEMPLATE = """\
name: {name}
parent: {parent}
purpose: {purpose}
created_at: "{created_at}"
status: {status}
"""
