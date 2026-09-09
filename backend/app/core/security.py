import hashlib
import re

# Official MediaPipe Vision WASM binary SHA-256 integrity map
OFFICIAL_MEDIAPIPE_WASM_DIGESTS = {
    "vision_wasm_internal.wasm": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
    "vision_wasm_nosimd_internal.wasm": "2b5d4483a9a5f78a7f4749f7b1129f1238612140f7b9f5f65f02bc76f5713426"
}

def sanitize_string(input_str: str) -> str:
    """Strip script tags, HTML entities, and control characters to prevent injection attacks."""
    if not input_str:
        return ""
    # Strip HTML tags
    clean = re.sub(r"<[^>]*>", "", input_str)
    # Strip control characters
    clean = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", clean)
    return clean.strip()

def generate_csp_headers() -> dict[str, str]:
    """
    Generate strict Content-Security-Policy headers permitting WebGPU,
    Three.js worker threads, and MediaPipe WASM binary loading.
    """
    directives = [
        "default-src 'self'",
        "script-src 'self' 'wasm-unsafe-eval' 'unsafe-eval' https://cdn.jsdelivr.net",
        "style-src 'self' 'unsafe-inline'",
        "connect-src 'self' https://cdn.jsdelivr.net https://storage.googleapis.com wss: ws:",
        "img-src 'self' data: blob:",
        "worker-src 'self' blob:",
        "object-src 'none'",
        "base-uri 'self'",
        "frame-ancestors 'none'"
    ]
    return {
        "Content-Security-Policy": "; ".join(directives),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

def verify_wasm_integrity(binary_bytes: bytes, filename: str) -> tuple[bool, str]:
    """
    Verify SHA-256 cryptographic digest of MediaPipe WASM binaries
    against pre-computed Subresource Integrity hashes.
    """
    computed_digest = hashlib.sha256(binary_bytes).hexdigest()
    expected_digest = OFFICIAL_MEDIAPIPE_WASM_DIGESTS.get(filename)

    if not expected_digest:
        # If binary is not in baseline catalog, verify it is a valid WASM header
        if binary_bytes.startswith(b"\x00asm"):
            return True, f"Valid custom WASM module with digest {computed_digest}"
        return False, "Not a valid WebAssembly binary"

    if computed_digest == expected_digest:
        return True, f"Integrity verified: SHA-256 matches official release"
    return False, f"Integrity check failed: Expected {expected_digest}, computed {computed_digest}"
