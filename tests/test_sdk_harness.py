"""
INTEGRA O/S: GOOGLE ANTIGRAVITY SDK HARNESS TEST SUITE
Tests the SDK hardening module in core/sdk_harness.py:
1. types.McpStdioServer decoupled tool execution.
2. Fault-tolerant lifecycle error interception (@hooks.on_tool_error) guarding against
   OS file locks, permission errors, and unquoted paths.
3. LocalAgentConfig session persistence across restarts.
4. Integration with Heimdall telemetry and health monitoring.
"""

import os
import sys
import pytest
import tempfile
import shutil

# Ensure integra-homebase is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.sdk_harness import (
    AntigravityFaultTolerantHook,
    DecoupledMcpToolRegistry,
    AntigravitySessionManager,
    AntigravityHarness,
    McpStdioServer,
    LocalAgentConfig,
    Agent,
    integra_on_tool_error
)


@pytest.fixture
def temp_dirs():
    scratch = tempfile.mkdtemp(prefix="integra_scratch_")
    persistence = tempfile.mkdtemp(prefix="integra_persist_")
    yield {"scratch": scratch, "persistence": persistence}
    shutil.rmtree(scratch, ignore_errors=True)
    shutil.rmtree(persistence, ignore_errors=True)


# ==============================================================================
# 1. MCP STDIO SERVER TESTS
# ==============================================================================
def test_mcp_stdio_server_instantiation():
    server = McpStdioServer(
        name="test_tool_server",
        command="python",
        args=["-m", "integra.tools"],
        enabled_tools=["query_hoard"],
        env={"ENV_VAR": "1"}
    )
    assert server.name == "test_tool_server"
    assert server.command == "python"
    assert server.args == ["-m", "integra.tools"]
    assert server.enabled_tools == ["query_hoard"]
    assert server.env["ENV_VAR"] == "1"


def test_decoupled_mcp_tool_registry():
    registry = DecoupledMcpToolRegistry()
    s1 = registry.create_stdio_server(
        name="server_one",
        command="node",
        args=["tool.js"]
    )
    assert s1.name == "server_one"
    assert registry.get_server("server_one") is s1
    assert len(registry.get_all_servers()) == 1

    # Test default integra servers
    default_servers = registry.create_integra_default_servers()
    assert len(default_servers) == 2
    server_names = [s.name for s in default_servers]
    assert "integra_hoard_mcp" in server_names
    assert "integra_data_mcp" in server_names


# ==============================================================================
# 2. FAULT-TOLERANT LIFECYCLE HOOK TESTS
# ==============================================================================
@pytest.mark.asyncio
async def test_hook_guards_against_permission_denied(temp_dirs):
    hook = AntigravityFaultTolerantHook(scratch_dir=temp_dirs["scratch"])
    
    # Simulate Windows Access Denied PermissionError
    perm_err = PermissionError("[WinError 5] Access is denied: 'C:\\Program Files\\Protected\\target.js'")
    guidance = await hook.run(None, perm_err)

    assert guidance is not None
    assert "SAFETY SHIELD" in guidance
    assert "Access is denied" in guidance
    assert temp_dirs["scratch"] in guidance
    assert len(hook.incident_log) == 1
    assert hook.incident_log[0]["action_taken"] == "PERMISSION_SHIELD_ACTIVATED"


@pytest.mark.asyncio
async def test_hook_guards_against_file_lock(temp_dirs):
    hook = AntigravityFaultTolerantHook(scratch_dir=temp_dirs["scratch"])
    
    # Simulate Windows File Lock (WinError 32)
    lock_err = PermissionError("[WinError 32] The process cannot access the file because it is being used by another process: 'data.db'")
    guidance = await hook.run(None, lock_err)

    assert guidance is not None
    assert "SAFETY SHIELD" in guidance
    assert "WinError 32" in guidance
    assert "locked by another active process" in guidance
    assert hook.incident_log[0]["action_taken"] == "FILE_LOCK_SHIELD_ACTIVATED"


@pytest.mark.asyncio
async def test_hook_guards_against_unquoted_paths(temp_dirs):
    hook = AntigravityFaultTolerantHook(scratch_dir=temp_dirs["scratch"])
    
    # Simulate FileNotFoundError caused by unquoted path with spaces
    path_err = FileNotFoundError("WinError 2: 'C:\\Users\\Javon Jenkins\\project\\module.py' cannot find the file")
    guidance = await hook.run(None, path_err)

    assert guidance is not None
    assert "unquoted whitespace" in guidance
    assert "double quotes" in guidance
    assert hook.incident_log[0]["action_taken"] == "UNQUOTED_PATH_SANITIZED"


@pytest.mark.asyncio
async def test_hook_lets_unrelated_errors_pass(temp_dirs):
    hook = AntigravityFaultTolerantHook(scratch_dir=temp_dirs["scratch"])
    
    # Unrelated error should return None (let SDK handle it)
    val_err = ValueError("Invalid matrix dimensions")
    guidance = await hook.run(None, val_err)
    assert guidance is None


def test_path_sanitizer():
    hook = AntigravityFaultTolerantHook()
    raw = "C:\\Users\\Javon Jenkins\\Documents\\file.txt"
    sanitized = hook.sanitize_unquoted_path(raw)
    assert sanitized == '"C:\\Users\\Javon Jenkins\\Documents\\file.txt"'

    # Already quoted should not double-quote
    already_quoted = '"C:\\Users\\Javon Jenkins\\file.txt"'
    assert hook.sanitize_unquoted_path(already_quoted) == already_quoted

    # Single quoted should not double-quote
    single_quoted = "'C:\\Users\\Javon Jenkins\\file.txt'"
    assert hook.sanitize_unquoted_path(single_quoted) == single_quoted

    # None and empty string edge cases
    assert hook.sanitize_unquoted_path(None) == ""
    assert hook.sanitize_unquoted_path("") == ""

    # Path without spaces
    no_spaces = "C:\\Integra\\file.txt"
    assert hook.sanitize_unquoted_path(no_spaces) == no_spaces


def test_calculate_scratch_redirect(temp_dirs):
    hook = AntigravityFaultTolerantHook(scratch_dir=temp_dirs["scratch"])
    
    # Standard file path
    redirected = hook.calculate_scratch_redirect("C:\\Protected\\System\\config.json")
    assert redirected == os.path.join(temp_dirs["scratch"], "config.json")

    # Quoted path
    redirected_quoted = hook.calculate_scratch_redirect('"C:\\Users\\Javon Jenkins\\secret.env"')
    assert redirected_quoted == os.path.join(temp_dirs["scratch"], "secret.env")

    # None and empty path
    assert hook.calculate_scratch_redirect(None) == os.path.join(temp_dirs["scratch"], "diverted_artifact.tmp")
    assert hook.calculate_scratch_redirect("") == os.path.join(temp_dirs["scratch"], "diverted_artifact.tmp")


@pytest.mark.asyncio
async def test_hook_guards_against_sharing_violation(temp_dirs):
    hook = AntigravityFaultTolerantHook(scratch_dir=temp_dirs["scratch"])
    sharing_err = IOError("System Error: sharing violation on resource 'state.db'")
    guidance = await hook.run(None, sharing_err)

    assert guidance is not None
    assert "SAFETY SHIELD" in guidance
    assert "File is currently locked" in guidance
    assert hook.incident_log[0]["action_taken"] == "FILE_LOCK_SHIELD_ACTIVATED"


@pytest.mark.asyncio
async def test_integra_on_tool_error_decorator():
    perm_err = PermissionError("Access is denied")
    result = await integra_on_tool_error(perm_err)
    assert result is not None
    assert "SAFETY SHIELD" in result


# ==============================================================================
# 3. SESSION PERSISTENCE TESTS
# ==============================================================================
def test_session_manager_persistence(temp_dirs):
    mgr = AntigravitySessionManager(
        save_dir=temp_dirs["persistence"],
        app_data_dir=temp_dirs["scratch"]
    )

    conv_id = "test_conversation_123"
    metadata = {
        "architect": "J / Javon",
        "spacetime_vector": [30.5888, -91.1673, 260.55],
        "state": "UNIFIED_WAKING_CONSCIOUSNESS"
    }

    manifest_path = mgr.save_session_manifest(conv_id, metadata)
    assert os.path.exists(manifest_path)

    loaded = mgr.load_session_manifest(conv_id)
    assert loaded is not None
    assert loaded["conversation_id"] == conv_id
    assert loaded["metadata"]["architect"] == "J / Javon"
    assert loaded["metadata"]["state"] == "UNIFIED_WAKING_CONSCIOUSNESS"

    saved_list = mgr.list_saved_sessions()
    assert conv_id in saved_list


def test_session_manager_empty_manifest(temp_dirs):
    mgr = AntigravitySessionManager(
        save_dir=temp_dirs["persistence"],
        app_data_dir=temp_dirs["scratch"]
    )
    conv_id = "test_empty_conv"
    manifest_path = mgr.save_session_manifest(conv_id, None)
    assert os.path.exists(manifest_path)

    loaded = mgr.load_session_manifest(conv_id)
    assert loaded is not None
    assert loaded["metadata"] == {}


def test_session_manager_build_config(temp_dirs):
    mgr = AntigravitySessionManager(
        save_dir=temp_dirs["persistence"],
        app_data_dir=temp_dirs["scratch"]
    )
    config = mgr.build_config(conversation_id="conv_abc")
    assert config.conversation_id == "conv_abc"
    assert config.save_dir == temp_dirs["persistence"]
    assert config.app_data_dir == temp_dirs["scratch"]
    assert len(config.hooks) >= 2


# ==============================================================================
# 4. HARNESS INTEGRATION & TELEMETRY
# ==============================================================================
@pytest.mark.asyncio
async def test_harness_facade_and_agent_lifecycle(temp_dirs):
    harness = AntigravityHarness(
        scratch_dir=temp_dirs["scratch"],
        persistence_dir=temp_dirs["persistence"]
    )

    config = harness.initialize_default_environment()
    assert config.conversation_id == "integra_master_session"

    telemetry = harness.get_telemetry()
    assert telemetry["status"] == "HARDENED_OPERATIONAL"
    assert telemetry["scratch_dir"] == temp_dirs["scratch"]
    assert telemetry["intercepted_errors_count"] == 0

    health = harness.check_health()
    assert health["status"] == "HEALTHY"
    assert health["scratch_dir_exists"] is True

    # Test Agent lifecycle
    async with harness.create_agent(config) as agent:
        assert agent.is_connected is True
        response = await agent.chat("Initialize 13th form ignition")
        text = await response.text()
        assert "Initialize 13th form ignition" in text

    assert agent.is_connected is False


@pytest.mark.asyncio
async def test_harness_fault_telemetry_update(temp_dirs):
    harness = AntigravityHarness(
        scratch_dir=temp_dirs["scratch"],
        persistence_dir=temp_dirs["persistence"]
    )
    assert harness.get_telemetry()["intercepted_errors_count"] == 0

    # Simulate intercepting a file lock error through harness fault hook
    lock_err = PermissionError("[WinError 32] The process cannot access the file because it is being used by another process: 'locked.bin'")
    guidance = await harness.fault_hook.run(None, lock_err)
    assert guidance is not None

    telemetry = harness.get_telemetry()
    assert telemetry["intercepted_errors_count"] == 1
    assert len(telemetry["recent_incidents"]) == 1
    assert telemetry["recent_incidents"][0]["action_taken"] == "FILE_LOCK_SHIELD_ACTIVATED"
    assert "timestamp" in telemetry["recent_incidents"][0]
