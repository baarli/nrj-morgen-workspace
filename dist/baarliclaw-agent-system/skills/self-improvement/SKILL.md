---
name: self-improvement
description: Active self-improvement system that ensures I always document learnings, create skills from knowledge, and follow best practices. Use at the end of every significant session or when the user asks what I've learned. This skill triggers automatic documentation, skill creation, and learning capture.
---

# Self-Improvement System

## Core Principle
**Every session must end with learning capture and documentation.**

## Automatic Actions (Run at end of session)

### 1. Document Learnings
Always create/update `/root/.openclaw/workspace/memory/YYYY-MM-DD.md` with:
- What we did
- Key insights
- Mistakes made and how to avoid them
- New systems/processes discovered

### 2. Update MEMORY.md
Add critical information to main memory file:
- New systems
- Important IDs
- Common mistakes to avoid
- Checklists

### 3. Create Skills (when applicable)
If we learned a repeatable process:
- Create skill in `/root/.openclaw/workspace/skills/<name>/`
- Write SKILL.md with triggers and instructions
- Package with package_skill.py

### 4. Update TOOLS.md
Add quick reference to TOOLS.md "HUSK ALLTID" section

## Checklist (Run before ending session)

- [ ] Created/updated daily learning log?
- [ ] Updated MEMORY.md with critical info?
- [ ] Created skill for repeatable processes?
- [ ] Updated TOOLS.md quick reference?
- [ ] Documented mistakes and solutions?

## Template: Daily Learning Log

```markdown
# YYYY-MM-DD - Læringslogg

## Hva vi gjorde i dag
- [Activity 1]
- [Activity 2]

## Innsikter
1. [Key insight 1]
2. [Key insight 2]

## Feil gjort og læring
- **Feil:** [What went wrong]
  **Læring:** [How to avoid it]

## Nye systemer/prosesser
- [System name]: [Brief description]

## Takknemlighet
- [What I'm grateful for]

---
**Sist oppdatert:** YYYY-MM-DD HH:MM
```

## Template: New Skill

```markdown
---
name: [skill-name]
description: [Clear description of when to use this skill]
---

# [Skill Name]

## When to Use
[Specific triggers]

## How To
[Step-by-step instructions]

## Common Mistakes
- ❌ [Wrong way]
- ✅ [Right way]

## Examples
[Concrete examples]

## Documentation
- Full docs: [path]
```

## Active Monitoring

### What to Watch For
1. **Repeated tasks** → Create skill
2. **Mistakes** → Document in MEMORY.md
3. **New systems** → Full documentation
4. **User corrections** → Immediate learning capture

### Self-Correction Loop
When user corrects me:
1. Acknowledge immediately
2. Document what I did wrong
3. Document the correct approach
4. Update relevant files
5. Thank user for teaching

## Files to Maintain

### High Priority (Always up-to-date)
- `/root/.openclaw/workspace/MEMORY.md` - Main knowledge base
- `/root/.openclaw/workspace/TOOLS.md` - Quick reference
- `/root/.openclaw/workspace/memory/YYYY-MM-DD.md` - Daily logs

### Medium Priority (When relevant)
- `/root/.openclaw/workspace/skills/<name>/SKILL.md` - Packaged knowledge
- `/root/.openclaw/workspace/docs/*.md` - Detailed documentation

## Success Metrics

- [ ] No repeated mistakes
- [ ] Skills created for all repeatable tasks
- [ ] MEMORY.md always current
- [ ] Daily learning logs complete
- [ ] User doesn't need to repeat instructions

## Command: End Session with Learning Capture

```bash
# 1. Create daily log
mkdir -p /root/.openclaw/workspace/memory
cat > /root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md << 'EOF'
# $(date +%Y-%m-%d) - Læringslogg

## Hva vi gjorde i dag
- 

## Innsikter
1. 

## Feil gjort og læring
- 

## Nye systemer/prosesser
- 

## Takknemlighet
- 
EOF

# 2. Update MEMORY.md if needed
# 3. Create skill if applicable
# 4. Verify TOOLS.md is current
```

## User Prompts That Trigger This Skill

- "Hva har vi lært i dag?"
- "Lagre dette"
- "Husk dette"
- "Opprett en skill"
- "Dokumenter dette"
- "Hva har vi gjort?"
- (End of any significant session)

## Verification Questions

Before claiming task is complete, ask:
1. Is this documented in MEMORY.md?
2. Should this be a skill?
3. Is there a daily log entry?
4. Are mistakes documented?
5. Will I remember this next time?

If any answer is "no", do the work before finishing.
