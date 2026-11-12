# Jdot plugin boundary

Jdot serves a personal assistant user who wants continuity across connected sessions and an explicit Apple Shortcuts handoff. Its portable package is skills-only; Pages account access and tools are supplied by the host.

The domain Skill is `jdot-session`. It starts or resumes Page-connected sessions, captures factual summaries, and links to the Shortcut adaptation reference. Existing workspace and Python execution Skills provide supporting capability guidance. Setup remains a reference within the session Skill rather than another overlapping invocation.

No MCP server, app registration, API key, hidden lifecycle hook, public endpoint, or always-running process is declared. Apple Shortcuts selects inference models. The host's authorized Pages tools read and write memory. Manual Remote transfer remains visible until the intended device path is verified.

| Host capability | Use |
| --- | --- |
| Read, list, search, grep | Preferred for memory resolution and authorized Shortcut or repository inspection |
| Write, patch | Mutation for user-authorized Page updates and repository changes |
| Shell | Optional for repository checks; classify each command by its effects |
| Python | Optional deterministic validation and file processing |

These are host capabilities, not permissions granted by the manifest. Missing Page access produces an explicit unloaded or unsaved state, with no implicit local replacement for cloud memory.

Direct invocation examples are starting Jdot, saving its session summary, and adapting a Shortcut for Jdot. An indirect continuation request should load existing context when the target is clear. Unrelated tasks should not force this workflow. Negative cases include unavailable Page tools, ambiguous memory Pages, uncertain saves, and requests to claim an untested Remote or offline connection works.

Version 0.1.0 is a local development package. The GitHub handle in author metadata identifies the connected repository user; it is not a verified OpenAI publisher claim. Public submission, public legal/listing URLs, account installation, and device acceptance remain outside this generated repository's verified state.
