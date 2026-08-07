"use client";

import React from "react";
import { useConnectorStudio } from "../hooks/useConnectorStudio";
import { ConnectorGrid } from "../components/ConnectorGrid";
import { AccountList } from "../components/AccountList";
import { HealthBadge } from "../components/HealthBadge";
import type { ConnectorHealthStatus } from "../types/connector";

export default function ConnectorStudioPage() {
  const {
    drivers,
    connections,
    selectedConnection,
    isLoading,
    error,
    selectConnection,
    handleTest,
    handleHealthCheck,
    handleRefresh,
    handleDelete,
  } = useConnectorStudio();

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "#f1f5f9",
        fontFamily: "'Inter', sans-serif",
        padding: "2rem",
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 700, margin: 0 }}>
          Connector Studio
        </h1>
        <p style={{ color: "#94a3b8", marginTop: "0.5rem", fontSize: "0.9rem" }}>
          Manage external integrations, accounts and connection links.
        </p>
      </div>

      {isLoading && (
        <div style={{ color: "#94a3b8", textAlign: "center", padding: "2rem" }}>
          Loading connectors…
        </div>
      )}

      {error && (
        <div
          style={{
            background: "#7f1d1d",
            border: "1px solid #dc2626",
            borderRadius: "8px",
            padding: "1rem",
            color: "#fca5a5",
            marginBottom: "1rem",
          }}
        >
          {error}
        </div>
      )}

      {/* Installed Drivers */}
      <section style={{ marginBottom: "2.5rem" }}>
        <h2 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem" }}>
          Installed Drivers
        </h2>
        <ConnectorGrid drivers={drivers} />
      </section>

      {/* Active Connections */}
      <section>
        <h2 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "1rem" }}>
          Connections
        </h2>
        {connections.length === 0 ? (
          <p style={{ color: "#64748b", fontSize: "0.875rem" }}>
            No connections configured.
          </p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {connections.map((conn) => {
              const latestHealth = conn.health_records?.at(-1);
              return (
                <div
                  key={conn.id}
                  style={{
                    background: "#1e293b",
                    border:
                      selectedConnection?.id === conn.id
                        ? "1px solid #3b82f6"
                        : "1px solid #334155",
                    borderRadius: "12px",
                    padding: "1.25rem",
                    cursor: "pointer",
                  }}
                  onClick={() =>
                    selectConnection(
                      selectedConnection?.id === conn.id ? null : conn
                    )
                  }
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 600 }}>{conn.name}</div>
                      <div style={{ fontSize: "0.8rem", color: "#64748b", marginTop: 2 }}>
                        {conn.is_enabled ? "Enabled" : "Disabled"}
                        {conn.labels.length > 0 && ` · ${conn.labels.join(", ")}`}
                      </div>
                    </div>
                    {latestHealth && (
                      <HealthBadge
                        status={latestHealth.status as ConnectorHealthStatus}
                      />
                    )}
                  </div>

                  {/* Action buttons */}
                  {selectedConnection?.id === conn.id && (
                    <div
                      style={{
                        display: "flex",
                        gap: "0.75rem",
                        marginTop: "1rem",
                        flexWrap: "wrap",
                      }}
                    >
                      {[
                        {
                          label: "Test",
                          action: () => handleTest(conn.id),
                          color: "#3b82f6",
                        },
                        {
                          label: "Health Check",
                          action: () => handleHealthCheck(conn.id),
                          color: "#22c55e",
                        },
                        {
                          label: "Refresh Token",
                          action: () => handleRefresh(conn.id),
                          color: "#f59e0b",
                        },
                        {
                          label: "Delete",
                          action: () => handleDelete(conn.id),
                          color: "#ef4444",
                        },
                      ].map(({ label, action, color }) => (
                        <button
                          key={label}
                          onClick={(e) => {
                            e.stopPropagation();
                            action();
                          }}
                          style={{
                            background: "transparent",
                            border: `1px solid ${color}`,
                            color,
                            borderRadius: "8px",
                            padding: "0.4rem 0.9rem",
                            fontSize: "0.8rem",
                            cursor: "pointer",
                            fontWeight: 500,
                          }}
                        >
                          {label}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}
