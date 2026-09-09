"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import RecruiterPortal from "@/components/RecruiterPortal";

const Studio = dynamic(() => import("@/components/Studio"), { ssr: false });

export default function HomePage() {
  const [viewMode, setViewMode] = useState<"studio" | "eval">("studio");

  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh", overflow: "hidden" }}>
      {/* Mode Switcher */}
      <div style={{
        position: "fixed",
        top: "8px",
        left: "50%",
        transform: "translateX(-50%)",
        zIndex: 99999,
        display: "flex",
        background: "rgba(15, 23, 42, 0.85)",
        border: "1px solid rgba(56, 189, 248, 0.3)",
        borderRadius: "8px",
        padding: "3px",
        backdropFilter: "blur(12px)",
        boxShadow: "0 8px 32px rgba(0, 0, 0, 0.5)"
      }}>
        <button
          onClick={() => setViewMode("studio")}
          style={{
            background: viewMode === "studio" ? "#2563eb" : "transparent",
            color: viewMode === "studio" ? "#ffffff" : "#94a3b8",
            border: "none",
            borderRadius: "6px",
            padding: "6px 14px",
            fontSize: "12px",
            fontWeight: 600,
            cursor: "pointer",
            transition: "all 0.15s ease"
          }}
        >
          3D Sculpting Studio
        </button>
        <button
          onClick={() => setViewMode("eval")}
          style={{
            background: viewMode === "eval" ? "#0284c7" : "transparent",
            color: viewMode === "eval" ? "#ffffff" : "#94a3b8",
            border: "none",
            borderRadius: "6px",
            padding: "6px 14px",
            fontSize: "12px",
            fontWeight: 600,
            cursor: "pointer",
            transition: "all 0.15s ease"
          }}
        >
          Recruiter Proof Portal (12 Tabs)
        </button>
      </div>

      {viewMode === "studio" ? (
        <Studio />
      ) : (
        <div style={{ width: "100vw", height: "100vh", overflowY: "auto" }}>
          <RecruiterPortal />
        </div>
      )}
    </div>
  );
}
