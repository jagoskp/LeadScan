"use client";

import React from "react";
import type { ConnectorHealthStatus } from "../types/connector";
import { formatHealthBadgeColor } from "../utils/helpers";

interface HealthBadgeProps {
  status: ConnectorHealthStatus;
}

export function HealthBadge({ status }: HealthBadgeProps) {
  const color = formatHealthBadgeColor(status);
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "0.35rem",
        fontSize: "0.75rem",
        fontWeight: 600,
        color,
        padding: "2px 10px",
        borderRadius: "9999px",
        border: `1px solid ${color}`,
        background: `${color}18`,
      }}
    >
      <span style={{ fontSize: "0.6rem" }}>●</span>
      {status}
    </span>
  );
}
