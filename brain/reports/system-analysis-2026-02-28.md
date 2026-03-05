# System-Wide Code Quality Analysis Report

**Generated:** 2026-02-28 05:07:10
**Workspace:** /root/.openclaw/workspace

## Executive Summary

- **Total files analyzed:** 195
- **Files with issues:** 195 (100.0%)
- **Total issues found:** 810
- **Security issues:** 30
- **Performance issues:** 78
- **Documentation gaps:** 138
- **Error handling issues:** 48

## Priority Matrix

| Priority | Category | Count | Action Required |
|----------|----------|-------|-----------------|
| 🔴 CRITICAL | Security Vulnerabilities | 6 | Immediate fix required |
| 🟠 HIGH | Error Handling | 48 | Fix within 1 week |
| 🟡 MEDIUM | Performance Issues | 78 | Address in next sprint |
| 🟢 LOW | Documentation Gaps | 138 | Address when convenient |

## 🔴 Security Vulnerabilities

| File | Issue | Severity |
|------|-------|----------|
| /scripts/daily-podcast-email.py | os.system() - command injection risk | MEDIUM |
| /scripts/daily-podcast-email.py | Hardcoded password detected | MEDIUM |
| /scripts/cli_toolkit.py | Use of input() - consider security implications | MEDIUM |
| /scripts/system_analyzer.py | os.system() - command injection risk | MEDIUM |
| /scripts/system_analyzer.py | Use of input() - consider security implications | MEDIUM |
| /scripts/import_nielsen_spreadsheet.py | os.system() - command injection risk | MEDIUM |
| /scripts/smart_backup_service.py | MD5 is cryptographically broken | MEDIUM |
| /scripts/brave-news-search-v2.py | Hardcoded API key detected | MEDIUM |
| /scripts/podcast-clipper.py | os.system() - command injection risk | MEDIUM |
| /scripts/live-search-api.py | Hardcoded API key detected | MEDIUM |
| /scripts/openai-generate-title.py | Hardcoded API key detected | MEDIUM |
| /scripts/generate_and_send_showprep.py | Hardcoded password detected | MEDIUM |
| /scripts/daily-podcast-email-v2.py | os.system() - command injection risk | MEDIUM |
| /scripts/daily-podcast-email-v2.py | Hardcoded password detected | MEDIUM |
| /scripts/send-mission-control-email.py | Hardcoded password detected | MEDIUM |
| /scripts/baarliclaw_toolkit.py | MD5 is cryptographically broken | MEDIUM |
| /scripts/uuid_toolkit.py | MD5 is cryptographically broken | MEDIUM |
| /scripts/file_toolkit.py | MD5 is cryptographically broken | MEDIUM |
| /scripts/quick-news-search.py | Hardcoded API key detected | MEDIUM |
| /scripts/cache_toolkit.py | MD5 is cryptographically broken | MEDIUM |
| /mission-control/api/security_hardening.py | MD5 is cryptographically broken | MEDIUM |
| /scripts/send-daily-email.sh | Command substitution with backticks - use $() instead | MEDIUM |
| /scripts/live-search.sh | Hardcoded API key | MEDIUM |
| /scripts/deploy-total-control.sh | Hardcoded token | MEDIUM |
| /scripts/system_analyzer.py | Use of eval() - dangerous code execution | HIGH |
| /scripts/system_analyzer.py | Use of exec() - dangerous code execution | HIGH |
| /scripts/security_toolkit.py | Use of eval() - dangerous code execution | HIGH |
| /scripts/security_toolkit.py | Use of exec() - dangerous code execution | HIGH |
| /scripts/serialization_toolkit.py | pickle usage - can execute arbitrary code | HIGH |
| /scripts/cache_toolkit.py | pickle usage - can execute arbitrary code | HIGH |

## 🟠 Error Handling Issues

| File | Issue |
|------|-------|
| /scripts/generate-mission-control-pages.py | Missing try/except for I/O or network operations |
| /scripts/regenerate-ui-2026.py | Missing try/except for I/O or network operations |
| /scripts/io_toolkit.py | Missing try/except for I/O or network operations |
| /scripts/build-mc-2026.py | Missing try/except for I/O or network operations |
| /scripts/report_generator.py | Missing try/except for I/O or network operations |
| /scripts/insert_to_supabase.py | Missing try/except for I/O or network operations |
| /nrjmorgen-ui/scripts/generate_component.py | Missing try/except for I/O or network operations |
| /api/status.sh | Missing 'set -e' for error handling |
| /mission-control/server.sh | Missing 'set -e' for error handling |
| /scripts/auto-sync-mission-control.sh | Missing 'set -e' for error handling |
| /scripts/auto-skill-selector.sh | Missing 'set -e' for error handling |
| /scripts/auto-exec-enforcer-cron.sh | Missing 'set -e' for error handling |
| /scripts/calendar-today.sh | Missing 'set -e' for error handling |
| /scripts/verify-podcast-system.sh | Missing 'set -e' for error handling |
| /scripts/self-dev-task-generator.sh | Missing 'set -e' for error handling |
| /scripts/build-mission-control-2026.sh | Missing 'set -e' for error handling |
| /scripts/send-daily-email.sh | Missing 'set -e' for error handling |
| /scripts/visualize-data.sh | Missing 'set -e' for error handling |
| /scripts/forecast-trends.sh | Missing 'set -e' for error handling |
| /scripts/research-topic.sh | Missing 'set -e' for error handling |
| /scripts/daily-email-report.sh | Missing 'set -e' for error handling |
| /scripts/auto-update-all-knowledge.sh | Missing 'set -e' for error handling |
| /scripts/live-search.sh | Missing 'set -e' for error handling |
| /scripts/continuous-autonomous-operation.sh | Missing 'set -e' for error handling |
| /scripts/notify-user.sh | Missing 'set -e' for error handling |
| /scripts/skill-health-check.sh | Missing 'set -e' for error handling |
| /scripts/dashboard.sh | Missing 'set -e' for error handling |
| /scripts/voice-transcribe.sh | Missing 'set -e' for error handling |
| /scripts/autonomous-mission-control.sh | Missing 'set -e' for error handling |
| /scripts/meeting-prep.sh | Missing 'set -e' for error handling |

## 🟡 Performance Bottlenecks

| File | Issue |
|------|-------|
| /scripts/data_analyzer.py | Using range(len()) - use enumerate() instead |
| /scripts/data_analyzer.py | List building in loop - use list comprehension |
| /scripts/fetch_nrj_dashboard_stats_v2.py | read() loads entire file - consider chunked reading |
| /scripts/daily-podcast-email.py | read() loads entire file - consider chunked reading |
| /scripts/email_toolkit.py | read() loads entire file - consider chunked reading |
| /scripts/generate-mission-control-pages.py | read() loads entire file - consider chunked reading |
| /scripts/testing_toolkit.py | List building in loop - use list comprehension |
| /scripts/regenerate-ui-2026.py | read() loads entire file - consider chunked reading |
| /scripts/autonomous-watchdog.py | read() loads entire file - consider chunked reading |
| /scripts/system_analyzer.py | List building in loop - use list comprehension |
| /scripts/system_analyzer.py | readlines() loads entire file - consider iteration |
| /scripts/system_analyzer.py | read() loads entire file - consider chunked reading |
| /scripts/content-hub-api.py | read() loads entire file - consider chunked reading |
| /scripts/security_audit_service.py | read() loads entire file - consider chunked reading |
| /scripts/web_scraper.py | read() loads entire file - consider chunked reading |
| /scripts/io_toolkit.py | read() loads entire file - consider chunked reading |
| /scripts/generate-showprepp.py | read() loads entire file - consider chunked reading |
| /scripts/perfect_clip_finder.py | List building in loop - use list comprehension |
| /scripts/event_toolkit.py | Global variable usage - consider encapsulation |
| /scripts/trigger_nrj_dashboard_update.py | read() loads entire file - consider chunked reading |
| /scripts/update_article_images.py | read() loads entire file - consider chunked reading |
| /scripts/security_toolkit.py | read() loads entire file - consider chunked reading |
| /scripts/podcast-clipper.py | read() loads entire file - consider chunked reading |
| /scripts/live-search-api.py | List building in loop - use list comprehension |
| /scripts/live-search-api.py | read() loads entire file - consider chunked reading |
| /scripts/auto_doc_generator.py | List building in loop - use list comprehension |
| /scripts/auto_doc_generator.py | read() loads entire file - consider chunked reading |
| /scripts/monitor-topic.py | read() loads entire file - consider chunked reading |
| /scripts/agent_orchestrator.py | List building in loop - use list comprehension |
| /scripts/openai-generate-title.py | read() loads entire file - consider chunked reading |

## 🟢 Documentation Gaps

| File | Type |
|------|------|
| /scripts/data_analyzer.py | Missing module docstring |
| /scripts/fetch_nrj_dashboard_stats_v2.py | Missing module docstring |
| /scripts/daily-podcast-email.py | Missing module docstring |
| /scripts/email_toolkit.py | Missing module docstring |
| /scripts/test_skills_lib.py | Missing module docstring |
| /scripts/dashboard_builder.py | Missing module docstring |
| /scripts/generate-mission-control-pages.py | Missing module docstring |
| /scripts/testing_toolkit.py | Missing module docstring |
| /scripts/cli_toolkit.py | Missing module docstring |
| /scripts/daily-podcast-with-skills.py | Missing module docstring |
| /scripts/regenerate-ui-2026.py | Missing module docstring |
| /scripts/autonomous-watchdog.py | Missing module docstring |
| /scripts/smart-generate-title.py | Missing module docstring |
| /scripts/system_analyzer.py | Missing module docstring |
| /scripts/update_nielsen_radio_stats.py | Missing module docstring |
| /scripts/import_nielsen_spreadsheet.py | Missing module docstring |
| /scripts/content-hub-api.py | Missing module docstring |
| /scripts/ai-research-module.py | Missing module docstring |
| /scripts/security_audit_service.py | Missing module docstring |
| /scripts/web_scraper.py | Missing module docstring |
| /scripts/log_analyzer.py | Missing module docstring |
| /scripts/smart_backup_service.py | Missing module docstring |
| /scripts/date_toolkit.py | Missing module docstring |
| /scripts/decorator_toolkit.py | Missing module docstring |
| /scripts/radio-stats-updater-v2.py | Missing module docstring |
| /scripts/io_toolkit.py | Missing module docstring |
| /scripts/cicd_toolkit.py | Missing module docstring |
| /scripts/configuration_manager.py | Missing module docstring |
| /scripts/performance_profiler.py | Missing module docstring |
| /scripts/generate-showprepp.py | Missing module docstring |

## Code Quality Statistics

### Most Complex Files

| File | Complexity | Functions | Classes | Lines |
|------|------------|-----------|---------|-------|
| /mission-control/api/total-control-api.py | 249 | 79 | 6 | 1646 |
| /mission-control/api/security_hardening.py | 116 | 26 | 5 | 631 |
| /scripts/system_analyzer.py | 109 | 15 | 1 | 575 |
| /scripts/ml_toolkit.py | 102 | 23 | 5 | 435 |
| /scripts/docs_toolkit.py | 85 | 18 | 6 | 493 |
| /scripts/perfect_clip_finder.py | 76 | 16 | 1 | 486 |
| /scripts/perfect-clip-finder.py | 76 | 16 | 1 | 486 |
| /scripts/data_analyzer.py | 75 | 18 | 3 | 409 |
| /scripts/api_builder.py | 74 | 36 | 4 | 344 |
| /scripts/testing_toolkit.py | 71 | 32 | 5 | 294 |
| /scripts/consolidated-morning-routine.py | 71 | 15 | 0 | 594 |
| /scripts/baarliclaw_toolkit.py | 70 | 25 | 3 | 334 |
| /scripts/brave-news-search.py | 67 | 9 | 0 | 430 |
| /scripts/automation_engine.py | 66 | 23 | 4 | 435 |
| /scripts/import_nielsen_spreadsheet.py | 65 | 5 | 0 | 366 |

### Largest Files

| File | Lines | Code | Comments | Blank |
|------|-------|------|----------|-------|
| /mission-control/api/total-control-api.py | 1646 | 1315 | 94 | 237 |
| /scripts/build-mc-2026.py | 636 | 556 | 3 | 77 |
| /mission-control/api/security_hardening.py | 631 | 460 | 54 | 117 |
| /scripts/consolidated-morning-routine.py | 594 | 444 | 27 | 123 |
| /scripts/build-mission-control-2026.sh | 582 | 481 | 13 | 88 |
| /scripts/system_analyzer.py | 575 | 460 | 41 | 74 |
| /skills/code-quality-checker/check-quality.sh | 548 | 409 | 60 | 79 |
| /scripts/dashboard_builder.py | 505 | 433 | 10 | 62 |
| /scripts/docs_toolkit.py | 493 | 387 | 17 | 89 |
| /scripts/perfect_clip_finder.py | 486 | 339 | 45 | 102 |
| /scripts/perfect-clip-finder.py | 486 | 339 | 45 | 102 |
| /scripts/video_toolkit.py | 449 | 374 | 13 | 62 |
| /scripts/automation_engine.py | 435 | 347 | 18 | 70 |
| /scripts/ml_toolkit.py | 435 | 307 | 28 | 100 |
| /scripts/brave-news-search.py | 430 | 324 | 29 | 77 |

### Files with Most Issues

| File | Issues |
|------|--------|
| /scripts/api_builder.py | 25 |
| /mission-control/api/backend-v2.py | 18 |
| /scripts/testing_toolkit.py | 17 |
| /scripts/bot_toolkit.py | 16 |
| /mission-control/api/total-control-api.py | 16 |
| /scripts/decorator_toolkit.py | 15 |
| /scripts/system_analyzer.py | 12 |
| /mission-control/api/backend.py | 12 |
| /mission-control/api/backend-simple.py | 12 |
| /scripts/import_nielsen_spreadsheet.py | 11 |
| /scripts/baarliclaw_toolkit.py | 11 |
| /scripts/event_toolkit.py | 10 |
| /scripts/state_toolkit.py | 10 |
| /scripts/cache_toolkit.py | 10 |
| /scripts/performance_profiler.py | 9 |

## Potential Code Duplication

### Common import: os
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/test_skills_lib.py
- /scripts/dashboard_builder.py

### Common import: sys
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/test_skills_lib.py
- /scripts/dashboard_builder.py

### Common import: json
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/fetch_nrj_dashboard_stats_v2.py
- /scripts/daily-podcast-email.py
- /scripts/dashboard_builder.py
- /scripts/daily-podcast-with-skills.py

### Common import: datetime
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/fetch_nrj_dashboard_stats_v2.py
- /scripts/daily-podcast-email.py
- /scripts/test_skills_lib.py
- /scripts/dashboard_builder.py

### Common import: timedelta
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/autonomous-watchdog.py
- /scripts/date_toolkit.py
- /scripts/generate-showprepp.py
- /scripts/security_toolkit.py

### Common import: Dict
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/email_toolkit.py
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/cli_toolkit.py

### Common import: List
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/email_toolkit.py
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/cli_toolkit.py

### Common import: Optional
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/email_toolkit.py
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/cli_toolkit.py

### Common import: Tuple
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/system_analyzer.py
- /scripts/log_analyzer.py
- /scripts/date_toolkit.py
- /scripts/perfect_clip_finder.py

### Common import: Any
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/cli_toolkit.py
- /scripts/security_audit_service.py

### Common import: Counter
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/log_analyzer.py
- /scripts/collections_toolkit.py
- /scripts/log_analyzer_service.py
- /scripts/math_toolkit.py

### Common import: setup_logging
Found in 5 files:
- /scripts/data_analyzer.py
- /scripts/email_toolkit.py
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/security_audit_service.py

### Common import: urllib.request
Found in 5 files:
- /scripts/fetch_nrj_dashboard_stats_v2.py
- /scripts/daily-podcast-email.py
- /scripts/autonomous-watchdog.py
- /scripts/update_nielsen_radio_stats.py
- /scripts/import_nielsen_spreadsheet.py

### Common import: argparse
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/cli_toolkit.py
- /scripts/daily-podcast-with-skills.py
- /scripts/radio-stats-updater-v2.py
- /scripts/perfect_clip_finder.py

### Common import: re
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/generate-mission-control-pages.py
- /scripts/daily-podcast-with-skills.py
- /scripts/regenerate-ui-2026.py
- /scripts/smart-generate-title.py

### Common import: smtplib
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/generate_and_send_showprep.py
- /scripts/send-daily-email.py
- /scripts/daily-podcast-email-v2.py

### Common import: MIMEBase
Found in 4 files:
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/daily-podcast-email-v2.py
- /scripts/send-mission-control-email.py

### Common import: MIMEMultipart
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/generate_and_send_showprep.py
- /scripts/send-daily-email.py
- /scripts/daily-podcast-email-v2.py

### Common import: MIMEText
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/generate_and_send_showprep.py
- /scripts/send-daily-email.py
- /scripts/daily-podcast-email-v2.py

### Common import: Path
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/daily-podcast-with-skills.py
- /scripts/system_analyzer.py
- /scripts/import_nielsen_spreadsheet.py
- /scripts/content-hub-api.py

### Common import: xml.etree.ElementTree
Found in 5 files:
- /scripts/daily-podcast-email.py
- /scripts/podcast-clipper.py
- /scripts/daily-podcast-email-v2.py
- /scripts/fetch-podcast.py
- /mission-control/api/total-control-api.py

### Common import: encoders
Found in 4 files:
- /scripts/daily-podcast-email.py
- /scripts/email_toolkit.py
- /scripts/daily-podcast-email-v2.py
- /scripts/send-mission-control-email.py

### Common import: dataclass
Found in 5 files:
- /scripts/email_toolkit.py
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/ai-research-module.py
- /scripts/security_audit_service.py

### Common import: Callable
Found in 5 files:
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/cli_toolkit.py
- /scripts/log_analyzer.py
- /scripts/decorator_toolkit.py

### Common import: field
Found in 5 files:
- /scripts/dashboard_builder.py
- /scripts/testing_toolkit.py
- /scripts/cicd_toolkit.py
- /scripts/state_toolkit.py
- /mission-control/api/security_hardening.py

### Common import: subprocess
Found in 5 files:
- /scripts/dashboard_builder.py
- /scripts/autonomous-watchdog.py
- /scripts/cicd_toolkit.py
- /scripts/dependency_checker.py
- /scripts/auto-insert-top10.py

### Common import: time
Found in 5 files:
- /scripts/testing_toolkit.py
- /scripts/cli_toolkit.py
- /scripts/autonomous-watchdog.py
- /scripts/web_scraper.py
- /scripts/log_analyzer.py

### Common import: traceback
Found in 4 files:
- /scripts/testing_toolkit.py
- /scripts/error_toolkit.py
- /scripts/consolidated-morning-routine.py
- /mission-control/api/total-control-api.py

### Common import: random
Found in 5 files:
- /scripts/autonomous-watchdog.py
- /scripts/web_scraper.py
- /scripts/autonomous-task-generator.py
- /scripts/color_toolkit.py
- /scripts/metrics_collector.py

### Common import: defaultdict
Found in 5 files:
- /scripts/system_analyzer.py
- /scripts/log_analyzer.py
- /scripts/performance_profiler.py
- /scripts/metrics_collector.py
- /scripts/collections_toolkit.py

### Common import: csv
Found in 4 files:
- /scripts/import_nielsen_spreadsheet.py
- /scripts/io_toolkit.py
- /scripts/data_transform_toolkit.py
- /scripts/fetch_podtoppen_live.py

### Common import: shutil
Found in 5 files:
- /scripts/content-hub-api.py
- /scripts/smart_backup_service.py
- /scripts/cicd_toolkit.py
- /scripts/cicd_toolkit.py
- /scripts/video-to-audio-pipeline.py

### Common import: requests
Found in 5 files:
- /scripts/ai-research-module.py
- /scripts/generate_and_send_showprep.py
- /scripts/supabase-publisher.py
- /scripts/image_toolkit.py
- /scripts/content-pipeline-v3.py

### Common import: logging
Found in 5 files:
- /scripts/ai-research-module.py
- /scripts/decorator_toolkit.py
- /scripts/baarliclaw_toolkit.py
- /scripts/supabase-publisher.py
- /scripts/content-pipeline-v3.py

### Common import: hashlib
Found in 5 files:
- /scripts/security_audit_service.py
- /scripts/smart_backup_service.py
- /scripts/security_toolkit.py
- /scripts/security_toolkit.py
- /scripts/baarliclaw_toolkit.py

### Common import: asdict
Found in 5 files:
- /scripts/security_audit_service.py
- /scripts/smart_backup_service.py
- /scripts/configuration_manager.py
- /scripts/metrics_collector.py
- /scripts/health_check_service.py

### Common import: DateUtils
Found in 5 files:
- /scripts/security_audit_service.py
- /scripts/smart_backup_service.py
- /scripts/configuration_manager.py
- /scripts/brave-news-search-v2.py
- /scripts/agent_orchestrator.py

### Common import: TerminalUI
Found in 5 files:
- /scripts/security_audit_service.py
- /scripts/smart_backup_service.py
- /scripts/configuration_manager.py
- /scripts/agent_orchestrator.py
- /scripts/metrics_collector.py

### Common import: Colors
Found in 5 files:
- /scripts/security_audit_service.py
- /scripts/smart_backup_service.py
- /scripts/configuration_manager.py
- /scripts/agent_orchestrator.py
- /scripts/metrics_collector.py

### Common import: urlparse
Found in 5 files:
- /scripts/web_scraper.py
- /scripts/update_article_images.py
- /scripts/url_toolkit.py
- /scripts/extract-video-urls.py
- /scripts/network_toolkit.py

### Common import: UUIDUtils
Found in 5 files:
- /scripts/smart_backup_service.py
- /scripts/smart_notification_service.py
- /scripts/task_queue_manager.py
- /scripts/api_gateway_service.py
- /scripts/toolkit-integration-demo.py

### Common import: Union
Found in 4 files:
- /scripts/date_toolkit.py
- /scripts/validation_toolkit.py
- /scripts/data_transform_toolkit.py
- /scripts/database_toolkit.py

### Common import: Enum
Found in 4 files:
- /scripts/cicd_toolkit.py
- /scripts/scheduler_toolkit.py
- /scripts/task_queue_manager.py
- /scripts/automation_engine.py

### Common import: yaml
Found in 4 files:
- /scripts/configuration_manager.py
- /scripts/config_toolkit.py
- /scripts/config_toolkit.py
- /scripts/config_toolkit.py

### Common import: urllib.parse
Found in 5 files:
- /scripts/generate-showprepp.py
- /scripts/update_article_images.py
- /scripts/morning-routine-v2.1.py
- /scripts/brave-news-search-parallel.py
- /scripts/baarliclaw_toolkit.py

### Common import: math
Found in 5 files:
- /scripts/perfect_clip_finder.py
- /scripts/perfect-clip-finder.py
- /scripts/chart_toolkit.py
- /scripts/math_toolkit.py
- /scripts/ml_toolkit.py

### Common import: urllib.error
Found in 5 files:
- /scripts/live-search-api.py
- /scripts/openai-generate-title.py
- /scripts/baarliclaw_toolkit.py
- /scripts/extract-video-urls.py
- /scripts/radio-stats-updater.py

### Common import: concurrent.futures
Found in 5 files:
- /scripts/morning-routine-v2.1.py
- /scripts/brave-news-search-parallel.py
- /scripts/morning-routine-v2.py
- /scripts/consolidated-morning-routine.py
- /scripts/brave-news-search.py

### Common import: uuid
Found in 5 files:
- /scripts/morning-routine-v2.1.py
- /scripts/auto-insert-top10.py
- /scripts/morning-routine-v2.py
- /scripts/uuid_toolkit.py
- /mission-control/api/total-control-api.py

### Common import: threading
Found in 5 files:
- /scripts/scheduler_toolkit.py
- /scripts/api_builder.py
- /scripts/automation_engine.py
- /mission-control/api/backend-v2.py
- /mission-control/api/test-api.py

### Common import: wraps
Found in 5 files:
- /scripts/baarliclaw_toolkit.py
- /scripts/error_toolkit.py
- /scripts/functional_toolkit.py
- /scripts/cache_toolkit.py
- /mission-control/api/security_hardening.py

### Common import: HTTPServer
Found in 5 files:
- /scripts/api_builder.py
- /scripts/api_gateway_service.py
- /mission-control/api/ai-suggestions-api.py
- /mission-control/api/backend-v2.py
- /mission-control/api/backend.py

### Common import: BaseHTTPRequestHandler
Found in 5 files:
- /scripts/api_builder.py
- /scripts/api_gateway_service.py
- /mission-control/api/ai-suggestions-api.py
- /mission-control/api/backend-v2.py
- /mission-control/api/backend.py

### Common import: psutil
Found in 4 files:
- /scripts/process_toolkit.py
- /scripts/performance_monitor.py
- /mission-control/api/real-api.py
- /mission-control/api/total-control-api.py

## Detailed Issues by File

### /.config/QUICK_REF.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /api/status.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /mission-control/api/ai-suggestions-api.py

- Class 'AIHandler' missing docstring
- Function 'main' missing docstring
- Function 'do_OPTIONS' missing docstring
- Function 'do_POST' missing docstring
- Function 'handle_suggest' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /mission-control/api/api-service.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- BEST PRACTICE: 13 potentially unquoted variable usages

### /mission-control/api/api.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 6 potentially unquoted variable usages

### /mission-control/api/backend-simple.py

- Class 'APIHandler' missing docstring
- Function 'do_GET' missing docstring
- Function 'do_POST' missing docstring
- Function 'do_OPTIONS' missing docstring
- Function 'get_status' missing docstring
- Function 'get_logs' missing docstring
- Function 'get_automations' missing docstring
- Function 'control_automation' missing docstring
- Function 'get_nrj_stats' missing docstring
- Function 'log_message' missing docstring
- ... and 2 more issues

### /mission-control/api/backend-v2.py

- Class 'APIHandler' missing docstring
- Function 'do_GET' missing docstring
- Function 'do_POST' missing docstring
- Function 'do_OPTIONS' missing docstring
- Function 'get_status' missing docstring
- Function 'get_logs' missing docstring
- Function 'get_automations' missing docstring
- Function 'get_nrj_stats' missing docstring
- Function 'control_automation' missing docstring
- Function 'get_morning_routine_status' missing docstring
- ... and 8 more issues

### /mission-control/api/backend.py

- Class 'APIHandler' missing docstring
- Function 'do_GET' missing docstring
- Function 'do_POST' missing docstring
- Function 'do_OPTIONS' missing docstring
- Function 'get_status' missing docstring
- Function 'get_logs' missing docstring
- Function 'get_automations' missing docstring
- Function 'control_automation' missing docstring
- Function 'get_nrj_stats' missing docstring
- Function 'log_message' missing docstring
- ... and 2 more issues

### /mission-control/api/data-api.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /mission-control/api/real-api.py

- High complexity function 'get_automations' (score: 11)
- PERFORMANCE: readlines() loads entire file - consider iteration
- DOCUMENTATION: Missing module docstring

### /mission-control/api/security_hardening.py

- High complexity function 'validate_sak_data' (score: 15)
- Function '__init__' missing docstring
- Function 'decorator' missing docstring
- Function 'wrapper' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- SECURITY: MD5 is cryptographically broken
- PERFORMANCE: List building in loop - use list comprehension
- DOCUMENTATION: Missing module docstring

### /mission-control/api/start-backend.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 9 potentially unquoted variable usages

### /mission-control/api/test-api.py

- Function 'main' missing docstring
- Function 'on_message' missing docstring
- Function 'on_error' missing docstring
- Function 'on_close' missing docstring
- Function 'on_open' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /mission-control/api/total-control-api.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'wrapper' missing docstring
- High complexity function 'check_auth' (score: 11)
- High complexity function '_route_request' (score: 18)
- Function 'do_GET' missing docstring
- Function 'do_POST' missing docstring
- Function 'do_PATCH' missing docstring
- ... and 6 more issues

### /mission-control/deploy-external.sh

- ERROR HANDLING: No explicit command error checking

### /mission-control/deploy.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 7 potentially unquoted variable usages

### /mission-control/server.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 20 potentially unquoted variable usages

### /nrjmorgen-ui/fix_catch_blocks_lib.py

- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /nrjmorgen-ui/scripts/deploy-functions.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /nrjmorgen-ui/scripts/generate_component.py

- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /nrjmorgen-ui/scripts/validate_accessibility.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/agent-dashboard.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 14 potentially unquoted variable usages

### /scripts/agent-wrapper.sh

- ERROR HANDLING: No explicit command error checking

### /scripts/agent_orchestrator.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- PERFORMANCE: List building in loop - use list comprehension
- DOCUMENTATION: Missing module docstring

### /scripts/ai-generate-title.py

- High complexity function 'simple_format' (score: 12)
- Function 'main' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/ai-research-module.py

- Function '__init__' missing docstring
- High complexity function '_analyze_findings' (score: 11)
- DOCUMENTATION: Missing module docstring

### /scripts/api_builder.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'run' missing docstring
- Function 'root' missing docstring
- Function 'get_user' missing docstring
- Function 'create_user' missing docstring
- Function 'decorator' missing docstring
- Function 'decorator' missing docstring
- Function 'decorator' missing docstring
- Function 'decorator' missing docstring
- ... and 15 more issues

### /scripts/api_gateway_service.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'root' missing docstring
- Function 'health' missing docstring
- Function 'stats' missing docstring
- Function 'echo' missing docstring
- Function 'services' missing docstring
- Function 'decorator' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/async_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'slow_square' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/auto-exec-enforcer-cron.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 14 potentially unquoted variable usages

### /scripts/auto-exec-enforcer.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 15 potentially unquoted variable usages

### /scripts/auto-insert-top10.py

- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/auto-learning-capture.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 11 potentially unquoted variable usages

### /scripts/auto-skill-selector.sh

- ERROR HANDLING: Missing 'set -e' or error handling options

### /scripts/auto-sync-mission-control.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /scripts/auto-update-all-knowledge.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 7 potentially unquoted variable usages

### /scripts/auto_doc_generator.py

- Function '__init__' missing docstring
- High complexity function 'generate_markdown_docs' (score: 15)
- PERFORMANCE: List building in loop - use list comprehension
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/automation_engine.py

- Class 'TaskStatus' missing docstring
- Function '__post_init__' missing docstring
- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'test_func' missing docstring
- Function 'on_complete' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/autonomous-mission-control.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 20 potentially unquoted variable usages

### /scripts/autonomous-mode.sh

- ERROR HANDLING: No explicit command error checking

### /scripts/autonomous-task-generator.py

- Class 'AutonomousTaskGenerator' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/autonomous-watchdog.py

- Class 'AutonomousWatchdog' missing docstring
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/baarliclaw_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'decorator' missing docstring
- Function 'decorator' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Function 'wrapper' missing docstring
- Function 'wrapper' missing docstring
- SECURITY: MD5 is cryptographically broken
- PERFORMANCE: read() loads entire file - consider chunked reading
- ... and 1 more issues

### /scripts/bot_toolkit.py

- Function '__post_init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'help_cmd' missing docstring
- Function 'status_cmd' missing docstring
- Function 'time_cmd' missing docstring
- Function 'ping_cmd' missing docstring
- Function 'help_cmd' missing docstring
- Function 'ping_cmd' missing docstring
- Function 'info_cmd' missing docstring
- ... and 6 more issues

### /scripts/brainstorm-ideas.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 12 potentially unquoted variable usages

### /scripts/brave-news-search-parallel.py

- High complexity function 'main' (score: 18)
- Function 'main' missing docstring
- Function 'priority' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/brave-news-search-v2.py

- SECURITY: Hardcoded API key detected
- DOCUMENTATION: Missing module docstring

### /scripts/brave-news-search.py

- High complexity function 'explain_why_nrj' (score: 16)
- High complexity function 'main' (score: 18)
- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/build-mc-2026.py

- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /scripts/build-mission-control-2026.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 15 potentially unquoted variable usages

### /scripts/cache_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'fibonacci' missing docstring
- Function 'decorator' missing docstring
- Function 'decorator' missing docstring
- Function 'wrapper' missing docstring
- Function 'wrapper' missing docstring
- SECURITY: pickle usage - can execute arbitrary code
- SECURITY: MD5 is cryptographically broken
- DOCUMENTATION: Missing module docstring

### /scripts/calendar-today.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 8 potentially unquoted variable usages

### /scripts/chart_toolkit.py

- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/cicd_toolkit.py

- Class 'StepStatus' missing docstring
- Function 'duration_ms' missing docstring
- Function 'success' missing docstring
- Function 'failed_steps' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/cli_toolkit.py

- Function '__init__' missing docstring
- SECURITY: Use of input() - consider security implications
- DOCUMENTATION: Missing module docstring

### /scripts/code_metrics_analyzer.py

- Function '__init__' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/collections_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/color_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/config_toolkit.py

- Function '__init__' missing docstring
- High complexity function '_load_file' (score: 11)
- High complexity function 'validate' (score: 11)
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/configuration_manager.py

- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/consolidated-morning-routine.py

- Function 'main' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/content-hub-api.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring
- DOCUMENTATION: 2 TODO/FIXME comments found

### /scripts/content-pipeline-v3.py

- Function '__post_init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '_get_headers' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/continuous-autonomous-operation.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 14 potentially unquoted variable usages

### /scripts/crisis-respond.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 9 potentially unquoted variable usages

### /scripts/daily-email-report.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 29 potentially unquoted variable usages

### /scripts/daily-podcast-clips.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 38 potentially unquoted variable usages

### /scripts/daily-podcast-email-v2.py

- High complexity function 'send_email_with_clips' (score: 17)
- High complexity function 'process_podcast' (score: 14)
- Function 'main' missing docstring
- SECURITY: os.system() - command injection risk
- SECURITY: Hardcoded password detected
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/daily-podcast-email.py

- High complexity function 'send_email_with_clips' (score: 17)
- Function 'main' missing docstring
- SECURITY: os.system() - command injection risk
- SECURITY: Hardcoded password detected
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/daily-podcast-with-skills.py

- High complexity function 'process_podcast' (score: 13)
- Function 'main' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/dashboard.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /scripts/dashboard_builder.py

- Function '__init__' missing docstring
- High complexity function '_render_component' (score: 30)
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/data_analyzer.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- High complexity function 'extract_entities' (score: 13)
- Function '__init__' missing docstring
- PERFORMANCE: Using range(len()) - use enumerate() instead
- PERFORMANCE: List building in loop - use list comprehension
- DOCUMENTATION: Missing module docstring

### /scripts/data_transform_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/database_toolkit.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/date_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/decorator_toolkit.py

- Function 'slow_function' missing docstring
- Function 'flaky_function' missing docstring
- Function 'expensive_calculation' missing docstring
- Function 'my_function' missing docstring
- Function 'wrapper' missing docstring
- Function 'decorator' missing docstring
- Function 'wrapper' missing docstring
- Function 'wrapper' missing docstring
- Function 'decorator' missing docstring
- Function 'wrapper' missing docstring
- ... and 5 more issues

### /scripts/dependency_checker.py

- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/deploy-total-control.sh

- SECURITY: Hardcoded token
- ERROR HANDLING: Missing 'set -e' or error handling options

### /scripts/deploy-video-function-manual.sh

- ERROR HANDLING: No explicit command error checking

### /scripts/docs_toolkit.py

- High complexity function 'parse_file' (score: 13)
- Function '__init__' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/email_toolkit.py

- Function '__post_init__' missing docstring
- Function '__init__' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/error_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'log_error' missing docstring
- Function 'flaky_function' missing docstring
- Function 'risky_function' missing docstring
- Function 'wrapper' missing docstring
- Function 'wrapper' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/event_toolkit.py

- Function '__init__' missing docstring
- Function '__new__' missing docstring
- Function '__init__' missing docstring
- Function 'on_message' missing docstring
- Function 'on_once' missing docstring
- Function 'handler' missing docstring
- Function 'slot1' missing docstring
- Function 'slot2' missing docstring
- PERFORMANCE: Global variable usage - consider encapsulation
- DOCUMENTATION: Missing module docstring

### /scripts/extract-video-urls.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/fetch-podcast.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/fetch_nielsen_live.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/fetch_nrj_dashboard_stats.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/fetch_nrj_dashboard_stats_v2.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/fetch_nrj_morgen_podcast.py

- Function 'main' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/fetch_podtoppen_live.py

- Function 'main' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/file_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- SECURITY: MD5 is cryptographically broken
- DOCUMENTATION: Missing module docstring

### /scripts/final-title-generator.py

- High complexity function 'generate_title' (score: 29)
- Function 'main' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/forecast-trends.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /scripts/format-title.py

- High complexity function 'format_title' (score: 20)
- DOCUMENTATION: Missing module docstring

### /scripts/functional_toolkit.py

- Function 'add' missing docstring
- Function 'fib' missing docstring
- Function 'composed' missing docstring
- Function 'curried' missing docstring
- Function 'partial_func' missing docstring
- Function 'wrapper' missing docstring
- Function 'flipped' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/generate-mission-control-pages.py

- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /scripts/generate-showprepp.py

- Function 'supabase_request' missing docstring
- Function 'generate_showprepp' missing docstring
- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/generate_and_send_showprep.py

- Function 'main' missing docstring
- SECURITY: Hardcoded password detected
- DOCUMENTATION: Missing module docstring

### /scripts/git_toolkit.py

- Function '__init__' missing docstring
- High complexity function 'status' (score: 14)
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/guaranteed-project-starter.py

- Class 'GuaranteedProjectStarter' missing docstring
- Function '__init__' missing docstring
- Function 'log' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring
- DOCUMENTATION: 1 TODO/FIXME comments found

### /scripts/health-check.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 18 potentially unquoted variable usages

### /scripts/health_check_service.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: readlines() loads entire file - consider iteration
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/http_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/image_toolkit.py

- Function '__init__' missing docstring
- High complexity function 'create_collage' (score: 13)
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/import_nielsen_spreadsheet.py

- High complexity function 'parse_csv_file' (score: 25)
- High complexity function 'parse_excel_file' (score: 26)
- Function 'main' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- SECURITY: os.system() - command injection risk
- ... and 1 more issues

### /scripts/insert-morning-news.py

- High complexity function 'main' (score: 14)
- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/insert_nrj_dashboard_data.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/insert_to_supabase.py

- Function 'main' missing docstring
- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /scripts/integrated-morning-routine.sh

- ERROR HANDLING: No explicit command error checking

### /scripts/io_toolkit.py

- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /scripts/iterator_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/live-search-api.py

- Function 'main' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- SECURITY: Hardcoded API key detected
- PERFORMANCE: List building in loop - use list comprehension
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/live-search.sh

- SECURITY: Hardcoded API key
- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /scripts/log_analyzer.py

- Function '__post_init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/log_analyzer_service.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- PERFORMANCE: readlines() loads entire file - consider iteration
- DOCUMENTATION: Missing module docstring

### /scripts/mandatory-preflight.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 13 potentially unquoted variable usages

### /scripts/math_toolkit.py

- PERFORMANCE: Using range(len()) - use enumerate() instead
- DOCUMENTATION: Missing module docstring

### /scripts/meeting-prep.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 8 potentially unquoted variable usages

### /scripts/memory-validator-cron.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 17 potentially unquoted variable usages

### /scripts/memory-validator.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 15 potentially unquoted variable usages

### /scripts/metrics_collector.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/mission-control-sync.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 24 potentially unquoted variable usages

### /scripts/ml-learning-analyzer.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 10 potentially unquoted variable usages

### /scripts/ml_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- High complexity function 'recommend_content_based' (score: 13)
- Function '__init__' missing docstring
- High complexity function 'kmeans' (score: 14)
- PERFORMANCE: Using range(len()) - use enumerate() instead
- DOCUMENTATION: Missing module docstring

### /scripts/monitor-topic.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/morning-routine-v2.1.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/morning-routine-v2.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/morning-routine.sh

- ERROR HANDLING: No explicit command error checking

### /scripts/network-manage.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 22 potentially unquoted variable usages

### /scripts/network_toolkit.py

- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/never-stop-mechanism.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 16 potentially unquoted variable usages

### /scripts/notify-user.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 46 potentially unquoted variable usages

### /scripts/openai-generate-title.py

- Function 'main' missing docstring
- SECURITY: Hardcoded API key detected
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/perfect-clip-finder.py

- Function 'main' missing docstring
- Function '__init__' missing docstring
- High complexity function 'find_perfect_clips' (score: 11)
- PERFORMANCE: List building in loop - use list comprehension
- DOCUMENTATION: Missing module docstring

### /scripts/perfect_clip_finder.py

- Function 'main' missing docstring
- Function '__init__' missing docstring
- High complexity function 'find_perfect_clips' (score: 11)
- PERFORMANCE: List building in loop - use list comprehension
- DOCUMENTATION: Missing module docstring

### /scripts/performance_monitor.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/performance_profiler.py

- Function '__new__' missing docstring
- Function 'wrapper' missing docstring
- Function '__init__' missing docstring
- Function '__enter__' missing docstring
- Function '__exit__' missing docstring
- Function '__str__' missing docstring
- Function 'slow_function' missing docstring
- Function 'fast_function' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/podcast-clipper.py

- High complexity function 'download_episode' (score: 11)
- Function 'main' missing docstring
- SECURITY: os.system() - command injection risk
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/preflight-checklist.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 13 potentially unquoted variable usages

### /scripts/process_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/quick-news-search.py

- SECURITY: Hardcoded API key detected
- DOCUMENTATION: Missing module docstring

### /scripts/radio-stats-updater-v2.py

- Function 'main' missing docstring
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/radio-stats-updater.py

- Function 'main' missing docstring
- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/regenerate-ui-2026.py

- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /scripts/regex_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/report_generator.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- PERFORMANCE: List building in loop - use list comprehension
- DOCUMENTATION: Missing module docstring
- ERROR HANDLING: Missing error handling for I/O or network operations

### /scripts/repurpose-content.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 18 potentially unquoted variable usages

### /scripts/research-topic.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 12 potentially unquoted variable usages

### /scripts/scheduler_toolkit.py

- Class 'TaskPriority' missing docstring
- Function '__init__' missing docstring
- High complexity function '_run_loop' (score: 11)
- Function 'test_task' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/scrapers/nielsen_scraper.py

- Function '__init__' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/scrapers/podtoppen_scraper.py

- Function '__init__' missing docstring
- High complexity function 'parse_stats' (score: 13)
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/security_audit_service.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/security_toolkit.py

- High complexity function 'generate' (score: 11)
- SECURITY: Use of eval() - dangerous code execution
- SECURITY: Use of exec() - dangerous code execution
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/self-dev-task-generator.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 20 potentially unquoted variable usages

### /scripts/send-daily-email.py

- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/send-daily-email.sh

- SECURITY: Command substitution with backticks - use $() instead
- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 24 potentially unquoted variable usages

### /scripts/send-mission-control-email.py

- Function 'send_email' missing docstring
- SECURITY: Hardcoded password detected
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/serialization_toolkit.py

- Class 'Person' missing docstring
- SECURITY: pickle usage - can execute arbitrary code
- DOCUMENTATION: Missing module docstring

### /scripts/session-end-handler.sh

- ERROR HANDLING: No explicit command error checking

### /scripts/show_nrj_dashboard_data.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/skill-activation.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- DOCUMENTATION: Script lacks comments

### /scripts/skill-health-check.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking

### /scripts/skill-master.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 6 potentially unquoted variable usages

### /scripts/smart-generate-title.py

- High complexity function 'smart_generate_title' (score: 23)
- Function 'main' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/smart_backup_service.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- SECURITY: MD5 is cryptographically broken
- DOCUMENTATION: Missing module docstring

### /scripts/smart_notification_service.py

- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/state_toolkit.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'value' missing docstring
- Function 'value' missing docstring
- Function '__init__' missing docstring
- Function 'on_count_change' missing docstring
- Function 'on_change' missing docstring
- Function 'counter_reducer' missing docstring
- Function 'on_state_change' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/string_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/summarize.sh

- ERROR HANDLING: Missing 'set -e' or error handling options

### /scripts/supabase-publisher.py

- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/system_analyzer.py

- Class 'CodeAnalyzer' missing docstring
- Function '__init__' missing docstring
- High complexity function 'analyze_ast' (score: 12)
- High complexity function 'generate_report' (score: 27)
- SECURITY: Use of eval() - dangerous code execution
- SECURITY: Use of exec() - dangerous code execution
- SECURITY: os.system() - command injection risk
- SECURITY: Use of input() - consider security implications
- PERFORMANCE: List building in loop - use list comprehension
- PERFORMANCE: readlines() loads entire file - consider iteration
- ... and 2 more issues

### /scripts/system_health_dashboard.py

- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/task_queue_manager.py

- Class 'TaskStatus' missing docstring
- Class 'TaskPriority' missing docstring
- Function '__post_init__' missing docstring
- Function 'to_dict' missing docstring
- Function '__init__' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/template_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/test_runner.py

- Function '__init__' missing docstring
- High complexity function 'print_report' (score: 12)
- DOCUMENTATION: Missing module docstring

### /scripts/test_skills_lib.py

- DOCUMENTATION: Missing module docstring

### /scripts/testing_toolkit.py

- Function 'passed_count' missing docstring
- Function 'failed_count' missing docstring
- Function 'total_duration_ms' missing docstring
- Function 'success_rate' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__call__' missing docstring
- Function 'call_count' missing docstring
- Function 'test_addition' missing docstring
- Function 'test_string' missing docstring
- ... and 7 more issues

### /scripts/toolkit-integration-demo.py

- DOCUMENTATION: Missing module docstring

### /scripts/trigger_nrj_dashboard_update.py

- High complexity function 'main' (score: 11)
- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/update_article_images.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/update_description_images.py

- Function 'main' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/update_nielsen_radio_stats.py

- Function 'main' missing docstring
- DOCUMENTATION: Missing module docstring

### /scripts/update_nrj_dashboard.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/update_nrj_podcast_dashboard.py

- Function 'main' missing docstring
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /scripts/url_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/uuid_toolkit.py

- SECURITY: MD5 is cryptographically broken
- DOCUMENTATION: Missing module docstring

### /scripts/validation_toolkit.py

- DOCUMENTATION: Missing module docstring

### /scripts/verify-podcast-system.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 15 potentially unquoted variable usages

### /scripts/video-to-audio-pipeline.py

- DOCUMENTATION: Missing module docstring
- DOCUMENTATION: 2 TODO/FIXME comments found

### /scripts/video_toolkit.py

- Function '__init__' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- Bare 'except:' clause found - should catch specific exceptions
- DOCUMENTATION: Missing module docstring

### /scripts/visualize-data.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 9 potentially unquoted variable usages

### /scripts/voice-transcribe.sh

- ERROR HANDLING: Missing 'set -e' or error handling options
- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 14 potentially unquoted variable usages

### /scripts/web_scraper.py

- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function '__init__' missing docstring
- Function 'get_tag' missing docstring
- Function 'get_tag' missing docstring
- Bare 'except:' clause found - should catch specific exceptions
- PERFORMANCE: read() loads entire file - consider chunked reading
- DOCUMENTATION: Missing module docstring

### /skills/code-quality-checker/check-quality.sh

- ERROR HANDLING: No explicit command error checking
- BEST PRACTICE: 116 potentially unquoted variable usages

## Recommendations

### Immediate Actions (This Week)

1. **Fix Critical Security Issues**
   - Replace eval()/exec() with safer alternatives
   - Remove hardcoded credentials
   - Enable SSL verification for all HTTP requests

2. **Add Error Handling**
   - Add try/except blocks around file I/O operations
   - Add 'set -e' to shell scripts
   - Implement proper error logging

### Short-term Improvements (Next 2 Weeks)

1. **Refactor Complex Functions**
   - Break down functions with complexity > 10
   - Extract common patterns into reusable functions

2. **Performance Optimization**
   - Replace string concatenation with join()
   - Use list comprehensions where appropriate
   - Compile regex patterns outside loops

### Long-term Improvements (Next Month)

1. **Documentation**
   - Add module docstrings to all files
   - Document all public functions and classes
   - Create README files for complex modules

2. **Code Organization**
   - Consolidate duplicate code patterns
   - Create shared utility modules
   - Implement consistent coding standards

3. **Testing**
   - Add unit tests for critical functions
   - Implement integration tests for APIs
   - Set up automated code quality checks
