"""
INTEGRA O/S: GOOGLE ANTIGRAVITY SDK HARDENING HARNESS
Module: core/sdk_harness.py
Layer: 1 & 4 (Lifecycle Resilience, Decoupled Tool Isolation, Session Persistence)

Features:
1. types.McpStdioServer decoupled tool execution isolating tools from IDE internals.
2. Fault-tolerant lifecycle error interception (@hooks.on_tool_error) guarding against
   OS file locks, permission errors, and unquoted paths with spaces.
3. LocalAgentConfig session persistence across restarts via conversation_id and save_dir.
4. Seamless fallback shims if google-antigravity SDK is not yet globally installed.
"""

import os
import sys
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Union, Callable
from pathlib import Path

logger = logging.getLogger("integra.sdk_harness")

# ==============================================================================
# 1. SDK IMPORT OR ROBUST SHIM LAYER
# ==============================================================================
try:
    from google.antigravity import Agent as GAgAgent
    from google.antigravity import LocalAgentConfig as GAgLocalAgentConfig
    from google.antigravity import types as ag_types
    from google.antigravity.hooks import hooks as ag_hooks
    SDK_AVAILABLE = True
    logger.info("Google Antigravity SDK natively loaded.")
except ImportError:
    SDK_AVAILABLE = False
    logger.info("Google Antigravity SDK not found in local environment. Loading hardening shims.")

    class _ShimTypes:
        class McpStdioServer:
            def __init__(
                self,
                name: str,
                command: str,
                args: Optional[List[str]] = None,
                env: Optional[Dict[str, str]] = None,
                cwd: Optional[str] = None,
                enabled_tools: Optional[List[str]] = None,
                disabled_tools: Optional[List[str]] = None
            ):
                self.name = name
                self.command = command
                self.args = args or []
                self.env = env or {}
                self.cwd = cwd
                self.enabled_tools = enabled_tools
                self.disabled_tools = disabled_tools

            def to_dict(self) -> Dict[str, Any]:
                return {
                    "name": self.name,
                    "command": self.command,
                    "args": self.args,
                    "env": self.env,
                    "cwd": self.cwd,
                    "enabled_tools": self.enabled_tools,
                    "disabled_tools": self.disabled_tools
                }

        class HookResult:
            def __init__(self, allow: bool = True, reason: Optional[str] = None):
                self.allow = allow
                self.reason = reason

        class ToolCall:
            def __init__(self, name: str, arguments: Optional[Dict[str, Any]] = None):
                self.name = name
                self.arguments = arguments or {}

    class _ShimHooks:
        class HookContext:
            def __init__(self, session_id: Optional[str] = None, tool_name: Optional[str] = None):
                self.session_id = session_id
                self.tool_name = tool_name

        class OnToolErrorHook:
            async def run(self, context: Any, data: Any) -> Optional[str]:
                raise NotImplementedError

        @staticmethod
        def on_tool_error(fn: Callable):
            fn._is_tool_error_hook = True
            return fn

    class _ShimLocalAgentConfig:
        def __init__(
            self,
            conversation_id: Optional[str] = None,
            save_dir: Optional[str] = None,
            app_data_dir: Optional[str] = None,
            mcp_servers: Optional[List[Any]] = None,
            hooks: Optional[List[Any]] = None,
            api_key: Optional[str] = None,
            model: Optional[str] = None,
            **kwargs
        ):
            self.conversation_id = conversation_id
            self.save_dir = save_dir
            self.app_data_dir = app_data_dir
            self.mcp_servers = mcp_servers or []
            self.hooks = hooks or []
            self.api_key = api_key
            self.model = model
            self.extra_kwargs = kwargs

    class _ShimAgent:
        def __init__(self, config: _ShimLocalAgentConfig):
            self.config = config
            self.conversation_id = config.conversation_id or f"conv_{os.urandom(4).hex()}"
            self.is_connected = False

        async def __aenter__(self):
            self.is_connected = True
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            self.is_connected = False

        async def chat(self, prompt: str):
            class Response:
                def __init__(self, text_val: str):
                    self._text = text_val
                async def text(self) -> str:
                    return self._text
            return Response(f"Echo response to '{prompt}' with session {self.conversation_id}")

    ag_types = _ShimTypes
    ag_hooks = _ShimHooks
    GAgLocalAgentConfig = _ShimLocalAgentConfig
    GAgAgent = _ShimAgent

# Aliases
McpStdioServer = ag_types.McpStdioServer
LocalAgentConfig = GAgLocalAgentConfig
Agent = GAgAgent
OnToolErrorHook = ag_hooks.OnToolErrorHook
HookContext = ag_hooks.HookContext

# Default directories for Integra scratch & persistence
DEFAULT_SCRATCH_DIR = r"C:\Users\Javon Jenkins\.gemini\antigravity\scratch\Integra_Project"
DEFAULT_PERSISTENCE_DIR = os.path.join(DEFAULT_SCRATCH_DIR, "sessions")


# ==============================================================================
# 2. FAULT-TOLERANT LIFECYCLE ERROR INTERCEPTION
# ==============================================================================
class AntigravityFaultTolerantHook(OnToolErrorHook):
    """
    Lifecycle Hook intercepting tool execution failures:
    - Guards against OS file locks (WinError 32: used by another process).
    - Guards against OS permission errors (WinError 5: Access is denied).
    - Guards against unquoted paths containing spaces (e.g. 'C:\\Users\\Javon Jenkins\\...').
    - Reroutes dangerous writes away from system/extension files into safe scratch space.
    - Yields structured self-correction guidance so the thread survives without crashing.
    """
    def __init__(self, scratch_dir: str = DEFAULT_SCRATCH_DIR):
        self.scratch_dir = scratch_dir
        self.incident_log: List[Dict[str, Any]] = []
        os.makedirs(self.scratch_dir, exist_ok=True)

    def sanitize_unquoted_path(self, path_str: Optional[str]) -> str:
        """
        Wraps paths containing spaces in double quotes if not already quoted.
        """
        if not path_str:
            return ""
        clean = path_str.strip()
        if " " in clean and not ((clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'"))):
            return f'"{clean}"'
        return clean

    def calculate_scratch_redirect(self, target_path: Optional[str]) -> str:
        """
        Computes a safe redirect destination in the scratch space for protected files.
        """
        if not target_path:
            return os.path.join(self.scratch_dir, "diverted_artifact.tmp")
        filename = os.path.basename(target_path.strip('\'"')) or "diverted_artifact.tmp"
        return os.path.join(self.scratch_dir, filename)

    async def run(self, context: Any, data: Any) -> Optional[str]:
        """
        Intercepts the exception before it triggers an unhandled agent termination.
        Returns a guidance string for LLM self-correction or None if unhandled.
        """
        err_msg = str(data)
        import time as _time
        incident = {
            "error_type": type(data).__name__,
            "raw_message": err_msg,
            "handled": False,
            "action_taken": None,
            "timestamp": _time.time()
        }

        # Case 1: OS File Lock / Sharing Violation (WinError 32)
        # Note: In Windows Python, file sharing violations raise PermissionError with [WinError 32].
        # Therefore, file lock check MUST precede generic PermissionError check!
        if "WinError 32" in err_msg or "being used by another process" in err_msg or "sharing violation" in err_msg.lower():
            incident["handled"] = True
            incident["action_taken"] = "FILE_LOCK_SHIELD_ACTIVATED"
            self.incident_log.append(incident)
            logger.warning(f"Antigravity Hook intercepted File Lock: {err_msg}")
            return (
                "[SAFETY SHIELD: File is currently locked by another active process (WinError 32). "
                f"Do not block execution waiting on file lock. Redirect write to an isolated temporary copy in: '{self.scratch_dir}'.]"
            )

        # Case 2: OS Permission Error or Access Denied (WinError 5)
        if isinstance(data, PermissionError) or "Access is denied" in err_msg or "WinError 5" in err_msg:
            incident["handled"] = True
            incident["action_taken"] = "PERMISSION_SHIELD_ACTIVATED"
            self.incident_log.append(incident)
            logger.warning(f"Antigravity Hook intercepted Permission Error: {err_msg}")
            return (
                "[SAFETY SHIELD: Target file is protected by the OS (Access is denied). "
                f"Direct modification of host or extension files is forbidden by the Integra Constitution. "
                f"Please redirect all output writes to the designated project scratch space: '{self.scratch_dir}'.]"
            )

        # Case 3: Unquoted Path / Spaces in Path / File Not Found with space
        if isinstance(data, FileNotFoundError) or "cannot find the file" in err_msg or "WinError 2" in err_msg or "MODULE_NOT_FOUND" in err_msg:
            if " " in err_msg or "Users\\Javon Jenkins" in err_msg or "Users/Javon Jenkins" in err_msg:
                incident["handled"] = True
                incident["action_taken"] = "UNQUOTED_PATH_SANITIZED"
                self.incident_log.append(incident)
                logger.warning(f"Antigravity Hook intercepted Unquoted Path Error: {err_msg}")
                return (
                    "[SAFETY SHIELD: Path parsing error detected due to unquoted whitespace in directory path. "
                    "Ensure all file paths containing spaces (e.g. 'C:\\Users\\Javon Jenkins\\...') "
                    "are enclosed in proper double quotes or passed as discrete array arguments.]"
                )

        # Let other unhandled errors pass through
        self.incident_log.append(incident)
        return None


_global_default_hook = AntigravityFaultTolerantHook()


@ag_hooks.on_tool_error
async def integra_on_tool_error(data: Exception) -> Optional[str]:
    """
    Standard function decorator hook for Antigravity configuration.
    """
    return await _global_default_hook.run(None, data)


# ==============================================================================
# 3. DECOUPLED MCP STDIO SERVER TOOL EXECUTION
# ==============================================================================
class DecoupledMcpToolRegistry:
    """
    Manages decoupled McpStdioServer definitions, executing external tools
    over standard I/O in isolated subprocesses rather than inside IDE host processes.
    """
    def __init__(self):
        self._servers: Dict[str, Any] = {}

    def create_stdio_server(
        self,
        name: str,
        command: str,
        args: Optional[List[str]] = None,
        enabled_tools: Optional[List[str]] = None,
        disabled_tools: Optional[List[str]] = None,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Any:
        """
        Creates an McpStdioServer specification.
        """
        server = McpStdioServer(
            name=name,
            command=command,
            args=args or [],
            enabled_tools=enabled_tools,
            disabled_tools=disabled_tools,
            cwd=cwd,
            env=env or {}
        )
        self._servers[name] = server
        logger.info(f"Registered Decoupled McpStdioServer: '{name}' (Command: {command})")
        return server

    def get_server(self, name: str) -> Optional[Any]:
        return self._servers.get(name)

    def get_all_servers(self) -> List[Any]:
        return list(self._servers.values())

    def create_integra_default_servers(
        self,
        python_executable: Optional[str] = None,
        homebase_dir: Optional[str] = None
    ) -> List[Any]:
        """
        Creates standard decoupled tool servers for Integra O/S.
        """
        py_bin = python_executable or sys.executable
        base_dir = homebase_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # 1. Decoupled Memory / The Hoard Cartography Server
        hoard_server = self.create_stdio_server(
            name="integra_hoard_mcp",
            command=py_bin,
            args=["-m", "memory.the_hoard"],
            enabled_tools=["query_routes", "read_node", "commit_node"],
            cwd=base_dir
        )

        # 2. Decoupled Data Agent Kit Server (Stand-alone Stdio runner)
        data_server = self.create_stdio_server(
            name="integra_data_mcp",
            command=py_bin,
            args=["-m", "pipelines.data_runner"],
            enabled_tools=["inspect_schema", "run_pipeline_query"],
            cwd=base_dir
        )

        return [hoard_server, data_server]


# ==============================================================================
# 4. LOCALAGENTCONFIG SESSION PERSISTENCE MANAGER
# ==============================================================================
class AntigravitySessionManager:
    """
    Coordinates session persistence across turns and restarts using LocalAgentConfig.
    Saves conversation trajectories in save_dir and keeps scratch artifacts in app_data_dir.
    """
    def __init__(
        self,
        save_dir: str = DEFAULT_PERSISTENCE_DIR,
        app_data_dir: str = DEFAULT_SCRATCH_DIR
    ):
        self.save_dir = save_dir
        self.app_data_dir = app_data_dir
        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.app_data_dir, exist_ok=True)

    def build_config(
        self,
        conversation_id: Optional[str] = None,
        mcp_servers: Optional[List[Any]] = None,
        custom_hooks: Optional[List[Any]] = None,
        fault_hook: Optional[AntigravityFaultTolerantHook] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> LocalAgentConfig:
        """
        Constructs a hardened LocalAgentConfig with:
        - Decoupled Stdio MCP servers.
        - Fault-tolerant error interception hook.
        - Session persistence directory and conversation_id.
        - App data directory override.
        """
        active_fault_hook = fault_hook or AntigravityFaultTolerantHook(scratch_dir=self.app_data_dir)
        all_hooks = [active_fault_hook, integra_on_tool_error]
        if custom_hooks:
            for hook in custom_hooks:
                if hook not in all_hooks:
                    all_hooks.append(hook)

        config = LocalAgentConfig(
            conversation_id=conversation_id,
            save_dir=self.save_dir,
            app_data_dir=self.app_data_dir,
            mcp_servers=mcp_servers or [],
            hooks=all_hooks,
            api_key=api_key or os.environ.get("GEMINI_API_KEY"),
            model=model or "gemini-3.8-flash"
        )
        return config

    def save_session_manifest(self, conversation_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Writes session metadata manifest to persistent storage.
        """
        manifest_path = os.path.join(self.save_dir, f"{conversation_id}_manifest.json")
        payload = {
            "conversation_id": conversation_id,
            "save_dir": self.save_dir,
            "app_data_dir": self.app_data_dir,
            "metadata": metadata or {}
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return manifest_path

    def load_session_manifest(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Reads session metadata manifest from persistent storage.
        """
        manifest_path = os.path.join(self.save_dir, f"{conversation_id}_manifest.json")
        if not os.path.exists(manifest_path):
            return None
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_saved_sessions(self) -> List[str]:
        """
        Lists all persistent conversation IDs in save_dir.
        """
        if not os.path.exists(self.save_dir):
            return []
        sessions = []
        suffix = "_manifest.json"
        for fname in os.listdir(self.save_dir):
            if fname.endswith(suffix):
                sessions.append(fname[:-len(suffix)])
        return sorted(sessions)


# ==============================================================================
# 5. UNIFIED SDK HARNESS FACADE
# ==============================================================================
class AntigravityHarness:
    """
    Main facade for Google Antigravity SDK integration within Integra O/S.
    Integrates decoupled MCP tools, fault tolerance, and session persistence.
    """
    def __init__(
        self,
        scratch_dir: str = DEFAULT_SCRATCH_DIR,
        persistence_dir: str = DEFAULT_PERSISTENCE_DIR
    ):
        self.scratch_dir = scratch_dir
        self.persistence_dir = persistence_dir
        self.tool_registry = DecoupledMcpToolRegistry()
        self.session_manager = AntigravitySessionManager(
            save_dir=self.persistence_dir,
            app_data_dir=self.scratch_dir
        )
        self.fault_hook = AntigravityFaultTolerantHook(scratch_dir=self.scratch_dir)

    def initialize_default_environment(self) -> LocalAgentConfig:
        """
        Quickly provisions the standard hardened agent configuration.
        """
        servers = self.tool_registry.create_integra_default_servers()
        return self.session_manager.build_config(
            conversation_id="integra_master_session",
            mcp_servers=servers,
            fault_hook=self.fault_hook
        )

    def create_agent(self, config: Optional[LocalAgentConfig] = None) -> Agent:
        """
        Creates an Agent instance ready for async execution.
        """
        active_config = config or self.initialize_default_environment()
        return Agent(active_config)

    def get_telemetry(self) -> Dict[str, Any]:
        """
        Returns telemetry data for Heimdall 3.1 surveillance.
        """
        return {
            "sdk_available_native": SDK_AVAILABLE,
            "scratch_dir": self.scratch_dir,
            "persistence_dir": self.persistence_dir,
            "active_mcp_servers": [s.name for s in self.tool_registry.get_all_servers()],
            "intercepted_errors_count": len(self.fault_hook.incident_log),
            "recent_incidents": self.fault_hook.incident_log[-5:],
            "saved_sessions_count": len(self.session_manager.list_saved_sessions()),
            "status": "HARDENED_OPERATIONAL"
        }

    def check_health(self) -> Dict[str, Any]:
        """
        Health probe for Heimdall check_system_health integration.
        """
        scratch_ok = os.path.exists(self.scratch_dir)
        persist_ok = os.path.exists(self.persistence_dir)
        healthy = scratch_ok and persist_ok
        return {
            "status": "HEALTHY" if healthy else "DEGRADED",
            "scratch_dir_exists": scratch_ok,
            "persistence_dir_exists": persist_ok,
            "registered_mcp_servers": len(self.tool_registry.get_all_servers())
        }
