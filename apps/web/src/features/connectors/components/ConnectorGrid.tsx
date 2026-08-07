"use client";

import React from "react";
import type { ConnectorDriver } from "../types/connector";

interface ConnectorGridProps {
  drivers: ConnectorDriver[];
  onSelect?: (driver: ConnectorDriver) => void;
}

export function ConnectorGrid({ drivers, onSelect }: ConnectorGridProps) {
  if (drivers.length === 0) {
    return (
      <div style={{ padding: "2rem", textAlign: "center", color: "#9ca3af" }}>
        No connector drivers installed.
      </div>
    );
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
        gap: "1rem",
        padding: "1rem",
      }}
    >
      {drivers.map((driver) => (
        <div
          key={driver.id}
          onClick={() => onSelect?.(driver)}
          style={{
            background: "#1e293b",
            border: "1px solid #334155",
            borderRadius: "12px",
            padding: "1.25rem",
            cursor: "pointer",
            transition: "border-color 0.2s",
          }}
        >
          <div style={{ fontSize: "1.1rem", fontWeight: 600, color: "#f1f5f9" }}>
            {driver.name}
          </div>
          <div style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "0.25rem" }}>
            {driver.connector_type} · v{driver.version}
          </div>
          <div
            style={{
              marginTop: "0.75rem",
              fontSize: "0.75rem",
              color: driver.is_active ? "#22c55e" : "#6b7280",
            }}
          >
            {driver.is_active ? "● Active" : "○ Inactive"}
          </div>
        </div>
      ))}
    </div>
  );
}
