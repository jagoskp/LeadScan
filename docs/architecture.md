# LeadScan AI Architecture Reference

This document outlines the high-level architecture and interactions of the **LeadScan AI** platform.

```mermaid
graph TD
    %% Applications Layer
    subgraph Applications [Applications Layer]
        Web[Web Portal - Next.js]
        Mobile[Mobile App - Flutter]
        Admin[Admin Dashboard - Next.js]
    end

    %% Services Layer
    subgraph Services [Services / Microservices]
        API[API Gateway - FastAPI]
        AIEngine[AI Engine - FastAPI]
        OCREngine[OCR Engine - FastAPI]
        TemporalWorker[Temporal Worker - Worker process]
    end

    %% Packages Layer
    subgraph Packages [Shared Libraries]
        SDK[Client SDK]
        Shared[Common types & validation models]
        Config[Global configuration validation]
        UI[Design System / React Components]
    end

    %% External Infrastructure
    subgraph Infrastructure [Data & Messaging Stores]
        Postgres[(PostgreSQL 18)]
        Redis[(Redis Cache)]
        TemporalServer[(Temporal Cluster)]
        S3Bucket[(S3 Storage)]
    end

    %% Relationships
    Web --> SDK
    Admin --> SDK
    SDK --> API

    API --> Postgres
    API --> Redis
    API --> TemporalServer

    TemporalWorker --> TemporalServer
    TemporalWorker --> OCREngine
    TemporalWorker --> AIEngine
    TemporalWorker --> S3Bucket

    %% Package references
    SDK --> Shared
    Config --> Shared
    UI --> Shared
```

## Directory Ownership & Mapping

- **Client apps** (`apps/`): Consume `@leadscan/sdk` and `@leadscan/ui` libraries.
- **Microservices** (`services/`): Decoupled Python microservices executing specialized tasks.
- **Shared Libraries** (`packages/`): Contains logic reusable across either the node workspace or python modules.
- **Infrastructure** (`infrastructure/`): Declarative setups (docker, kubernetes) configuring external resources.
