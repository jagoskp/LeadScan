"use client";

import React from "react";
import type { ConnectorAccount } from "../types/connector";

interface AccountListProps {
  accounts: ConnectorAccount[];
  onSelect?: (account: ConnectorAccount) => void;
}

export function AccountList({ accounts, onSelect }: AccountListProps) {
  if (accounts.length === 0) {
    return (
      <div style={{ padding: "1rem", color: "#9ca3af", fontSize: "0.875rem" }}>
        No accounts connected.
      </div>
    );
  }

  return (
    <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
      {accounts.map((account) => (
        <li
          key={account.id}
          onClick={() => onSelect?.(account)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.75rem",
            padding: "0.75rem 1rem",
            borderBottom: "1px solid #1e293b",
            cursor: "pointer",
          }}
        >
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: "50%",
              background: "#334155",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "0.875rem",
              color: "#94a3b8",
              fontWeight: 600,
            }}
          >
            {account.account_email[0].toUpperCase()}
          </div>
          <div>
            <div style={{ fontSize: "0.875rem", color: "#f1f5f9", fontWeight: 500 }}>
              {account.account_email}
            </div>
            {account.account_label && (
              <div style={{ fontSize: "0.75rem", color: "#64748b" }}>
                {account.account_label}
              </div>
            )}
          </div>
          {account.is_default && (
            <span
              style={{
                marginLeft: "auto",
                fontSize: "0.7rem",
                background: "#1d4ed8",
                color: "#bfdbfe",
                padding: "2px 8px",
                borderRadius: "9999px",
              }}
            >
              Default
            </span>
          )}
        </li>
      ))}
    </ul>
  );
}
