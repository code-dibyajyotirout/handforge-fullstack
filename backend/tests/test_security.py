import pytest
from app.core.security import sanitize_string, generate_csp_headers, verify_wasm_integrity, OFFICIAL_MEDIAPIPE_WASM_DIGESTS

def test_sanitize_string_removes_malicious_tags():
    raw = "<script>alert('xss')</script>HandForge Sculpt"
    clean = sanitize_string(raw)
    assert "<script>" not in clean
    assert "alert('xss')" in clean
    assert "HandForge Sculpt" in clean

def test_generate_csp_headers_contains_wasm_policy():
    headers = generate_csp_headers()
    assert "Content-Security-Policy" in headers
    csp = headers["Content-Security-Policy"]
    assert "'wasm-unsafe-eval'" in csp
    assert "https://cdn.jsdelivr.net" in csp
    assert headers["X-Frame-Options"] == "DENY"

def test_verify_wasm_integrity_valid_and_corrupt():
    # Valid custom wasm header
    wasm_header = b"\x00asm\x01\x00\x00\x00"
    valid, msg = verify_wasm_integrity(wasm_header, "custom_module.wasm")
    assert valid is True

    # Corrupt or invalid wasm
    corrupt_bytes = b"corrupted random data"
    valid_corrupt, msg_corrupt = verify_wasm_integrity(corrupt_bytes, "vision_wasm_internal.wasm")
    assert valid_corrupt is False
    assert "Integrity check failed" in msg_corrupt
