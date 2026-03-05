# Auto-Generated Documentation
*Generated: 2026-02-28T05:06:54.604516*
*Total Python modules: 119*
*Total Shell scripts: 47*

## Python Modules
### agent_orchestrator.py

**Classes:**
- `ServiceStatus` (extends object)
  - Status for en tjeneste
- `AgentOrchestrator` (extends object)
  - Hoved-orkestrator for alle tjenester

**Functions:**
- `__init__(self, name: str, status: str = "unknown", last_run: Optional[str] = None) -> None`
- `__init__(self) -> None`
- `register_service(self, name: str, status: str = "unknown") -> None`
  - Registrer en tjeneste...
- `update_service(self, name: str, status: str, message: str = "") -> None`
  - Oppdater tjeneste-status...
- `check_all_services(self) -> Dict[str, Any]`
  - Sjekk alle tjenester...
- `get_dashboard(self) -> str`
  - Generer dashboard-visning...
- `auto_heal(self) -> None`
  - Automatisk reparasjon av problemer...
- `initialize_orchestrator() -> AgentOrchestrator`
  - Initialiser orkestrator med alle kjente tjenester...
- `main() -> None`
  - Hovedfunksjon...

---

### ai-generate-title.py

**Functions:**
- `generate_title_with_kimi(original_title, description="") -> None`
  - Bruk kimi for å generere en kort, konsis tittel....
- `simple_format(title, description="") -> None`
  - Enkel formatering basert på regler....
- `main() -> None`

---

### ai-research-module.py

**Classes:**
- `ResearchResult` (extends object)
  - Resultat fra AI research
- `AIResearchEngine` (extends object)
  - AI-drevet research motor

**Functions:**
- `__init__(self) -> None`
- `search(self, query: str, freshness: str = "pd") -> ResearchResult`
  - Søk etter nyheter...
- `search_multi(self, queries: List[str], freshness: str = "pd") -> List[ResearchResult]`
  - Søk i flere kilder...
- `_analyze_findings(self, findings: List[Dict]) -> str`
  - Analyser funn og gi oppsummering...
- `_calculate_confidence(self, findings: List[Dict]) -> float`
  - Beregn konfidens-score...
- `get_trending_topics(self) -> List[Dict]`
  - Hent trending topics...
- `main() -> None`
  - Test AI Research Module...

---

### api_builder.py

**Classes:**
- `Route` (extends object)
  - API Route definition
- `APIBuilder` (extends object)
  - Build simple HTTP APIs
- `APIHandler` (extends BaseHTTPRequestHandler)
- `CRUDAPI` (extends object)
  - Quick CRUD API for a resource

**Functions:**
- `__init__(self, title: str = "API", version: str = "1.0.0") -> None`
- `get(self, path: str, description: str = "") -> None`
  - Decorator for GET routes...
- `decorator(func: Callable) -> None`
- `post(self, path: str, description: str = "") -> None`
  - Decorator for POST routes...
- `decorator(func: Callable) -> None`
- `put(self, path: str, description: str = "") -> None`
  - Decorator for PUT routes...
- `decorator(func: Callable) -> None`
- `delete(self, path: str, description: str = "") -> None`
  - Decorator for DELETE routes...
- `decorator(func: Callable) -> None`
- `_match_route(self, method: str, path: str) -> Optional[Tuple[Route, Dict[str, str]]]`
  - Match request to route and extract parameters...
- ... and 26 more functions

---

### api_gateway_service.py

**Classes:**
- `APIRequest` (extends object)
  - API request data
- `APIResponse` (extends object)
  - API response data
- `RateLimiter` (extends object)
  - Simple rate limiter
- `APIGateway` (extends object)
  - API Gateway

**Functions:**
- `__init__(self, max_requests: int = 100, window_seconds: int = 60) -> None`
- `is_allowed(self, client_id: str) -> bool`
  - Sjekk om request er tillatt...
- `get_remaining(self, client_id: str) -> int`
  - Hent gjenværende requests...
- `__init__(self, cache_ttl: int = 300) -> None`
- `route(self, path: str, methods: List[str] = None) -> None`
  - Decorator for å registrere route...
- `decorator(func: Callable) -> None`
- `add_middleware(self, middleware: Callable) -> None`
  - Legg til middleware...
- `handle_request(self, request: APIRequest) -> APIResponse`
  - Håndter en request...
- `get_stats(self) -> Dict[str, Any]`
  - Hent gateway-statistikk...
- `create_sample_gateway() -> APIGateway`
  - Lag en sample gateway...
- ... and 7 more functions

---

### async_toolkit.py

**Classes:**
- `AsyncUtils` (extends object)
  - Async utilities
- `ParallelRunner` (extends object)
  - Run tasks in parallel
- `RateLimiter` (extends object)
  - Rate limiter
- `Debouncer` (extends object)
  - Debounce function calls

**Functions:**
- `sleep(seconds: float) -> None`
  - Async sleep...
- `gather(*tasks: Awaitable) -> List[Any]`
  - Gather multiple async tasks...
- `run_in_thread(func: Callable, *args, **kwargs) -> Any`
  - Run sync function in thread...
- `timeout(task: Awaitable, seconds: float) -> Any`
  - Run task with timeout...
- `create_task(coro: Awaitable) -> asyncio.Task`
  - Create background task...
- `__init__(self, max_workers: int = 4) -> None`
- `run(self, func: Callable, items: List[Any]) -> List[Any]`
  - Run function on all items in parallel...
- `shutdown(self) -> None`
  - Shutdown executor...
- `__init__(self, calls: int, period: float) -> None`
- `acquire(self) -> None`
  - Acquire rate limit slot...
- ... and 9 more functions

---

### auto_doc_generator.py

**Classes:**
- `AutoDocGenerator` (extends object)
  - Automatically generates documentation from code files

**Functions:**
- `__init__(self, workspace_path='/root/.openclaw/workspace') -> None`
- `extract_python_docstrings(self, file_path) -> None`
  - Extract docstrings and function signatures from Python files...
- `extract_shell_comments(self, file_path) -> None`
  - Extract comments from shell scripts...
- `scan_workspace(self) -> None`
  - Scan entire workspace for code files...
- `generate_markdown_docs(self, scan_results) -> None`
  - Generate markdown documentation from scan results...
- `generate_json_index(self, scan_results) -> None`
  - Generate searchable JSON index...
- `run(self) -> None`
  - Run full documentation generation...
- `main() -> None`
  - Main entry point...

---

### automation_engine.py

**Classes:**
- `TaskStatus` (extends Enum)
- `Task` (extends object)
  - Represents a single automation task
- `AutomationEngine` (extends object)
  - Central automation engine
    
    Features:
    - Task queue with priorities
    - Dependency management
    - Retry logic
    - Parallel execution
    - Progress tracking
- `WorkflowBuilder` (extends object)
  - Build complex workflows with the automation engine

**Functions:**
- `__post_init__(self) -> None`
- `to_dict(self) -> Dict`
- `__init__(self, max_workers: int = 4) -> None`
- `register_callback(self, event: str, callback: Callable) -> None`
  - Register a callback for an event...
- `_trigger_callbacks(self, event: str, data: Any) -> None`
  - Trigger all callbacks for an event...
- `add_task(self, name: str, command: str, 
                 depends_on: Optional[List[str]] = None,
                 max_retries: int = 3) -> str`
  - Add a new task to the queue
        
        Args:
            name: Task name
            command: ...
- `_can_run(self, task: Task) -> bool`
  - Check if task can run (dependencies satisfied)...
- `_execute_task(self, task: Task) -> bool`
  - Execute a single task...
- `_worker_loop(self) -> None`
  - Worker thread loop...
- `start(self) -> None`
  - Start the automation engine...
- ... and 11 more functions

---

### autonomous-task-generator.py

**Classes:**
- `AutonomousTaskGenerator` (extends object)

**Functions:**
- `__init__(self) -> None`
- `load_tasks(self) -> None`
  - Load existing task queue...
- `save_tasks(self, tasks) -> None`
  - Save task queue...
- `generate_feature_ideas(self) -> None`
  - Generate new feature ideas based on current state...
- `generate_optimization_tasks(self) -> None`
  - Generate performance optimization tasks...
- `generate_bug_fix_tasks(self) -> None`
  - Generate potential bug fix tasks...
- `select_next_task(self, tasks) -> None`
  - Intelligently select next task based on priority and dependencies...
- `create_implementation_plan(self, task) -> None`
  - Create detailed implementation plan for a task...
- `run(self) -> None`
  - Main execution loop...

---

### autonomous-watchdog.py

**Classes:**
- `AutonomousWatchdog` (extends object)

**Functions:**
- `__init__(self) -> None`
- `log(self, message) -> None`
  - Log with timestamp...
- `update_heartbeat(self) -> None`
  - Update heartbeat timestamp...
- `get_last_project_time(self) -> None`
  - Get timestamp of last project...
- `record_project_start(self, project_name) -> None`
  - Record that a new project has started...
- `check_idle_time(self) -> None`
  - Check how long I've been idle...
- `generate_new_project(self) -> None`
  - Generate and start a new project...
- `notify_user(self, project) -> None`
  - Notify user about new project...
- `start_project_implementation(self, project) -> None`
  - Start implementing the project...
- `check_system_health(self) -> None`
  - Check if all systems are healthy...
- ... and 1 more functions

---

### baarliclaw_toolkit.py

**Classes:**
- `APIClient` (extends object)
  - Generic API client with retry logic and caching
- `BraveSearchClient` (extends object)
  - Dedicated client for Brave Search API
- `SupabaseClient` (extends object)
  - Client for Supabase operations

**Functions:**
- `setup_logging(name: str, level=logging.INFO) -> logging.Logger`
  - Set up consistent logging for all scripts...
- `__init__(self, base_url: str, api_key: Optional[str] = None, 
                 timeout: int = 30, max_retries: int = 3) -> None`
- `_make_request(self, endpoint: str, method: str = 'GET', 
                      data: Optional[Dict] = None, 
                      headers: Optional[Dict] = None) -> Optional[Dict]`
  - Make HTTP request with retry logic...
- `get(self, endpoint: str, **kwargs) -> Optional[Dict]`
  - GET request...
- `post(self, endpoint: str, data: Dict, **kwargs) -> Optional[Dict]`
  - POST request...
- `__init__(self, api_key: str) -> None`
- `search_news(self, query: str, count: int = 10, 
                    freshness: str = 'pd',
                    language: str = 'nb',
                    country: str = 'no') -> List[Dict]`
  - Search for news articles
        
        Args:
            query: Search query
            count: N...
- `search_web(self, query: str, count: int = 10) -> List[Dict]`
  - Search web (not just news)...
- `__init__(self, url: str, key: str) -> None`
- `insert(self, table: str, data: Dict) -> Optional[Dict]`
  - Insert data into table...
- ... and 15 more functions

---

### bot_toolkit.py

**Classes:**
- `BotMessage` (extends object)
  - Bot message structure
- `SlackBot` (extends object)
  - Slack bot framework
- `DiscordBot` (extends object)
  - Discord bot framework
- `BotResponseBuilder` (extends object)
  - Build rich bot responses

**Functions:**
- `__post_init__(self) -> None`
- `__init__(self, token: Optional[str] = None) -> None`
- `command(self, name: str) -> None`
  - Decorator for bot commands...
- `decorator(func: Callable) -> None`
- `on(self, event: str) -> None`
  - Decorator for event handlers...
- `decorator(func: Callable) -> None`
- `parse_command(self, text: str) -> tuple`
  - Parse command from message text...
- `process_message(self, message: Dict) -> Optional[str]`
  - Process incoming message...
- `send_message(self, channel: str, text: str, 
                    attachments: Optional[List[Dict]] = None) -> bool`
  - Send message to Slack...
- `send_dm(self, user: str, text: str) -> bool`
  - Send direct message...
- ... and 22 more functions

---

### brave-news-search-parallel.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkler...
- `search_single(query, api_key, count=10, timeout=10) -> None`
  - Enkelt søk med timeout...
- `format_results(data) -> None`
  - Formater søkeresultater...
- `main() -> None`
- `priority(article) -> None`

---

### brave-news-search-v2.py

**Functions:**
- `search_category(category_name, queries, api_key) -> None`
  - Søk i en kategori med caching og retry...
- `analyze_entertainment_value(article) -> None`
  - Analyser underholdningsverdi med TextAnalyzer...
- `format_title(title) -> None`
  - Formater tittel med StringUtils...
- `create_summary(description, source) -> None`
  - Lag oppsummering...
- `collect_all_articles() -> None`
  - Samle alle artikler fra alle kategorier...
- `select_top_articles(articles, count=15) -> None`
  - Velg topp artikler med spredning...
- `main() -> None`
  - Hovedfunksjon...

---

### brave-news-search.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkler...
- `search_brave(query, api_key, count=10, freshness='pd') -> None`
  - Søk med Brave API
    
    Args:
        query: Søkeord
        api_key: Brave API nøkkel
        co...
- `format_article(result) -> None`
  - Formater en artikkel fra Brave resultat...
- `create_summary(description, source) -> None`
  - Lag 2-3 setninger med essens...
- `calculate_entertainment_score(title, description) -> None`
  - Vurder underholdningsverdi (0-100)...
- `explain_why_nrj(title, description) -> None`
  - Forklar hvorfor saken fungerer på NRJ Morgen...
- `is_relevant_source(url) -> None`
  - Sjekk om kilden er relevant for NRJ Morgen...
- `is_excluded(title, description) -> None`
  - Sjekk om saken skal ekskluderes - KUTT: sport, hard politikk, krig, harde nyheter...
- `main() -> None`

---

### build-mc-2026.py

**Functions:**
- `build_page(filename, title, active_nav, extra_scripts, content) -> None`
  - Build a single page...

---

### cache_toolkit.py

**Classes:**
- `CacheEntry` (extends object)
  - Cache entry
- `MemoryCache` (extends object)
  - In-memory cache
- `FileCache` (extends object)
  - File-based cache
- `CacheDecorator` (extends object)
  - Cache decorator utilities

**Functions:**
- `__init__(self, default_ttl: Optional[int] = None) -> None`
- `get(self, key: str) -> Optional[Any]`
  - Get value from cache...
- `set(self, key: str, value: Any, ttl: Optional[int] = None) -> None`
  - Set value in cache...
- `delete(self, key: str) -> bool`
  - Delete from cache...
- `clear(self) -> None`
  - Clear all cache...
- `keys(self) -> list`
  - Get all keys...
- `stats(self) -> Dict`
  - Get cache statistics...
- `__init__(self, cache_dir: str = "/tmp/baarliclaw_cache") -> None`
- `_get_path(self, key: str) -> str`
  - Get file path for key...
- `get(self, key: str) -> Optional[Any]`
  - Get value from file cache...
- ... and 13 more functions

---

### chart_toolkit.py

**Classes:**
- `DataPoint` (extends object)
  - Single data point
- `SVGChart` (extends object)
  - Generate SVG charts
- `ASCIIChart` (extends object)
  - Generate ASCII charts for terminal

**Functions:**
- `__init__(self, width: int = 800, height: int = 400) -> None`
- `_get_chart_area(self) -> Tuple[int, int, int, int]`
  - Get chart drawing area...
- `line_chart(self, data: List[DataPoint], 
                   title: str = "",
                   color: str = "#3b82f6") -> str`
  - Generate line chart...
- `bar_chart(self, data: List[DataPoint], 
                  title: str = "",
                  color: str = "#3b82f6") -> str`
  - Generate bar chart...
- `pie_chart(self, data: List[DataPoint], 
                  title: str = "",
                  colors: Optional[List[str]] = None) -> str`
  - Generate pie chart...
- `_format_value(self, value: float) -> str`
  - Format value for display...
- `bar(data: List[float], labels: Optional[List[str]] = None,
            width: int = 40, height: int = 10) -> str`
  - Generate ASCII bar chart...
- `sparkline(data: List[float]) -> str`
  - Generate sparkline...
- `quick_line_chart(data: List[Tuple[Any, float]], title: str = "") -> str`
  - Quick line chart...
- `quick_bar_chart(data: List[Tuple[str, float]], title: str = "") -> str`
  - Quick bar chart...
- ... and 1 more functions

---

### cicd_toolkit.py

**Classes:**
- `StepStatus` (extends Enum)
- `PipelineStep` (extends object)
  - Pipeline step
- `Pipeline` (extends object)
  - Pipeline definition
- `PipelineRunner` (extends object)
  - Run CI/CD pipelines
- `DeploymentManager` (extends object)
  - Manage deployments

**Functions:**
- `duration_ms(self) -> float`
- `success(self) -> bool`
- `failed_steps(self) -> List[PipelineStep]`
- `__init__(self) -> None`
- `on(self, event: str, callback: Callable) -> None`
  - Register callback...
- `_trigger(self, event: str, data: Any) -> None`
  - Trigger callbacks...
- `create_pipeline(self, name: str) -> Pipeline`
  - Create new pipeline...
- `add_step(self, pipeline: Pipeline, name: str, command: str,
                 allow_failure: bool = False) -> None`
  - Add step to pipeline...
- `run_pipeline(self, pipeline: Pipeline) -> bool`
  - Run a pipeline...
- `generate_report(self, pipeline: Pipeline) -> str`
  - Generate pipeline report...
- ... and 5 more functions

---

### cli_toolkit.py

**Classes:**
- `CLIBuilder` (extends object)
  - Build CLI applications
- `TerminalUI` (extends object)
  - Terminal UI utilities
- `Colors` (extends object)
  - Terminal colors

**Functions:**
- `__init__(self, name: str, description: str = "") -> None`
- `add_argument(self, *args, **kwargs) -> None`
  - Add argument...
- `add_command(self, name: str, func: Callable, help: str = "") -> None`
  - Add subcommand...
- `parse(self, args: Optional[List[str]] = None) -> None`
  - Parse arguments...
- `run(self, args: Optional[List[str]] = None) -> None`
  - Run CLI...
- `print_table(headers: List[str], rows: List[List[str]]) -> None`
  - Print ASCII table...
- `print_progress(current: int, total: int, width: int = 40) -> None`
  - Print progress bar...
- `ask(question: str, default: Optional[str] = None) -> str`
  - Ask user for input...
- `confirm(question: str, default: bool = False) -> bool`
  - Ask for confirmation...
- `select(question: str, options: List[str]) -> int`
  - Let user select from options...
- ... and 5 more functions

---

### code_metrics_analyzer.py

**Classes:**
- `CodeMetricsAnalyzer` (extends object)
  - Analyze code metrics for quality assessment

**Functions:**
- `__init__(self, workspace_path='/root/.openclaw/workspace') -> None`
- `analyze_python_file(self, file_path) -> None`
  - Analyze a Python file for metrics...
- `analyze_shell_file(self, file_path) -> None`
  - Analyze a shell script for metrics...
- `analyze_workspace(self) -> None`
  - Analyze entire workspace...
- `calculate_summary(self) -> None`
  - Calculate summary statistics...
- `generate_report(self) -> None`
  - Generate full report...
- `print_report(self, report) -> None`
  - Print formatted report...
- `save_report(self, report, output_dir='/root/.openclaw/workspace/brain/reports') -> None`
  - Save report to JSON...
- `main() -> None`
  - Main entry point...

---

### collections_toolkit.py

**Classes:**
- `ListUtils` (extends object)
  - List utilities
- `DictUtils` (extends object)
  - Dictionary utilities

**Functions:**
- `chunk(lst: List, size: int) -> List[List]`
  - Split list into chunks...
- `flatten(lst: List) -> List`
  - Flatten nested list...
- `unique(lst: List) -> List`
  - Get unique elements...
- `get_nested(d: Dict, path: str, default: Any = None) -> Any`
  - Get nested dict value...

---

### color_toolkit.py

**Classes:**
- `ColorUtils` (extends object)
  - Color utilities
- `TerminalColors` (extends object)
  - Terminal color codes

**Functions:**
- `hex_to_rgb(hex_color: str) -> Tuple[int, int, int]`
  - Convert hex to RGB...
- `rgb_to_hex(r: int, g: int, b: int) -> str`
  - Convert RGB to hex...
- `rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]`
  - Convert RGB to HSL...
- `lighten(hex_color: str, amount: float = 0.1) -> str`
  - Lighten color...
- `darken(hex_color: str, amount: float = 0.1) -> str`
  - Darken color...
- `random_color() -> str`
  - Generate random color...
- `is_valid_hex(hex_color: str) -> bool`
  - Check if valid hex color...
- `colorize(text: str, color: str) -> str`
  - Colorize text...
- `hex_to_rgb(hex_color: str) -> Tuple[int, int, int]`
  - Quick hex to RGB...
- `rgb_to_hex(r: int, g: int, b: int) -> str`
  - Quick RGB to hex...
- ... and 1 more functions

---

### config_toolkit.py

**Classes:**
- `ConfigManager` (extends object)
  - Manage configuration files
- `EnvironmentConfig` (extends object)
  - Load config from environment variables
- `ConfigValidator` (extends object)
  - Validate configuration

**Functions:**
- `__init__(self, config_dir: str = "./config") -> None`
- `load(self, name: str) -> Dict[str, Any]`
  - Load configuration file...
- `_load_file(self, filepath: str) -> Dict`
  - Load a single config file...
- `_parse_value(self, value: str) -> Any`
  - Parse config value...
- `save(self, name: str, config: Dict, format: str = "json") -> None`
  - Save configuration...
- `get(self, name: str, key: str, default: Any = None) -> Any`
  - Get config value...
- `set(self, name: str, key: str, value: Any) -> None`
  - Set config value...
- `list_configs(self) -> List[str]`
  - List available configs...
- `load(prefix: str = "") -> Dict[str, Any]`
  - Load config from env vars...
- `get(key: str, default: Any = None, 
            type_func: Optional[type] = None) -> Any`
  - Get environment variable...
- ... and 4 more functions

---

### configuration_manager.py

**Classes:**
- `ConfigManager` (extends object)
  - Konfigurasjons-håndtering

**Functions:**
- `__init__(self, config_dir: str = "/tmp/configs") -> None`
- `load_all(self) -> None`
  - Last alle konfigurasjoner...
- `get(self, name: str, key: str = None, default: Any = None) -> Any`
  - Hent konfigurasjons-verdi...
- `set(self, name: str, key: str, value: Any) -> None`
  - Sett konfigurasjons-verdi...
- `save(self, name: str, format: str = "json") -> None`
  - Lagre konfigurasjon til fil...
- `validate(self, name: str, schema: Dict[str, str]) -> List[str]`
  - Valider konfigurasjon mot skjema...
- `create_default_configs(self) -> None`
  - Opprett standard-konfigurasjoner...
- `display_configs(self) -> None`
  - Vis alle konfigurasjoner...
- `_print_config(self, config: Dict, indent: int = 0) -> None`
  - Hjelpefunksjon for å printe konfigurasjon...
- `main() -> None`
  - Hovedfunksjon...

---

### consolidated-morning-routine.py

**Functions:**
- `log(message, emoji="") -> None`
  - Logg med timestamp...
- `search_brave(query, count=5) -> None`
  - Søk med Brave API...
- `is_excluded(title, description) -> None`
  - Sjekk om saken skal ekskluderes...
- `calculate_score(title, description) -> None`
  - Vurder underholdningsverdi (0-100)...
- `generate_short_title(original_title, description) -> None`
  - Generer tittel på maks 7 ord med OpenAI...
- `fetch_image_from_url(url) -> None`
  - Prøv å hente bilde fra artikkelens meta tags...
- `get_fallback_image(source) -> None`
  - Fallback-bilder for kjente kilder...
- `supabase_request(method, path, data=None, params=None) -> None`
  - Gjør en Supabase-forespørsel...
- `step1_search_news() -> None`
  - STEG 1: Søk etter nyheter...
- `step2_generate_titles(articles) -> None`
  - STEG 2: Generer OpenAI-titler...
- ... and 5 more functions

---

### content-hub-api.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkler...
- `upload_audio(file_path, title, description, tags=None, agenda_item_id=None) -> None`
  - Last opp lydfil til content-hub...
- `create_audio_clip(file_path, title, description, source_url=None, agenda_item_id=None) -> None`
  - Opprett en ny audio-clip i content-hub...
- `link_to_agenda_item(clip_id, agenda_item_id) -> None`
  - Link en audio-clip til en sak i Supabase...
- `list_clips() -> None`
  - List alle lokale audio-clips...
- `main() -> None`

---

### content-pipeline-v3.py

**Classes:**
- `ContentItem` (extends object)
  - Representerer et innholdselement
- `AIResearchModule` (extends object)
  - AI-drevet research modul for nyheter
- `ContentApprovalWorkflow` (extends object)
  - Content approval workflow system
- `SupabasePublisher` (extends object)
  - Publiserer innhold til Supabase
- `ContentPipeline` (extends object)
  - Hoved pipeline klasse

**Functions:**
- `load_credentials() -> None`
  - Load credentials from env file...
- `__post_init__(self) -> None`
- `__init__(self) -> None`
- `search_news(self, query: str, freshness: str = "pd") -> List[Dict]`
  - Søk etter nyheter via Brave API...
- `research_all_categories(self) -> List[ContentItem]`
  - Research alle kategorier og returner funn...
- `__init__(self) -> None`
- `submit_for_approval(self, item: ContentItem) -> bool`
  - Send innhold til godkjenning...
- `auto_approve(self, item: ContentItem) -> bool`
  - Auto-godkjenn basert på regler...
- `reject(self, item: ContentItem, reason: str) -> None`
  - Avvis innhold...
- `__init__(self) -> None`
- ... and 8 more functions

---

### daily-podcast-email-v2.py

**Functions:**
- `load_processed() -> None`
  - Last liste over allerede prosesserte episoder...
- `save_processed(processed) -> None`
  - Lagre liste over prosesserte episoder...
- `fetch_rss(rss_url) -> None`
  - Hent og parse RSS-feed...
- `download_episode(audio_url, output_path) -> None`
  - Last ned episode...
- `create_clip(input_path, output_path, start, duration) -> None`
  - Lag klipp med ffmpeg...
- `create_video(input_path, output_path) -> None`
  - Konverter til videoformat (1080x1920)...
- `send_email_with_clips(recipient, clips_info, smtp_host="smtp.gmail.com", smtp_port=587, username=None, password=None) -> None`
  - Send e-post med klipp vedlegg...
- `process_podcast(podcast_key, processed, use_perfect_clip=True) -> None`
  - Prosesser en podcast med PERFECT CLIP FINDER...
- `main() -> None`

---

### daily-podcast-email.py

**Functions:**
- `load_processed() -> None`
  - Last liste over allerede prosesserte episoder...
- `save_processed(processed) -> None`
  - Lagre liste over prosesserte episoder...
- `fetch_rss(rss_url) -> None`
  - Hent og parse RSS-feed...
- `download_episode(audio_url, output_path) -> None`
  - Last ned episode...
- `create_clip(input_path, output_path, start, duration) -> None`
  - Lag klipp med ffmpeg...
- `create_video(input_path, output_path) -> None`
  - Konverter til videoformat (1080x1920)...
- `send_email_with_clips(recipient, clips_info, smtp_host="smtp.gmail.com", smtp_port=587, username=None, password=None) -> None`
  - Send e-post med klipp vedlegg...
- `process_podcast(podcast_key, processed) -> None`
  - Prosesser en podcast...
- `main() -> None`

---

### daily-podcast-with-skills.py

**Functions:**
- `load_processed() -> None`
  - Last liste over allerede prosesserte episoder...
- `save_processed(processed) -> None`
  - Lagre liste over prosesserte episoder...
- `process_podcast(podcast_key: str, processed: dict, use_perfect_clip: bool = True) -> None`
  - Prosesser en podcast med SKILLS...
- `main() -> None`

---

### dashboard_builder.py

**Classes:**
- `Component` (extends object)
  - Base dashboard component
- `DashboardBuilder` (extends object)
  - Build HTML dashboards programmatically

**Functions:**
- `__init__(self, title: str = "Dashboard") -> None`
- `_default_css(self) -> str`
  - Default dashboard CSS...
- `_default_js(self) -> str`
  - Default dashboard JavaScript...
- `header(self, title: str, subtitle: str = "") -> None`
  - Add header section...
- `metric(self, label: str, value: Any, 
               change: Optional[float] = None,
               prefix: str = "",
               suffix: str = "",
               positive_is_good: bool = True) -> None`
  - Add metric card...
- `chart(self, chart_type: str, data: List[Dict], 
              title: str = "", x_key: str = "x", y_key: str = "y") -> None`
  - Add chart (line, bar, pie)...
- `table(self, data: List[Dict], columns: Optional[List[str]] = None,
              title: str = "") -> None`
  - Add data table...
- `progress(self, label: str, value: float, max_value: float = 100) -> None`
  - Add progress bar...
- `divider(self) -> None`
  - Add horizontal divider...
- `_render_component(self, component: Component) -> str`
  - Render single component to HTML...
- ... and 4 more functions

---

### data_analyzer.py

**Classes:**
- `TrendAnalyzer` (extends object)
  - Analyze trends in data over time
- `TextAnalyzer` (extends object)
  - Analyze text data
- `DataVisualizer` (extends object)
  - Create visualizations from data

**Functions:**
- `__init__(self) -> None`
- `add_point(self, value: float, timestamp: Optional[datetime] = None) -> None`
  - Add a data point...
- `load_from_list(self, data: List[Dict]) -> None`
  - Load data from list of dicts with 'value' and 'timestamp...
- `calculate_moving_average(self, window: int = 7) -> List[float]`
  - Calculate moving average...
- `detect_trend(self) -> Dict[str, Any]`
  - Detect overall trend in data
        
        Returns:
            {
                'direction': 'u...
- `find_anomalies(self, threshold: float = 2.0) -> List[Dict]`
  - Find anomalous data points using standard deviation
        
        Args:
            threshold: Nu...
- `predict_next(self, method: str = 'linear') -> Optional[float]`
  - Predict next value
        
        Methods: linear, average...
- `get_summary(self) -> Dict[str, Any]`
  - Get summary statistics...
- `__init__(self) -> None`
- `extract_keywords(self, texts: List[str], top_n: int = 10) -> List[Tuple[str, int]]`
  - Extract most common keywords from texts...
- ... and 8 more functions

---

### data_transform_toolkit.py

**Classes:**
- `DataTransformer` (extends object)
  - Transform data between formats
- `TextTransformer` (extends object)
  - Text transformation utilities
- `DateTimeTransformer` (extends object)
  - Date/time transformation utilities

**Functions:**
- `json_to_csv(json_data: List[Dict], 
                    output_path: Optional[str] = None) -> Optional[str]`
  - Convert JSON to CSV...
- `csv_to_json(csv_content: str) -> List[Dict]`
  - Convert CSV to JSON...
- `flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict`
  - Flatten nested dictionary...
- `unflatten_dict(d: Dict, sep: str = '_') -> Dict`
  - Unflatten dictionary...
- `rename_keys(data: Dict, key_map: Dict[str, str]) -> Dict`
  - Rename dictionary keys...
- `filter_keys(data: Dict, keys: List[str]) -> Dict`
  - Filter dictionary to only include certain keys...
- `convert_types(data: Dict, type_map: Dict[str, type]) -> Dict`
  - Convert values to specific types...
- `slugify(text: str) -> str`
  - Convert text to URL-friendly slug...
- `camel_to_snake(name: str) -> str`
  - Convert CamelCase to snake_case...
- `snake_to_camel(name: str) -> str`
  - Convert snake_case to CamelCase...
- ... and 13 more functions

---

### database_toolkit.py

**Classes:**
- `QueryResult` (extends object)
  - Database query result
- `SQLiteManager` (extends object)
  - SQLite database manager
- `QueryBuilder` (extends object)
  - Build SQL queries programmatically

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self, db_path: str) -> None`
- `_ensure_dir(self) -> None`
  - Ensure database directory exists...
- `_get_connection(self) -> None`
  - Get database connection...
- `execute(self, query: str, params: Optional[Tuple] = None) -> QueryResult`
  - Execute a query...
- `create_table(self, table_name: str, columns: Dict[str, str]) -> None`
  - Create a table
        
        Args:
            table_name: Name of the table
            columns:...
- `insert(self, table_name: str, data: Dict[str, Any]) -> int`
  - Insert a row...
- `insert_many(self, table_name: str, data: List[Dict[str, Any]]) -> None`
  - Insert multiple rows...
- `select(self, table_name: str, 
               columns: Optional[List[str]] = None,
               where: Optional[str] = None,
               params: Optional[Tuple] = None,
               order_by: Optional[str] = None,
               limit: Optional[int] = None) -> QueryResult`
  - Select rows...
- `update(self, table_name: str, data: Dict[str, Any], 
               where: str, params: Tuple) -> None`
  - Update rows...
- ... and 17 more functions

---

### date_toolkit.py

**Classes:**
- `DateUtils` (extends object)
  - Date utilities
- `TimeUtils` (extends object)
  - Time utilities

**Functions:**
- `now() -> datetime`
  - Get current datetime...
- `today() -> date`
  - Get current date...
- `parse(date_string: str, fmt: str = "%Y-%m-%d") -> Optional[datetime]`
  - Parse date from string...
- `format(dt: Union[datetime, date], fmt: str = "%Y-%m-%d") -> str`
  - Format date to string...
- `add_days(dt: datetime, days: int) -> datetime`
  - Add days to date...
- `add_hours(dt: datetime, hours: int) -> datetime`
  - Add hours to datetime...
- `start_of_day(dt: datetime) -> datetime`
  - Get start of day...
- `end_of_day(dt: datetime) -> datetime`
  - Get end of day...
- `start_of_week(dt: datetime) -> datetime`
  - Get start of week (Monday)...
- `end_of_week(dt: datetime) -> datetime`
  - Get end of week (Sunday)...
- ... and 11 more functions

---

### decorator_toolkit.py

**Classes:**
- `Decorators` (extends object)
  - Collection of useful decorators

**Functions:**
- `timer(func: Callable) -> Callable`
  - Time function execution...
- `wrapper(*args, **kwargs) -> None`
- `retry(max_attempts: int = 3, delay: float = 1.0) -> None`
  - Retry function on failure...
- `decorator(func: Callable) -> Callable`
- `wrapper(*args, **kwargs) -> None`
- `log_calls(func: Callable) -> Callable`
  - Log function calls...
- `wrapper(*args, **kwargs) -> None`
- `cache_result(func: Callable) -> Callable`
  - Cache function results...
- `wrapper(*args) -> None`
- `throttle(seconds: float) -> None`
  - Throttle function calls...
- ... and 14 more functions

---

### dependency_checker.py

**Classes:**
- `DependencyChecker` (extends object)
  - Check system and Python dependencies

**Functions:**
- `__init__(self) -> None`
- `add_check(self, name: str, check_type: str, **kwargs) -> None`
  - Add a dependency check...
- `check_command(self, command: str, args: List[str] = None, 
                      version_flag: str = '--version') -> Tuple[bool, str]`
  - Check if a command is available...
- `check_python_package(self, package: str) -> Tuple[bool, str]`
  - Check if a Python package is installed...
- `check_file_exists(self, path: str) -> Tuple[bool, str]`
  - Check if a file exists...
- `check_env_var(self, var: str) -> Tuple[bool, str]`
  - Check if environment variable is set...
- `run_checks(self) -> None`
  - Run all registered checks...
- `print_report(self) -> None`
  - Print formatted report...
- `save_report(self, output_dir='/root/.openclaw/workspace/brain/reports') -> None`
  - Save report to JSON...
- `run_full_check() -> None`
  - Run full dependency check for BaarliClaw workspace...

---

### docs_toolkit.py

**Classes:**
- `FunctionDoc` (extends object)
  - Function documentation
- `ClassDoc` (extends object)
  - Class documentation
- `ModuleDoc` (extends object)
  - Module documentation
- `PythonDocParser` (extends object)
  - Parse Python files for documentation
- `MarkdownGenerator` (extends object)
  - Generate Markdown documentation
- `DocsBuilder` (extends object)
  - Build documentation for a project
- `Calculator` (extends object)
  - A simple calculator class.

**Functions:**
- `parse_file(self, filepath: str) -> Optional[ModuleDoc]`
  - Parse a Python file...
- `_get_docstring(self, node) -> str`
  - Extract docstring from node...
- `_parse_function(self, node: ast.FunctionDef) -> Optional[FunctionDoc]`
  - Parse function definition...
- `_parse_class(self, node: ast.ClassDef) -> Optional[ClassDoc]`
  - Parse class definition...
- `_get_signature(self, node: ast.FunctionDef) -> str`
  - Get function signature...
- `_get_params(self, node: ast.FunctionDef) -> List[Dict[str, str]]`
  - Extract parameter info...
- `_get_return_type(self, node: ast.FunctionDef) -> Optional[str]`
  - Get return type annotation...
- `_get_annotation(self, annotation) -> str`
  - Convert annotation to string...
- `_get_value(self, node) -> str`
  - Get value from AST node...
- `_extract_examples(self, docstring: str) -> List[str]`
  - Extract examples from docstring...
- ... and 10 more functions

---

### email_toolkit.py

**Classes:**
- `EmailMessage` (extends object)
  - Email message structure
- `EmailSender` (extends object)
  - Send emails via SMTP
- `EmailTemplate` (extends object)
  - Email templates

**Functions:**
- `__post_init__(self) -> None`
- `__init__(self, smtp_server: str = "", smtp_port: int = 587,
                 username: str = "", password: str = "") -> None`
- `send(self, message: EmailMessage) -> bool`
  - Send an email...
- `send_simple(self, to: str, subject: str, body: str) -> bool`
  - Send simple text email...
- `render(cls, template_name: str, **kwargs) -> Dict[str, str]`
  - Render a template...

---

### error_toolkit.py

**Classes:**
- `ErrorInfo` (extends object)
  - Error information
- `ErrorHandler` (extends object)
  - Central error handling
- `RetryManager` (extends object)
  - Retry logic for functions
- `SafeExecutor` (extends object)
  - Safely execute functions
- `ErrorFormatter` (extends object)
  - Format errors for display

**Functions:**
- `__init__(self) -> None`
- `register(self, handler: Callable) -> None`
  - Register error handler...
- `handle(self, exception: Exception, context: Optional[Dict] = None) -> None`
  - Handle an exception...
- `get_errors(self, limit: Optional[int] = None) -> List[ErrorInfo]`
  - Get recent errors...
- `clear(self) -> None`
  - Clear error history...
- `has_errors(self, error_type: Optional[str] = None) -> bool`
  - Check if errors exist...
- `__call__(self, func: Callable) -> Callable`
  - Decorator for retry logic...
- `wrapper(*args, **kwargs) -> None`
- `__init__(self, default_return: Any = None,
                 log_errors: bool = True) -> None`
- `execute(self, func: Callable, *args, **kwargs) -> Any`
  - Execute function safely...
- ... and 10 more functions

---

### event_toolkit.py

**Classes:**
- `Event` (extends object)
  - Event data
- `EventEmitter` (extends object)
  - Event emitter (like Node.js)
- `EventBus` (extends object)
  - Global event bus
- `Signal` (extends object)
  - Simple signal/slot pattern

**Functions:**
- `__init__(self) -> None`
- `on(self, event: str, listener: Callable) -> None`
  - Add event listener...
- `once(self, event: str, listener: Callable) -> None`
  - Add one-time listener...
- `off(self, event: str, listener: Callable) -> None`
  - Remove event listener...
- `emit(self, event: str, data: Any = None) -> None`
  - Emit event...
- `listener_count(self, event: str) -> int`
  - Get number of listeners...
- `remove_all_listeners(self, event: Optional[str] = None) -> None`
  - Remove all listeners...
- `__new__(cls) -> None`
- `subscribe(self, event: str, callback: Callable) -> None`
  - Subscribe to event...
- `publish(self, event: str, data: Any = None) -> None`
  - Publish event...
- ... and 12 more functions

---

### extract-video-urls.py

**Functions:**
- `fetch_page(url) -> None`
  - Hent HTML-innhold fra URL...
- `extract_video_urls_vg(html, base_url) -> None`
  - Ekstraher video-URLer fra VG-artikler...
- `extract_video_urls_tv2(html, base_url) -> None`
  - Ekstraher video-URLer fra TV2-artikler...
- `extract_video_urls_dagbladet(html, base_url) -> None`
  - Ekstraher video-URLer fra Dagbladet-artikler...
- `extract_video_urls_nrk(html, base_url) -> None`
  - Ekstraher video-URLer fra NRK-artikler...
- `extract_video_urls_nettavisen(html, base_url) -> None`
  - Ekstraher video-URLer fra Nettavisen-artikler...
- `extract_video_urls_generic(html, base_url) -> None`
  - Generisk ekstrahering for ukjente kilder...
- `extract_video_urls(url) -> None`
  - Hovedfunksjon - ekstraher video-URLer fra en artikkel...
- `main() -> None`

---

### fetch-podcast.py

**Functions:**
- `fetch_feed() -> None`
  - Hent og parse RSS-feed...
- `parse_episodes(root) -> None`
  - Parse episoder fra RSS...
- `main() -> None`

---

### fetch_nielsen_live.py

**Functions:**
- `fetch_nielsen_data() -> None`
  - Hent data fra Nielsen API...
- `parse_nrj_data(data) -> None`
  - Parse NRJ-data fra Nielsen respons...
- `insert_to_supabase(nrj_data) -> None`
  - Insert data til Supabase...
- `main() -> None`

---

### fetch_nrj_dashboard_stats.py

**Functions:**
- `fetch_nielsen_data() -> None`
  - Hent NRJ radio-tall fra Nielsen API...
- `fetch_podtoppen_data() -> None`
  - Hent NRJ Morgen Podkast tall fra Podtoppen...
- `create_dashboard_html(nielsen_data, podtoppen_data) -> None`
  - Lag HTML for dashboard-visning...
- `insert_to_supabase(html_content, nielsen_data, podtoppen_data) -> None`
  - Insert samlet statistikk til Supabase...
- `main() -> None`

---

### fetch_nrj_dashboard_stats_v2.py

**Functions:**
- `fetch_nielsen_nrj_data() -> None`
  - Hent NRJ radio-tall fra Nielsen API...
- `fetch_podtoppen_nrj_data() -> None`
  - Hent NRJ Morgen Podkast tall fra Podtoppen...
- `create_dashboard_content(nielsen_data, podtoppen_data) -> None`
  - Lag JSON-struktur for dashboard...
- `insert_to_supabase(dashboard_data, nielsen_data, podtoppen_data) -> None`
  - Insert til agenda_items for dashboard-visning...
- `main() -> None`

---

### fetch_nrj_morgen_podcast.py

**Functions:**
- `fetch_podtoppen_data() -> None`
  - Hent data fra Podtoppen export...
- `find_nrj_morgen_podcast(csv_data) -> None`
  - Finn spesifikt NRJ Morgen Podkast...
- `find_ranking(csv_data, podcast_name) -> None`
  - Finn rangering for podkasten...
- `insert_to_supabase(podcast_data, rank) -> None`
  - Insert NRJ Morgen Podkast data til Supabase...
- `main() -> None`

---

### fetch_podtoppen_live.py

**Functions:**
- `fetch_podtoppen_data() -> None`
  - Hent data fra Podtoppen export...
- `parse_podtoppen_csv(csv_data) -> None`
  - Parse CSV-data og finn NRJ-podkaster...
- `insert_to_supabase(podcast_data) -> None`
  - Insert data til Supabase...
- `main() -> None`

---

### file_toolkit.py

**Classes:**
- `FileManager` (extends object)
  - Advanced file management
- `FileWatcher` (extends object)
  - Watch files for changes

**Functions:**
- `__init__(self, base_path: str = ".") -> None`
- `list_files(self, pattern: str = "*", 
                   recursive: bool = False) -> List[Dict]`
  - List files with metadata...
- `find_duplicates(self) -> List[List[str]]`
  - Find duplicate files by hash...
- `_hash_file(self, filepath: str, block_size: int = 65536) -> Optional[str]`
  - Calculate MD5 hash of file...
- `organize_by_date(self, source_dir: str, dest_dir: str,
                        date_format: str = "%Y/%m") -> None`
  - Organize files by modification date...
- `organize_by_type(self, source_dir: str, dest_dir: str) -> None`
  - Organize files by type/extension...
- `clean_old_files(self, days: int = 30, 
                       pattern: str = "*",
                       dry_run: bool = True) -> List[str]`
  - Find or delete old files...
- `sync_directories(self, source: str, dest: str, 
                        delete: bool = False) -> Dict`
  - Sync two directories...
- `get_directory_size(self, path: Optional[str] = None) -> int`
  - Get total size of directory...
- `format_size(self, size_bytes: int) -> str`
  - Format bytes to human readable...
- ... and 7 more functions

---

### final-title-generator.py

**Functions:**
- `generate_title(title, description="") -> None`
  - Generate concise title from news article....
- `main() -> None`

---

### format-title.py

**Functions:**
- `format_title(original_title) -> None`
  - Formater en nyhetstittel til kort, konsis versjon.
    Mål: 5-8 ord som forklarer saken 100%...

---

### functional_toolkit.py

**Classes:**
- `Functional` (extends object)
  - Functional programming utilities

**Functions:**
- `pipe(value: T, *functions: Callable) -> Any`
  - Pipe value through functions...
- `compose(*functions: Callable) -> Callable`
  - Compose functions right to left...
- `composed(x) -> None`
- `curry(func: Callable, arity: int = None) -> Callable`
  - Curry a function...
- `curried(*args) -> None`
- `partial(func: Callable, *args, **kwargs) -> Callable`
  - Partial application...
- `partial_func(*more_args, **more_kwargs) -> None`
- `memoize(func: Callable) -> Callable`
  - Memoize function...
- `wrapper(*args) -> None`
- `map(func: Callable[[T], U], iterable: List[T]) -> List[U]`
  - Map function over list...
- ... and 13 more functions

---

### generate-mission-control-pages.py

**Functions:**
- `load_template() -> None`
  - Load the master template...
- `generate_page(template, page_config) -> None`
  - Generate a page from template and config...
- `get_page_configs() -> None`
  - Get configuration for all pages...
- `regenerate_all_pages() -> None`
  - Regenerate all HTML pages from template...
- `sync_shared_components() -> None`
  - Sync shared components across all existing pages...
- `verify_consistency() -> None`
  - Verify all pages have consistent elements...

---

### generate-showprepp.py

**Functions:**
- `supabase_request(method, path, params=None) -> None`
- `generate_showprepp() -> None`
- `main() -> None`

---

### generate_and_send_showprep.py

**Functions:**
- `fetch_articles() -> None`
  - Hent saker fra Supabase...
- `generate_showprep(articles) -> None`
  - Generer showprepp fra artikler...
- `send_email(html_content) -> None`
  - Send e-post med showprepp...
- `main() -> None`

---

### git_toolkit.py

**Classes:**
- `GitStatus` (extends object)
  - Git repository status
- `GitManager` (extends object)
  - Manage Git repositories
- `GitAutoCommit` (extends object)
  - Auto-commit changes

**Functions:**
- `__init__(self, repo_path: str = ".") -> None`
- `_run(self, args: List[str], check: bool = True) -> Tuple[bool, str]`
  - Run git command...
- `status(self) -> GitStatus`
  - Get repository status...
- `add(self, files: List[str]) -> bool`
  - Stage files...
- `commit(self, message: str) -> bool`
  - Commit staged changes...
- `push(self, remote: str = "origin", branch: Optional[str] = None) -> bool`
  - Push to remote...
- `pull(self, remote: str = "origin", branch: Optional[str] = None) -> bool`
  - Pull from remote...
- `log(self, n: int = 10) -> List[Dict]`
  - Get commit history...
- `diff(self, staged: bool = False) -> str`
  - Get diff...
- `branch_list(self) -> List[Dict]`
  - List branches...
- ... and 10 more functions

---

### guaranteed-project-starter.py

**Classes:**
- `GuaranteedProjectStarter` (extends object)

**Functions:**
- `__init__(self) -> None`
- `log(self, message) -> None`
- `get_active_projects(self) -> None`
  - Get list of active projects...
- `save_active_projects(self, projects) -> None`
  - Save active projects list...
- `get_completed_projects(self) -> None`
  - Get list of completed projects...
- `mark_project_active(self, project) -> None`
  - Mark a project as active...
- `mark_project_completed(self, project_name) -> None`
  - Mark a project as completed...
- `generate_project_idea(self) -> None`
  - Generate a concrete project idea...
- `start_project(self, project) -> None`
  - Start working on a project...
- `notify_user(self, project) -> None`
  - Notify user about new project...
- ... and 4 more functions

---

### health_check_service.py

**Classes:**
- `HealthCheckResult` (extends object)
  - Resultat av en helse-sjekk
- `HealthCheckService` (extends object)
  - Helse-sjekk tjeneste

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self) -> None`
- `register_check(self, name: str, func: callable) -> None`
  - Registrer en sjekk-funksjon...
- `run_check(self, name: str) -> HealthCheckResult`
  - Kjør en sjekk...
- `run_all_checks(self) -> List[HealthCheckResult]`
  - Kjør alle registrerte sjekker...
- `get_overall_status(self) -> str`
  - Hent overall status...
- `display_report(self) -> None`
  - Vis helse-rapport...
- `check_disk_space() -> Dict`
  - Sjekk disk-plass...
- `check_memory() -> Dict`
  - Sjekk minne...
- `check_services() -> Dict`
  - Sjekk at viktige tjenester kjører...
- ... and 2 more functions

---

### http_toolkit.py

**Classes:**
- `HTTPResponse` (extends object)
  - HTTP response
- `HTTPClient` (extends object)
  - Advanced HTTP client
- `RESTClient` (extends object)
  - REST API client

**Functions:**
- `json(self) -> Optional[Dict]`
  - Parse response as JSON...
- `__init__(self, base_url: str = "", 
                 timeout: int = 30,
                 retries: int = 3,
                 retry_delay: float = 1.0) -> None`
- `_make_request(self, method: str, url: str,
                     headers: Optional[Dict] = None,
                     data: Optional[bytes] = None) -> HTTPResponse`
  - Make HTTP request with retries...
- `get(self, url: str, 
            headers: Optional[Dict] = None,
            use_cache: bool = False) -> HTTPResponse`
  - GET request...
- `post(self, url: str,
             data: Optional[Dict] = None,
             json_data: Optional[Dict] = None,
             headers: Optional[Dict] = None) -> HTTPResponse`
  - POST request...
- `put(self, url: str,
            json_data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> HTTPResponse`
  - PUT request...
- `delete(self, url: str,
               headers: Optional[Dict] = None) -> HTTPResponse`
  - DELETE request...
- `set_auth_token(self, token: str, header: str = "Authorization") -> None`
  - Set auth token...
- `set_basic_auth(self, username: str, password: str) -> None`
  - Set basic auth...
- `clear_cache(self) -> None`
  - Clear response cache...
- ... and 9 more functions

---

### image_toolkit.py

**Classes:**
- `ImageProcessor` (extends object)
  - Handle all image operations
- `ImageGenerator` (extends object)
  - Generate images using AI services

**Functions:**
- `__init__(self) -> None`
- `load_image(self, source: str) -> Optional[Image.Image]`
  - Load image from file path or URL
        
        Args:
            source: File path or URL...
- `save_image(self, image: Image.Image, output_path: str, 
                   quality: int = 95) -> bool`
  - Save image to file...
- `resize(self, image: Image.Image, width: Optional[int] = None,
               height: Optional[int] = None, maintain_aspect: bool = True) -> Image.Image`
  - Resize image
        
        Args:
            image: PIL Image
            width: New width (optio...
- `crop(self, image: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image`
  - Crop image
        
        Args:
            image: PIL Image
            box: (left, top, right, b...
- `crop_to_aspect(self, image: Image.Image, aspect_ratio: float) -> Image.Image`
  - Crop image to specific aspect ratio (width/height)
        
        Common ratios:
        - 16/9 = ...
- `apply_filter(self, image: Image.Image, filter_type: str) -> Image.Image`
  - Apply filter to image
        
        Filters: blur, sharpen, contour, emboss, brightness, contrast...
- `create_collage(self, images: List[Image.Image], 
                      layout: str = 'grid') -> Image.Image`
  - Create collage from multiple images
        
        Layouts: grid (2x2), horizontal, vertical...
- `__init__(self, openai_key: Optional[str] = None) -> None`
- `generate_with_dalle(self, prompt: str, size: str = "1024x1024") -> Optional[str]`
  - Generate image with DALL-E
        
        Returns URL of generated image...
- ... and 3 more functions

---

### import_nielsen_spreadsheet.py

**Functions:**
- `find_downloaded_file() -> None`
  - Finn den nyeste Nielsen-filen i download-mappen...
- `parse_csv_file(filepath) -> None`
  - Parse CSV-fil fra Nielsen...
- `parse_excel_file(filepath) -> None`
  - Parse Excel-fil fra Nielsen...
- `insert_to_supabase(data) -> None`
  - Insert parsed data til Supabase...
- `main() -> None`

---

### insert-morning-news.py

**Functions:**
- `supabase_request(method, path, data=None, params=None) -> None`
  - Gjør en Supabase-forespørsel...
- `fetch_image_from_url(url) -> None`
  - Prøv å hente bilde fra artikkelens meta tags...
- `get_fallback_image(source) -> None`
  - Fallback-bilder for kjente kilder...
- `create_notes(article) -> None`
  - Lag notes-feltet på riktig format...
- `create_description_with_image(article, image_url) -> None`
  - Lag description med HTML img tag...
- `main() -> None`

---

### insert_nrj_dashboard_data.py

**Functions:**
- `fetch_nielsen_nrj() -> None`
  - Hent NRJ radio-tall fra Nielsen API...
- `fetch_podtoppen_nrj() -> None`
  - Hent NRJ Morgen Podkast tall fra Podtoppen...
- `insert_nielsen_data(data) -> None`
  - Insert Nielsen data i nielsen_weekly_metrics...
- `insert_podtoppen_data(data) -> None`
  - Insert Podtoppen data i podtoppen_weekly_data...
- `main() -> None`

---

### insert_to_supabase.py

**Functions:**
- `get_image_for_source(source) -> None`
  - Fallback-bilder for ulike kilder...
- `insert_article(article, order_index) -> None`
  - Insert en artikkel til Supabase...
- `main() -> None`

---

### io_toolkit.py

**Classes:**
- `FileIO` (extends object)
  - File I/O operations

**Functions:**
- `read_text(path: str) -> str`
  - Read text file...
- `write_text(path: str, content: str) -> None`
  - Write text file...
- `read_json(path: str) -> Any`
  - Read JSON file...
- `write_json(path: str, data: Any, indent: int = 2) -> None`
  - Write JSON file...
- `read_lines(path: str) -> List[str]`
  - Read file as lines...
- `append_line(path: str, line: str) -> None`
  - Append line to file...
- `exists(path: str) -> bool`
  - Check if file exists...
- `size(path: str) -> int`
  - Get file size...
- `read_file(path: str) -> str`
  - Quick file read...
- `write_file(path: str, content: str) -> None`
  - Quick file write...
- ... and 2 more functions

---

### iterator_toolkit.py

**Classes:**
- `IteratorUtils` (extends object)
  - Iterator utilities
- `GeneratorUtils` (extends object)
  - Generator utilities

**Functions:**
- `batch(iterable: Iterable[T], size: int) -> Iterator[List[T]]`
  - Batch iterator into chunks...
- `take(iterable: Iterable[T], n: int) -> List[T]`
  - Take first n elements...
- `skip(iterable: Iterable[T], n: int) -> Iterator[T]`
  - Skip first n elements...
- `enumerate_from(iterable: Iterable[T], start: int = 0) -> Iterator[tuple[int, T]]`
  - Enumerate from specific start...
- `cycle(iterable: Iterable[T], times: int = 1) -> Iterator[T]`
  - Cycle through iterable n times...
- `pairwise(iterable: Iterable[T]) -> Iterator[tuple[T, T]]`
  - Iterate pairwise...
- `window(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]`
  - Sliding window...
- `range_step(start: int, stop: int, step: int) -> Iterator[int]`
  - Range with custom step...
- `countdown(start: int, stop: int = 0) -> Iterator[int]`
  - Countdown generator...
- `repeat(value: T, times: int = None) -> Iterator[T]`
  - Repeat value n times (or forever if None)...
- ... and 3 more functions

---

### live-search-api.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkler fra credentials-fil...
- `search_newsapi(query, api_key, freshness_hours=1) -> None`
  - Søk med NewsAPI...
- `format_results(data, max_results=10) -> None`
  - Formater søkeresultater...
- `main() -> None`

---

### log_analyzer.py

**Classes:**
- `LogEntry` (extends object)
  - Parsed log entry
- `LogParser` (extends object)
  - Parse various log formats
- `LogAnalyzer` (extends object)
  - Analyze log entries
- `LogMonitor` (extends object)
  - Monitor logs in real-time

**Functions:**
- `__post_init__(self) -> None`
- `__init__(self, format_type: Optional[str] = None) -> None`
- `parse_line(self, line: str) -> Optional[LogEntry]`
  - Parse a single log line...
- `_parse_timestamp(self, ts_str: str) -> Optional[datetime]`
  - Parse timestamp string...
- `parse_file(self, filepath: str, max_lines: Optional[int] = None) -> List[LogEntry]`
  - Parse entire log file...
- `__init__(self, entries: List[LogEntry]) -> None`
- `level_counts(self) -> Dict[str, int]`
  - Count entries by level...
- `hourly_distribution(self) -> Dict[int, int]`
  - Get entries per hour...
- `top_messages(self, n: int = 10) -> List[Tuple[str, int]]`
  - Get most common messages...
- `search(self, pattern: str) -> List[LogEntry]`
  - Search for pattern in messages...
- ... and 13 more functions

---

### log_analyzer_service.py

**Classes:**
- `LogEntry` (extends object)
  - En logg-entry
- `LogPattern` (extends object)
  - Et oppdaget mønster
- `LogAnalyzer` (extends object)
  - Logg-analysator

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self) -> None`
- `parse_line(self, line: str, line_number: int, source: str = "unknown") -> Optional[LogEntry]`
  - Parse en logg-linje...
- `analyze_file(self, filepath: str) -> 'LogAnalyzer'`
  - Analyser en logg-fil...
- `_analyze_patterns(self) -> None`
  - Analyser mønstre i loggene...
- `get_summary(self) -> Dict[str, Any]`
  - Hent oppsummering...
- `get_errors(self, limit: int = 20) -> List[LogEntry]`
  - Hent feil-entries...
- `display_report(self) -> None`
  - Vis analyse-rapport...
- `main() -> None`
  - Hovedfunksjon...

---

### math_toolkit.py

**Classes:**
- `StatsResult` (extends object)
  - Statistics result
- `Statistics` (extends object)
  - Statistical calculations
- `MathUtils` (extends object)
  - Mathematical utilities
- `RandomUtils` (extends object)
  - Random utilities

**Functions:**
- `calculate(data: List[float]) -> StatsResult`
  - Calculate all statistics...
- `percentile(data: List[float], p: float) -> float`
  - Calculate percentile...
- `correlation(x: List[float], y: List[float]) -> float`
  - Calculate Pearson correlation coefficient...
- `moving_average(data: List[float], window: int) -> List[float]`
  - Calculate moving average...
- `normalize(data: List[float], method: str = "minmax") -> List[float]`
  - Normalize data...
- `clamp(value: float, min_val: float, max_val: float) -> float`
  - Clamp value between min and max...
- `lerp(start: float, end: float, t: float) -> float`
  - Linear interpolation...
- `map_range(value: float, 
                  from_min: float, from_max: float,
                  to_min: float, to_max: float) -> float`
  - Map value from one range to another...
- `round_to(value: float, nearest: float) -> float`
  - Round to nearest multiple...
- `is_prime(n: int) -> bool`
  - Check if number is prime...
- ... and 9 more functions

---

### metrics_collector.py

**Classes:**
- `MetricPoint` (extends object)
  - Et metrikk-punkt
- `MetricsCollector` (extends object)
  - Samler og aggregerer metrikker

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self, storage_file: str = "/tmp/metrics.json") -> None`
- `load(self) -> None`
  - Last metrikker fra fil...
- `save(self) -> None`
  - Lagre metrikker til fil...
- `record(self, name: str, value: float, tags: Dict[str, str] = None) -> None`
  - Registrer en metrikk...
- `get_metric(self, name: str, since: Optional[str] = None) -> List[MetricPoint]`
  - Hent metrikker etter navn...
- `aggregate(self, name: str, period: str = "1h") -> Dict[str, Any]`
  - Aggreger metrikker over en periode...
- `get_all_names(self) -> List[str]`
  - Hent alle metrikk-navn...
- `get_dashboard(self) -> str`
  - Generer dashboard-visning...
- `export_to_prometheus(self) -> str`
  - Eksporter til Prometheus format...
- ... and 2 more functions

---

### ml_toolkit.py

**Classes:**
- `SimpleClassifier` (extends object)
  - Simple text classifier using bag-of-words
- `RecommendationEngine` (extends object)
  - Simple recommendation engine
- `TimeSeriesForecaster` (extends object)
  - Simple time series forecasting
- `Clustering` (extends object)
  - Simple clustering algorithms
- `Similarity` (extends object)
  - Text and vector similarity functions

**Functions:**
- `__init__(self) -> None`
- `_tokenize(self, text: str) -> List[str]`
  - Simple tokenization...
- `train(self, text: str, label: str) -> None`
  - Train on a single document...
- `predict(self, text: str) -> Dict[str, float]`
  - Predict class probabilities...
- `__init__(self) -> None`
- `add_interaction(self, user_id: str, item_id: str) -> None`
  - Record user-item interaction...
- `add_item_features(self, item_id: str, features: Dict[str, Any]) -> None`
  - Add features for an item...
- `get_similar_users(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]`
  - Find users with similar taste...
- `recommend(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]`
  - Recommend items for a user...
- `recommend_content_based(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]`
  - Content-based recommendations...
- ... and 13 more functions

---

### monitor-topic.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkler...
- `check_news(topic, api_key, last_titles) -> None`
  - Sjekk etter nye nyheter...
- `main() -> None`

---

### morning-routine-v2.1.py

**Functions:**
- `search_brave(query, count=5) -> None`
  - Søk med Brave API...
- `is_excluded(title, description) -> None`
  - Sjekk om saken skal ekskluderes...
- `calculate_score(title, description) -> None`
  - Vurder underholdningsverdi (0-100)...
- `generate_short_title(original_title, description) -> None`
  - Generer tittel på maks 7 ord med OpenAI...
- `fetch_from_source(source_key, source_config) -> None`
  - Hent saker fra en kilde...
- `main() -> None`

---

### morning-routine-v2.py

**Functions:**
- `generate_short_title(original_title, description) -> None`
  - Generer tittel på maks 7 ord med OpenAI...
- `search_brave(query, count=10) -> None`
  - Søk med Brave API...
- `is_excluded(title, description) -> None`
  - Sjekk om saken skal ekskluderes...
- `calculate_score(title, description) -> None`
  - Vurder underholdningsverdi (0-100)...
- `explain_why(title, description) -> None`
  - Forklar hvorfor saken fungerer på NRJ...
- `fetch_from_source(source_key, source_config) -> None`
  - Hent saker fra en kilde...
- `main() -> None`

---

### network_toolkit.py

**Classes:**
- `PingResult` (extends object)
  - Ping test result
- `PortScanResult` (extends object)
  - Port scan result
- `NetworkTools` (extends object)
  - Network diagnostic tools
- `ServiceMonitor` (extends object)
  - Monitor services and websites

**Functions:**
- `ping(self, host: str, count: int = 4, timeout: int = 5) -> PingResult`
  - Ping a host...
- `check_port(self, host: str, port: int, timeout: int = 3) -> bool`
  - Check if a port is open...
- `scan_ports(self, host: str, 
                   ports: Optional[List[int]] = None) -> List[PortScanResult]`
  - Scan ports on a host...
- `get_ip(self, hostname: str) -> Optional[str]`
  - Resolve hostname to IP...
- `get_hostname(self, ip: str) -> Optional[str]`
  - Resolve IP to hostname...
- `check_url(self, url: str, timeout: int = 10) -> Dict`
  - Check URL availability...
- `speed_test_simple(self) -> Dict`
  - Simple speed test (download from test file)...
- `get_local_ip(self) -> str`
  - Get local IP address...
- `get_network_info(self) -> Dict`
  - Get network interface info...
- `traceroute(self, host: str, max_hops: int = 30) -> List[Dict]`
  - Simple traceroute...
- ... and 7 more functions

---

### openai-generate-title.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkkel fra credentials...
- `generate_title_with_openai(original_title, description="") -> None`
  - Bruk OpenAI GPT-4 for å generere en kort, konsis tittel....
- `main() -> None`

---

### perfect-clip-finder.py

**Classes:**
- `PerfectClipFinder` (extends object)
  - Finn perfekte klipp basert på flere parametere

**Functions:**
- `__init__(self, audio_path: str) -> None`
- `_load_audio(self) -> None`
  - Last inn lydfil...
- `analyze_audio_energy(self, start: float, end: float) -> float`
  - Analyser lydnivå og dynamikk (0-100)...
- `detect_laughter(self, start: float, end: float) -> float`
  - Detekter latter og glede (0-100)...
- `analyze_conversation_pace(self, start: float, end: float) -> float`
  - Analyser samtaletempo (0-100)...
- `analyze_emotional_intensity(self, start: float, end: float) -> float`
  - Analyser emosjonell intensitet (0-100)...
- `analyze_quote_quality(self, start: float, end: float) -> float`
  - Vurder sitat-kvalitet (relatable, morsomt, tankevekkende)...
- `_get_transcript_segment(self, start: float, end: float) -> str`
  - Hent transkripsjon for tidssegment...
- `_analyze_text_quality(self, text: str, base_score: float) -> float`
  - Analyser tekst-kvalitet...
- `calculate_viral_potential(self, start: float, end: float, 
                                   audio_score: float, laughter_score: float,
                                   emotional_score: float) -> float`
  - Beregn viral potensial (0-100)...
- ... and 6 more functions

---

### perfect_clip_finder.py

**Classes:**
- `PerfectClipFinder` (extends object)
  - Finn perfekte klipp basert på flere parametere

**Functions:**
- `__init__(self, audio_path: str) -> None`
- `_load_audio(self) -> None`
  - Last inn lydfil...
- `analyze_audio_energy(self, start: float, end: float) -> float`
  - Analyser lydnivå og dynamikk (0-100)...
- `detect_laughter(self, start: float, end: float) -> float`
  - Detekter latter og glede (0-100)...
- `analyze_conversation_pace(self, start: float, end: float) -> float`
  - Analyser samtaletempo (0-100)...
- `analyze_emotional_intensity(self, start: float, end: float) -> float`
  - Analyser emosjonell intensitet (0-100)...
- `analyze_quote_quality(self, start: float, end: float) -> float`
  - Vurder sitat-kvalitet (relatable, morsomt, tankevekkende)...
- `_get_transcript_segment(self, start: float, end: float) -> str`
  - Hent transkripsjon for tidssegment...
- `_analyze_text_quality(self, text: str, base_score: float) -> float`
  - Analyser tekst-kvalitet...
- `calculate_viral_potential(self, start: float, end: float, 
                                   audio_score: float, laughter_score: float,
                                   emotional_score: float) -> float`
  - Beregn viral potensial (0-100)...
- ... and 6 more functions

---

### performance_monitor.py

**Classes:**
- `PerformanceSnapshot` (extends object)
  - Ytelses-snapshot
- `PerformanceMonitor` (extends object)
  - Ytelses-overvåking

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self, history_file: str = "/tmp/performance_history.json") -> None`
- `load(self) -> None`
  - Last historikk...
- `save(self) -> None`
  - Lagre historikk...
- `capture(self) -> PerformanceSnapshot`
  - Ta ytelses-snapshot...
- `get_current_status(self) -> Dict[str, Any]`
  - Hent nåværende status...
- `display_dashboard(self) -> None`
  - Vis ytelses-dashboard...
- `_draw_bar(self, percent: float, width: int = 40) -> None`
  - Tegn progress bar...
- `check_alerts(self) -> List[str]`
  - Sjekk for varsler...
- `main() -> None`
  - Hovedfunksjon...

---

### performance_profiler.py

**Classes:**
- `PerformanceProfiler` (extends object)
  - Track and analyze performance metrics
- `Timer` (extends object)
  - Context manager for timing code blocks

**Functions:**
- `__new__(cls) -> None`
- `reset(cls) -> None`
  - Reset all profiling data...
- `record(cls, name, duration) -> None`
  - Record a timing measurement...
- `get_stats(cls, name=None) -> None`
  - Get profiling statistics...
- `print_report(cls) -> None`
  - Print formatted performance report...
- `save_report(cls, output_dir='/root/.openclaw/workspace/brain/reports') -> None`
  - Save report to JSON file...
- `profile(func) -> None`
  - Decorator to profile function execution time...
- `wrapper(*args, **kwargs) -> None`
- `__init__(self, name="block") -> None`
- `__enter__(self) -> None`
- ... and 4 more functions

---

### podcast-clipper.py

**Functions:**
- `fetch_rss() -> None`
  - Hent og parse RSS-feed...
- `list_episodes(limit=10) -> None`
  - List siste episoder...
- `download_episode(episode_index=0, output_dir=None, quiet=False) -> None`
  - Last ned en episode...
- `analyze_audio(filepath) -> None`
  - Analyser lydfil for å finne beste øyeblikk (placeholder)...
- `create_clip(audio_path, start, end, output_path, text=None) -> None`
  - Klipp ut en del av lydfilen...
- `create_video(audio_path, text, output_path, template="default") -> None`
  - Lag video fra audio med tekst-overlay...
- `get_latest_episode_info() -> None`
  - Hent info om siste episode...
- `main() -> None`

---

### process_toolkit.py

**Classes:**
- `ProcessUtils` (extends object)
  - Process utilities
- `SystemUtils` (extends object)
  - System utilities

**Functions:**
- `run(command: List[str], cwd: Optional[str] = None, 
            env: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None) -> Dict[str, Any]`
  - Run command and return result...
- `get_processes() -> List[Dict]`
  - Get list of running processes...
- `kill_process(pid: int, force: bool = False) -> bool`
  - Kill process by PID...
- `get_system_info() -> Dict`
  - Get system information...
- `get_env(key: str, default: Optional[str] = None) -> Optional[str]`
  - Get environment variable...
- `set_env(key: str, value: str) -> None`
  - Set environment variable...
- `get_cwd() -> str`
  - Get current working directory...
- `change_dir(path: str) -> None`
  - Change working directory...
- `exit(code: int = 0) -> None`
  - Exit program...
- `run_command(command: str) -> str`
  - Quick command execution...
- ... and 2 more functions

---

### radio-stats-updater-v2.py

**Classes:**
- `RadioStatsUpdater` (extends object)
  - Hent og oppdater radiotall for NRJ Morgen - MED EKTE DATA

**Functions:**
- `__init__(self) -> None`
- `update_podtoppen(self) -> bool`
  - Hent og oppdater Podtoppen-tall - EKTE DATA...
- `update_nielsen(self) -> bool`
  - Hent og oppdater Nielsen-tall...
- `_save_stats(self, stats_type: str, data: dict) -> bool`
  - Lagre statistikk...
- `generate_report(self) -> str`
  - Generer rapport fra lagrede data...
- `main() -> None`

---

### radio-stats-updater.py

**Classes:**
- `RadioStatsUpdater` (extends object)
  - Hent og oppdater radiotall for NRJ Morgen

**Functions:**
- `__init__(self) -> None`
- `fetch_nielsen_data(self) -> Optional[Dict]`
  - Hent radiotall fra Nielsen iPort
        
        Note: Krever autentisering. I produksjon ville det...
- `fetch_podtoppen_data(self, podcast_id: str = "3873") -> Optional[Dict]`
  - Hent podtoppen-tall for NRJ Morgen Podkast
        
        Args:
            podcast_id: Podtoppen ...
- `update_nrjmorgen_dashboard(self, stats_type: str, data: Dict) -> bool`
  - Oppdater dashboard på nrjmorgen.com
        
        Args:
            stats_type: 'nielsen' eller '...
- `_save_local(self, stats_type: str, data: Dict) -> bool`
  - Lagre data lokalt hvis Supabase ikke er tilgjengelig...
- `generate_report(self, nielsen_data: Dict, podtoppen_data: Dict) -> str`
  - Generer rapport av tallene...
- `run_nielsen_update(self) -> bool`
  - Kjør oppdatering av Nielsen-tall...
- `run_podtoppen_update(self) -> bool`
  - Kjør oppdatering av Podtoppen-tall...
- `main() -> None`

---

### regenerate-ui-2026.py

**Functions:**
- `load_template() -> None`
  - Load the 2026 template...
- `generate_page(template, page_config) -> None`
  - Generate a page from template and config...
- `get_page_configs() -> None`
  - Get configuration for all pages...
- `regenerate_all_pages() -> None`
  - Regenerate all HTML pages from template...

---

### regex_toolkit.py

**Classes:**
- `RegexUtils` (extends object)
  - Regex utilities

**Functions:**
- `is_match(pattern: str, text: str) -> bool`
  - Check if text matches pattern...
- `find_all(pattern: str, text: str) -> List[str]`
  - Find all matches...
- `find_first(pattern: str, text: str) -> Optional[str]`
  - Find first match...
- `replace(pattern: str, text: str, replacement: str) -> str`
  - Replace all matches...
- `replace_first(pattern: str, text: str, replacement: str) -> str`
  - Replace first match only...
- `split(pattern: str, text: str) -> List[str]`
  - Split by pattern...
- `extract_groups(pattern: str, text: str) -> Optional[tuple]`
  - Extract groups from match...
- `check_pattern(pattern_name: str, text: str) -> bool`
  - Check against common pattern...
- `matches(pattern: str, text: str) -> bool`
  - Quick match check...
- `extract(pattern: str, text: str) -> List[str]`
  - Quick extract...
- ... and 1 more functions

---

### report_generator.py

**Classes:**
- `ReportSection` (extends object)
  - En seksjon i en rapport
- `ReportGenerator` (extends object)
  - Rapport-generator

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self, title: str = "BaarliClaw Report") -> None`
- `add_section(self, title: str, content: str = "", data: Dict = None) -> None`
  - Legg til seksjon...
- `to_markdown(self) -> str`
  - Generer Markdown-rapport...
- `to_html(self) -> str`
  - Generer HTML-rapport...
- `to_json(self) -> str`
  - Generer JSON-rapport...
- `save(self, filepath: str, format: str = "markdown") -> None`
  - Lagre rapport til fil...
- `generate_system_report() -> ReportGenerator`
  - Generer system-rapport...
- `main() -> None`
  - Hovedfunksjon...

---

### scheduler_toolkit.py

**Classes:**
- `TaskPriority` (extends Enum)
- `ScheduledTask` (extends object)
  - Scheduled task
- `TaskScheduler` (extends object)
  - Schedule and run tasks

**Functions:**
- `__init__(self) -> None`
- `schedule(self, name: str, func: Callable,
                 scheduled_time: datetime,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 args: tuple = None,
                 kwargs: Dict = None,
                 recurring: bool = False,
                 interval_seconds: Optional[int] = None) -> str`
  - Schedule a task...
- `schedule_in(self, name: str, func: Callable,
                   seconds: int,
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   **kwargs) -> str`
  - Schedule task to run in X seconds...
- `start(self) -> None`
  - Start the scheduler...
- `stop(self) -> None`
  - Stop the scheduler...
- `_run_loop(self) -> None`
  - Main scheduler loop...
- `test_task() -> None`

---

### security_audit_service.py

**Classes:**
- `SecurityFinding` (extends object)
  - Et sikkerhets-funn
- `SecurityAuditService` (extends object)
  - Sikkerhets-audit tjeneste

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self) -> None`
- `check_file_permissions(self, filepath: str) -> List[SecurityFinding]`
  - Sjekk fil-rettigheter...
- `scan_for_secrets(self, filepath: str) -> List[SecurityFinding]`
  - Skann etter hemmeligheter i kode...
- `check_critical_files(self) -> List[SecurityFinding]`
  - Sjekk kritiske filer...
- `audit_directory(self, directory: str, max_files: int = 100) -> List[SecurityFinding]`
  - Audit en hel mappe...
- `run_full_audit(self) -> List[SecurityFinding]`
  - Kjør full audit...
- `get_summary(self) -> Dict[str, Any]`
  - Hent oppsummering...
- `display_report(self) -> None`
  - Vis audit-rapport...
- `main() -> None`
  - Hovedfunksjon...

---

### security_toolkit.py

**Classes:**
- `PasswordManager` (extends object)
  - Password generation and validation
- `TokenManager` (extends object)
  - Generate and validate tokens
- `Encryption` (extends object)
  - Simple encryption utilities
- `InputValidator` (extends object)
  - Validate and sanitize input
- `SecurityScanner` (extends object)
  - Scan for security issues

**Functions:**
- `generate(length: int = 16, 
                 include_upper: bool = True,
                 include_lower: bool = True,
                 include_digits: bool = True,
                 include_special: bool = True) -> str`
  - Generate secure password...
- `check_strength(password: str) -> Dict`
  - Check password strength...
- `hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]`
  - Hash password with salt...
- `verify_password(password: str, key: bytes, salt: bytes) -> bool`
  - Verify password against hash...
- `generate(length: int = 32) -> str`
  - Generate secure random token...
- `generate_api_key(prefix: str = "baarli") -> str`
  - Generate API key...
- `generate_otp(length: int = 6) -> str`
  - Generate one-time password...
- `xor_encrypt(data: str, key: str) -> str`
  - Simple XOR encryption (not for production!)...
- `xor_decrypt(encrypted: str, key: str) -> str`
  - Decrypt XOR encrypted data...
- `caesar_cipher(text: str, shift: int) -> str`
  - Caesar cipher (for educational purposes)...
- ... and 11 more functions

---

### send-daily-email.py

**Functions:**
- `load_credentials() -> None`
  - Last credentials fra .env fil...
- `markdown_to_showprepp_html(markdown_text) -> None`
  - Konverter markdown til mobilvennlig SHOWPREPP HTML...
- `send_showprepp_email(report_file, to_email) -> None`
  - Send SHOWPREPP e-post via Gmail...

---

### send-mission-control-email.py

**Functions:**
- `send_email() -> None`

---

### serialization_toolkit.py

**Classes:**
- `JSONSerializer` (extends object)
  - JSON serialization
- `PickleSerializer` (extends object)
  - Pickle serialization
- `Base64Serializer` (extends object)
  - Base64 encoding
- `DataConverter` (extends object)
  - Convert between data formats
- `Person` (extends object)

**Functions:**
- `encode(data: Any, indent: Optional[int] = None) -> str`
  - Encode to JSON string...
- `decode(json_str: str) -> Any`
  - Decode from JSON string...
- `save(data: Any, filepath: str, indent: int = 2) -> None`
  - Save to JSON file...
- `load(filepath: str) -> Any`
  - Load from JSON file...
- `encode(data: Any) -> bytes`
  - Encode to pickle bytes...
- `decode(pickle_bytes: bytes) -> Any`
  - Decode from pickle bytes...
- `save(data: Any, filepath: str) -> None`
  - Save to pickle file...
- `load(filepath: str) -> Any`
  - Load from pickle file...
- `encode(data: bytes) -> str`
  - Encode bytes to base64 string...
- `decode(base64_str: str) -> bytes`
  - Decode base64 string to bytes...
- ... and 10 more functions

---

### show_nrj_dashboard_data.py

**Functions:**
- `fetch_nielsen_nrj() -> None`
  - Hent NRJ radio-tall fra Nielsen API...
- `fetch_podtoppen_nrj() -> None`
  - Hent NRJ Morgen Podkast tall fra Podtoppen...
- `main() -> None`

---

### smart-generate-title.py

**Functions:**
- `smart_generate_title(original_title, description="") -> None`
  - Generer en konsis, informativ tittel basert på original og beskrivelse....
- `main() -> None`

---

### smart_backup_service.py

**Classes:**
- `BackupEntry` (extends object)
  - En backup-post
- `SmartBackupService` (extends object)
  - Smart backup-tjeneste

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self, backup_dir: str = "/tmp/backups") -> None`
- `load_manifest(self) -> None`
  - Last manifest...
- `save_manifest(self) -> None`
  - Lagre manifest...
- `calculate_checksum(self, filepath: str) -> str`
  - Beregn MD5 checksum...
- `backup_file(self, source_path: str, incremental: bool = True) -> Optional[BackupEntry]`
  - Backup en fil...
- `backup_directory(self, source_dir: str, pattern: str = "*") -> List[BackupEntry]`
  - Backup en hel mappe...
- `restore(self, source_path: str, version: Optional[int] = None,
                restore_path: Optional[str] = None) -> bool`
  - Gjenopprett fra backup...
- `list_backups(self, source_path: Optional[str] = None) -> List[BackupEntry]`
  - List alle backups...
- `cleanup_old(self, keep_versions: int = 5) -> None`
  - Slett gamle versjoner...
- ... and 3 more functions

---

### smart_notification_service.py

**Classes:**
- `Notification` (extends object)
  - En varsling
- `SmartNotificationService` (extends object)
  - Smart varslings-tjeneste

**Functions:**
- `to_dict(self) -> Dict`
- `__init__(self, storage_file: str = "/tmp/notifications.json") -> None`
- `load(self) -> None`
  - Last varslinger fra fil...
- `save(self) -> None`
  - Lagre varslinger til fil...
- `notify(self, title: str, message: str, priority: str = "normal", 
               category: str = "info", action_required: bool = False,
               action_url: Optional[str] = None) -> str`
  - Opprett ny varsling...
- `get_unread(self, min_priority: str = "low") -> List[Notification]`
  - Hent uleste varslinger...
- `mark_read(self, notification_id: str) -> None`
  - Merk varsling som lest...
- `mark_all_read(self) -> None`
  - Merk alle som lest...
- `get_summary(self) -> Dict[str, Any]`
  - Hent oppsummering...
- `cleanup_old(self, days: int = 7) -> None`
  - Slett gamle varslinger...
- ... and 3 more functions

---

### state_toolkit.py

**Classes:**
- `StateChange` (extends object)
  - State change record
- `StateManager` (extends object)
  - Manage application state
- `ObservableValue` (extends object)
  - Observable value
- `Store` (extends object)
  - Simple store (like Redux)

**Functions:**
- `__init__(self, initial_state: Optional[Dict] = None) -> None`
- `get(self, key: str, default: Any = None) -> Any`
  - Get state value...
- `set(self, key: str, value: Any) -> None`
  - Set state value...
- `update(self, updates: Dict[str, Any]) -> None`
  - Update multiple values...
- `subscribe(self, key: str, callback: Callable) -> None`
  - Subscribe to state changes...
- `unsubscribe(self, key: str, callback: Callable) -> None`
  - Unsubscribe from state changes...
- `_notify(self, key: str, old_value: Any, new_value: Any) -> None`
  - Notify listeners...
- `get_state(self) -> Dict`
  - Get full state copy...
- `set_state(self, state: Dict) -> None`
  - Set full state...
- `get_history(self) -> List[StateChange]`
  - Get change history...
- ... and 18 more functions

---

### string_toolkit.py

**Classes:**
- `StringUtils` (extends object)
  - String utilities
- `TextFormatter` (extends object)
  - Text formatting utilities

**Functions:**
- `camel_case(text: str) -> str`
  - Convert to camelCase...
- `pascal_case(text: str) -> str`
  - Convert to PascalCase...
- `snake_case(text: str) -> str`
  - Convert to snake_case...
- `kebab_case(text: str) -> str`
  - Convert to kebab-case...
- `title_case(text: str) -> str`
  - Convert to Title Case...
- `remove_accents(text: str) -> str`
  - Remove accents from characters...
- `extract_numbers(text: str) -> List[int]`
  - Extract all numbers from text...
- `extract_words(text: str, min_length: int = 2) -> List[str]`
  - Extract words from text...
- `similarity(str1: str, str2: str) -> float`
  - Calculate string similarity (0-1)...
- `levenshtein_distance(str1: str, str2: str) -> int`
  - Calculate Levenshtein distance...
- ... and 10 more functions

---

### supabase-publisher.py

**Classes:**
- `SupabasePublisher` (extends object)
  - Publiserer innhold til Supabase

**Functions:**
- `__init__(self) -> None`
- `_get_headers(self) -> Dict`
  - Get Supabase API headers...
- `publish_content(self, content_item: Dict) -> bool`
  - Publiser et innholdselement til Supabase...
- `publish_batch(self, content_items: List[Dict]) -> Dict`
  - Publiser flere innholdselementer...
- `get_existing_items(self, date: str = None) -> List[Dict]`
  - Hent eksisterende items for en dato...
- `main() -> None`
  - Test Supabase integration...

---

### system_health_dashboard.py

**Classes:**
- `SystemHealthDashboard` (extends object)
  - Real-time system health monitoring

**Functions:**
- `__init__(self) -> None`
- `check_disk_usage(self) -> None`
  - Check disk usage for workspace...
- `count_files(self) -> None`
  - Count various file types...
- `check_git_status(self) -> None`
  - Check git repository status...
- `check_cron_jobs(self) -> None`
  - Check cron job status...
- `check_skills(self) -> None`
  - Check skills directory...
- `check_memory_files(self) -> None`
  - Check memory files...
- `generate_report(self) -> None`
  - Generate comprehensive health report...
- `save_report(self, report) -> None`
  - Save report to file...
- `print_report(self, report) -> None`
  - Print formatted report...
- ... and 1 more functions

---

### task_queue_manager.py

**Classes:**
- `TaskStatus` (extends Enum)
- `TaskPriority` (extends Enum)
- `Task` (extends object)
  - En oppgave i køen
- `TaskQueueManager` (extends object)
  - Håndtering av oppgave-kø

**Functions:**
- `__post_init__(self) -> None`
- `to_dict(self) -> Dict`
- `__init__(self, storage_file: str = "/tmp/task_queue.json") -> None`
- `load(self) -> None`
  - Last oppgaver fra fil...
- `save(self) -> None`
  - Lagre oppgaver til fil...
- `add_task(self, name: str, description: str = "", 
                 priority: TaskPriority = TaskPriority.NORMAL,
                 dependencies: List[str] = None,
                 scheduled_for: Optional[str] = None) -> str`
  - Legg til ny oppgave...
- `register_handler(self, task_name: str, handler: Callable) -> None`
  - Registrer handler for oppgave-type...
- `get_ready_tasks(self) -> List[Task]`
  - Hent oppgaver som er klare til kjøring...
- `execute_task(self, task_id: str) -> bool`
  - Kjør en oppgave...
- `process_queue(self, max_tasks: int = 10) -> Dict[str, int]`
  - Behandle køen...
- ... and 4 more functions

---

### template_toolkit.py

**Classes:**
- `HTMLComponents` (extends object)
  - Reusable HTML components
- `CSSTemplates` (extends object)
  - CSS style templates
- `PageTemplates` (extends object)
  - Complete page templates

**Functions:**
- `card(title: str, content: str, footer: str = "") -> str`
  - Generate card component...
- `alert(message: str, type: str = "info") -> str`
  - Generate alert component...
- `button(text: str, onclick: str = "", style: str = "primary") -> str`
  - Generate button component...
- `badge(text: str, style: str = "default") -> str`
  - Generate badge component...
- `progress_bar(value: int, max_value: int = 100, 
                    color: str = "#3498db") -> str`
  - Generate progress bar...
- `modern_dark() -> str`
  - Modern dark theme CSS...
- `minimal_light() -> str`
  - Minimal light theme CSS...
- `landing_page(title: str, subtitle: str, 
                    cta_text: str = "Get Started") -> str`
  - Generate landing page...
- `admin_dashboard(title: str = "Dashboard") -> str`
  - Generate admin dashboard template...
- `quick_card(title: str, content: str) -> str`
  - Quick card generation...
- ... and 2 more functions

---

### testing_toolkit.py

**Classes:**
- `TestResult` (extends object)
  - Test result
- `TestSuite` (extends object)
  - Test suite results
- `TestRunner` (extends object)
  - Run tests and collect results
- `Assert` (extends object)
  - Assertion helpers
- `Mock` (extends object)
  - Simple mocking utility

**Functions:**
- `passed_count(self) -> int`
- `failed_count(self) -> int`
- `total_duration_ms(self) -> float`
- `success_rate(self) -> float`
- `__init__(self, suite_name: str = "Test Suite") -> None`
- `setup(self, func: Callable) -> None`
  - Set setup function...
- `teardown(self, func: Callable) -> None`
  - Set teardown function...
- `test(self, name: Optional[str] = None) -> None`
  - Decorator for test functions...
- `decorator(func: Callable) -> None`
- `wrapper(*args, **kwargs) -> None`
- ... and 22 more functions

---

### toolkit-integration-demo.py

**Functions:**
- `demo_validation() -> None`
  - Demo: validation_toolkit...
- `demo_string_utils() -> None`
  - Demo: string_toolkit...
- `demo_data_analysis() -> None`
  - Demo: data_analyzer...
- `demo_math_stats() -> None`
  - Demo: math_toolkit...
- `demo_collections() -> None`
  - Demo: collections_toolkit...
- `demo_date_utils() -> None`
  - Demo: date_toolkit...
- `demo_colors() -> None`
  - Demo: color_toolkit...
- `demo_uuid() -> None`
  - Demo: uuid_toolkit...
- `demo_cli() -> None`
  - Demo: cli_toolkit...
- `main() -> None`
  - Kjør alle demos...

---

### trigger_nrj_dashboard_update.py

**Functions:**
- `invoke_nielsen_scrape() -> None`
  - Trigger Nielsen scrape Supabase function...
- `invoke_podtoppen_scrape() -> None`
  - Trigger Podtoppen scrape Supabase function...
- `check_nielsen_data() -> None`
  - Sjekk siste NRJ data i nielsen_weekly_metrics...
- `check_podtoppen_data() -> None`
  - Sjekk siste NRJ Morgen data i podtoppen_weekly_data...
- `main() -> None`

---

### update_article_images.py

**Functions:**
- `get_image_from_article(url) -> None`
  - Hent bilde-URL fra artikkelens meta tags...
- `update_agenda_item(item_id, image_url, created_by) -> None`
  - Oppdater agenda item med bilde og created_by...
- `main() -> None`

---

### update_description_images.py

**Functions:**
- `get_image_from_metadata(link_metadata) -> None`
  - Hent bilde fra link_metadata...
- `update_description(item_id, image_url, title) -> None`
  - Oppdater description med bilde...
- `main() -> None`

---

### update_nielsen_radio_stats.py

**Functions:**
- `insert_to_supabase(data) -> None`
  - Insert radiotall til Supabase...
- `save_locally(data) -> None`
  - Lagre data lokalt...
- `main() -> None`

---

### update_nrj_dashboard.py

**Functions:**
- `fetch_nielsen_data() -> None`
  - Hent NRJ radio-tall fra Nielsen API...
- `fetch_podtoppen_data() -> None`
  - Hent NRJ Morgen Podkast tall fra Podtoppen...
- `find_existing_stats_item() -> None`
  - Finn eksisterende NRJ Statistikk item...
- `create_dashboard_html(nielsen_data, podtoppen_data) -> None`
  - Lag HTML for dashboard-visning...
- `update_supabase(item_id, html_content, nielsen_data, podtoppen_data) -> None`
  - Oppdater eksisterende item i Supabase...
- `main() -> None`

---

### update_nrj_podcast_dashboard.py

**Functions:**
- `fetch_podtoppen_data() -> None`
  - Hent data fra Podtoppen export...
- `find_nrj_morgen_podcast(csv_data) -> None`
  - Finn NRJ Morgen Podkast i dataene...
- `insert_to_podtoppen_table(podcast_data) -> None`
  - Insert data til podtoppen_weekly_data tabellen...
- `main() -> None`

---

### url_toolkit.py

**Classes:**
- `URLUtils` (extends object)
  - URL utilities

**Functions:**
- `parse(url: str) -> Dict`
  - Parse URL into components...
- `build_query(params: Dict) -> str`
  - Build query string from dict...
- `parse_query(query: str) -> Dict[str, List[str]]`
  - Parse query string to dict...
- `join(base: str, url: str) -> str`
  - Join base URL with relative URL...
- `encode(text: str) -> str`
  - URL encode text...
- `decode(text: str) -> str`
  - URL decode text...
- `is_absolute(url: str) -> bool`
  - Check if URL is absolute...
- `get_domain(url: str) -> str`
  - Extract domain from URL...
- `add_params(url: str, params: Dict) -> str`
  - Add query parameters to URL...
- `parse_url(url: str) -> Dict`
  - Quick URL parse...
- ... and 2 more functions

---

### uuid_toolkit.py

**Classes:**
- `UUIDUtils` (extends object)
  - UUID utilities
- `IDGenerator` (extends object)
  - Various ID generators

**Functions:**
- `generate_v4() -> str`
  - Generate UUID v4 (random)...
- `generate_v1() -> str`
  - Generate UUID v1 (timestamp-based)...
- `generate_short() -> str`
  - Generate short UUID (8 chars)...
- `from_string(text: str, namespace: Optional[uuid.UUID] = None) -> str`
  - Generate UUID from string (v5)...
- `from_name(name: str) -> str`
  - Generate deterministic UUID from name...
- `is_valid(uuid_str: str) -> bool`
  - Check if string is valid UUID...
- `normalize(uuid_str: str) -> str`
  - Normalize UUID string...
- `to_int(uuid_str: str) -> int`
  - Convert UUID to integer...
- `to_bytes(uuid_str: str) -> bytes`
  - Convert UUID to bytes...
- `nanoid(size: int = 21) -> str`
  - Generate nanoID-like string...
- ... and 5 more functions

---

### validation_toolkit.py

**Classes:**
- `ValidationResult` (extends object)
  - Validation result
- `Validator` (extends object)
  - Data validator
- `DataCleaner` (extends object)
  - Clean and normalize data

**Functions:**
- `email(value: str) -> ValidationResult`
  - Validate email address...
- `url(value: str, require_https: bool = False) -> ValidationResult`
  - Validate URL...
- `phone(value: str, country: str = "NO") -> ValidationResult`
  - Validate phone number...
- `number(value: Any, min_val: Optional[float] = None, 
               max_val: Optional[float] = None) -> ValidationResult`
  - Validate number...
- `text(value: str, min_length: int = 0, 
             max_length: Optional[int] = None,
             allow_empty: bool = False) -> ValidationResult`
  - Validate text...
- `date(value: str, format: str = "%Y-%m-%d") -> ValidationResult`
  - Validate date...
- `normalize_whitespace(text: str) -> str`
  - Normalize whitespace...
- `remove_special_chars(text: str, keep: str = "") -> str`
  - Remove special characters...
- `normalize_phone(phone: str) -> str`
  - Normalize phone number...
- `slugify(text: str) -> str`
  - Convert to URL-friendly slug...
- ... and 4 more functions

---

### video-to-audio-pipeline.py

**Functions:**
- `load_credentials() -> None`
  - Last API-nøkler fra credentials-fil...
- `download_video(url, output_path) -> None`
  - Last ned video med yt-dlp...
- `extract_audio(video_path, audio_path) -> None`
  - Ekstraher lyd fra video med ffmpeg...
- `transcribe_audio(audio_path) -> None`
  - Transkriber lyd med whisper...
- `find_best_quotes(transcript, num_quotes=3) -> None`
  - Finn beste sitater fra transkripsjon...
- `clip_audio(audio_path, output_path, start_time, end_time) -> None`
  - Klipp ut del av lydfil...
- `upload_to_content_hub(file_path, title, description, agenda_item_id=None) -> None`
  - Last opp til content-hub (foreløpig: lagre lokalt og logg)...
- `process_video(url, article_title, article_source, agenda_item_id=None) -> None`
  - Prosesser én video gjennom hele pipelinen...
- `main() -> None`
  - Hovedfunksjon - kan kalles med URL eller prosesser dagens saker...

---

### video_toolkit.py

**Classes:**
- `VideoInfo` (extends object)
  - Video metadata
- `VideoProcessor` (extends object)
  - Handle video operations with ffmpeg

**Functions:**
- `__init__(self) -> None`
- `_find_ffmpeg(self) -> Optional[str]`
  - Find ffmpeg binary...
- `_run_ffmpeg(self, args: List[str], timeout: int = 300) -> Tuple[bool, str]`
  - Run ffmpeg command...
- `get_info(self, video_path: str) -> Optional[VideoInfo]`
  - Get video metadata using ffprobe...
- `trim(self, input_path: str, output_path: str, 
             start: float, duration: float) -> bool`
  - Trim video segment
        
        Args:
            input_path: Source video
            output_pa...
- `resize(self, input_path: str, output_path: str,
               width: Optional[int] = None, height: Optional[int] = None,
               maintain_aspect: bool = True) -> bool`
  - Resize video
        
        Args:
            input_path: Source video
            output_path: Ou...
- `extract_audio(self, input_path: str, output_path: str,
                      format: str = 'mp3', bitrate: str = '192k') -> bool`
  - Extract audio from video...
- `create_thumbnail(self, input_path: str, output_path: str,
                        time: float = 0) -> bool`
  - Extract thumbnail at specific time...
- `concatenate(self, input_paths: List[str], output_path: str) -> bool`
  - Concatenate multiple videos...
- `add_text_overlay(self, input_path: str, output_path: str,
                        text: str, x: int = 10, y: int = 10,
                        font_size: int = 24, color: str = 'white') -> bool`
  - Add text overlay to video...
- ... and 5 more functions

---

### web_scraper.py

**Classes:**
- `SimpleScraper` (extends object)
  - Simple scraper using only standard library
- `FeedReader` (extends object)
  - Read RSS/Atom feeds
- `SitemapParser` (extends object)
  - Parse XML sitemaps

**Functions:**
- `__init__(self, delay: float = 1.0) -> None`
- `_rate_limit(self) -> None`
  - Respect rate limits...
- `fetch(self, url: str, headers: Optional[Dict] = None) -> Optional[str]`
  - Fetch HTML from URL
        
        Args:
            url: Target URL
            headers: Optional...
- `_parse_cookies(self, cookie_header: str, domain: str) -> None`
  - Parse and store cookies...
- `extract_links(self, html: str, base_url: str) -> List[Dict]`
  - Extract all links from HTML...
- `extract_emails(self, html: str) -> List[str]`
  - Extract email addresses from HTML...
- `extract_phones(self, html: str) -> List[str]`
  - Extract phone numbers from HTML...
- `extract_meta(self, html: str) -> Dict[str, str]`
  - Extract meta tags from HTML...
- `extract_article(self, html: str) -> Dict[str, Any]`
  - Extract article content from HTML
        Simple version - looks for common patterns...
- `__init__(self) -> None`
- ... and 10 more functions

---

## Shell Scripts
### agent-dashboard.sh
Agent Performance Dashboard
Shows metrics about my learning and performance...

---

### agent-wrapper.sh
AGENT WRAPPER - Forces pre-flight before any work
This script wraps the agent and ensures mandatory procedures...

---

### auto-exec-enforcer-cron.sh
AUTO-EXEC ENFORCER - CRON VERSION
Non-interactive version for scheduled execution...

**Functions:**
- `log()`
- `run_with_verification()`
  - Function to run script with verification (non-interactive)

---

### auto-exec-enforcer.sh
AUTO-EXEC ENFORCER - Forces execution of mandatory scripts
This runs automatically and cannot be skipped...

**Functions:**
- `run_with_verification()`
  - Function to run script with verification

---

### auto-learning-capture.sh
Auto-learning capture script
Run at end of every session to ensure documentation...

---

### auto-skill-selector.sh
Velger automatisk riktig skills basert på kontekst...

---

### auto-sync-mission-control.sh
AUTO-SYNC TRIGGER - Runs automatically after every change
This ensures Mission Control is ALWAYS consistent...

**Functions:**
- `log()`

---

### auto-update-all-knowledge.sh
AUTO-UPDATE ALL KNOWLEDGE
Updates ALL files, prompts, scripts and documentation with new information...

**Functions:**
- `log()`

---

### autonomous-mission-control.sh
Autonomous Mission Control Development Script
Runs continuously to improve Mission Control without human oversight...

**Functions:**
- `log()`
  - Logging function
- `notify_start()`
  - Notify user of new task
- `is_maintenance_window()`
  - Check if it's maintenance window (02:00-04:00 CET)
- `check_health()`
  - Check system health
- `find_improvements()`
  - Find improvement opportunities

---

### autonomous-mode.sh
AUTONOMOUS MODE - Self-running agent system
This script enables fully autonomous operation...

---

### brainstorm-ideas.sh
/root/.openclaw/workspace/scripts/brainstorm-ideas.sh
Generere kreative ideer...

---

### build-mission-control-2026.sh
BUILD MISSION CONTROL 2026 - Complete with all functionality
This script builds all pages with the new 2026 design AND all existing features...

**Functions:**
- `build_page()`
  - Function to build a page

---

### calendar-today.sh
/root/.openclaw/workspace/scripts/calendar-today.sh
Vis dagens agenda...

---

### continuous-autonomous-operation.sh
Continuous Autonomous Operation - Ensures 24/7 autonomous operation
This script runs continuously and ensures I never stop working...

**Functions:**
- `log()`
  - Logging function
- `ensure_continuous_operation()`
  - Ensure I'm always running
- `self_heal()`
  - Self-healing mechanism
- `generate_project_if_idle()`
  - Generate new project if idle
- `main()`
  - Never-ending loop

---

### crisis-respond.sh
/root/.openclaw/workspace/scripts/crisis-respond.sh
Håndtere kriser...

---

### daily-email-report.sh
/root/.openclaw/workspace/scripts/daily-email-report.sh
Genererer daglig SHOWPREPP-rapport for NRJ Morgen
Konfigurasjon...

---

### daily-podcast-clips.sh
Daglig posting av podkast-klipp - Faktisk implementasjon
For "Baarli og Benjamin går i terapi"...

**Functions:**
- `log()`
  - Funksjon for logging

---

### dashboard.sh
/root/.openclaw/workspace/scripts/dashboard.sh
Farger...

---

### deploy-total-control.sh
Deploy Total Control Dashboard to Netlify...

---

### deploy-video-function-manual.sh
deploy-video-function.sh - Deploy Supabase Edge Function via API...

---

### forecast-trends.sh
/root/.openclaw/workspace/scripts/forecast-trends.sh
Forutsi kommende trender...

---

### health-check.sh
/root/.openclaw/workspace/scripts/health-check.sh...

---

### integrated-morning-routine.sh
/root/.openclaw/workspace/scripts/integrated-morning-routine.sh
INTEGRERT MORGENRUTINE v2.1 - 15 saker med god spredning
Sist oppdatert: 2026-02-24
- 15 saker per dag (økt fra 10)
- 5 kategorier med m...

---

### live-search.sh
/root/.openclaw/workspace/scripts/live-search.sh
Sanntidssøk etter ferske nyheter...

---

### mandatory-preflight.sh
Mandatory Pre-Flight Enforcer
This script MUST run before any work begins
It blocks execution until checklist is complete...

---

### meeting-prep.sh
/root/.openclaw/workspace/scripts/meeting-prep.sh
Forberede møter...

---

### memory-validator-cron.sh
MEMORY VALIDATOR - Non-interactive version for cron
Validates memory without requiring user input...

**Functions:**
- `log()`

---

### memory-validator.sh
MEMORY VALIDATOR - Ensures I actually read MEMORY.md
This quizzes me on the content to verify understanding...

---

### mission-control-sync.sh
MISSION CONTROL SYNC - Ensures all HTML files are consistent
This script MUST be run after EVERY change to ensure consistency...

**Functions:**
- `log()`
- `sync_file()`
  - 2. Function to sync a single file

---

### ml-learning-analyzer.sh
ML-Based Learning Analyzer
Analyzes session logs to identify patterns and suggest improvements...

---

### morning-routine.sh
/root/.openclaw/workspace/scripts/integrated-morning-routine.sh
INTEGRERT MORGENRUTINE v2.1 - 15 saker med god spredning
Sist oppdatert: 2026-02-24
- 15 saker per dag (økt fra 10)
- 5 kategorier med m...

---

### network-manage.sh
/root/.openclaw/workspace/scripts/network-manage.sh
Håndtere kontakter og nettverk...

---

### never-stop-mechanism.sh
NEVER STOP MECHANISM
This script ensures I NEVER stop working - it restarts me if I stop...

**Functions:**
- `log()`
- `check_if_working()`
  - Function to check if I'm working
- `restart_work()`
  - Function to restart work
- `ensure_scripts_running()`
  - Function to ensure all scripts are running
- `main()`
  - Main loop

---

### notify-user.sh
User Notification System for Autonomous Tasks
Sends notification when starting new tasks...

**Functions:**
- `notify_user()`
  - Function to send notification
- `notify_completion()`
  - Function to notify task completion
- `notify_issue()`
  - Function to notify about issues

---

### preflight-checklist.sh
Pre-flight checklist - Run at the START of every session/task
Ensures I have all context and knowledge before starting work...

---

### repurpose-content.sh
/root/.openclaw/workspace/scripts/repurpose-content.sh
Gjenbruke innhold på tvers av plattformer...

---

### research-topic.sh
/root/.openclaw/workspace/scripts/research-topic.sh
Dyp research om et tema...

---

### self-dev-task-generator.sh
Autonomous Self-Development Task Generator
Kjører autonomt og genererer utviklingsoppgaver...

**Functions:**
- `analyze_workspace()`
  - Funksjon: Analyser workspace for forbedringsmuligheter
- `generate_daily_task()`
  - Funksjon: Generer dagens utviklingsoppgave
- `create_daily_log()`
  - Funksjon: Opprett dagens logg

---

### send-daily-email.sh
/root/.openclaw/workspace/scripts/send-daily-email.sh
Sender daglig rapport via Gmail
Last credentials...

---

### session-end-handler.sh
SESSION END HANDLER - Automatically runs at session end
This ensures learning capture happens even if I forget...

---

### skill-activation.sh
Aktiverer alle relevante skills for en oppgave...

---

### skill-health-check.sh
Sjekker at alle skills er klare til bruk...

---

### skill-master.sh
/root/.openclaw/workspace/scripts/skill-master.sh
Master control for alle skills...

---

### summarize.sh
summarize.sh - Lokal summarize funksjon
Bruker kimi_fetch + OpenAI/Anthropic API...

---

### verify-podcast-system.sh
Verifiser at podcast-klippe-systemet fungerer
Bruk: bash verify-podcast-system.sh...

---

### visualize-data.sh
/root/.openclaw/workspace/scripts/visualize-data.sh
Lage enkle visualiseringer...

**Functions:**
- `ascii_bar()`
  - ASCII Bar Chart

---

### voice-transcribe.sh
/root/.openclaw/workspace/scripts/voice-transcribe.sh
Transkriber talememoer til tekst...

---

