# Official Files Policy

## Official source of truth
- Prefer .tsx over .js when both exist
- Prefer current active file over .bak/.stable/.broken variants
- Backup files must not be imported by app routes
- Route imports must point only to official active files

## Cleanup rule
Before major feature work:
1. Identify official file
2. Move obsolete variants to archive later
3. Keep backups outside active route path if needed
