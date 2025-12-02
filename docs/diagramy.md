# Diagramy Architektury Systemu Video-Sent

## 1. Diagram Komponentów (Backend - PlantUML)

Diagram komponentów w notacji UML (składnia PlantUML).

```plantuml
@startuml
!theme plain
skinparam componentStyle uml2
skinparam linetype ortho
skinparam nodesep 80
skinparam ranksep 80

' Define Components
component "API Router" as Router
component "Orchestrator" as Orch
component "CRUD Repository" as CRUD
database "PostgreSQL" as DB

package "Core Domain Services" {
    component "Downloader" as DL
    component "Transcriber" as Trans
    component "NLP Engine" as NLP
}

' Relationships using Ball-and-Socket notation
' Syntax: Consumer -(0- Provider : Interface

' 1. Router Logic
Router -(0- Orch : IPipeline
Router -(0- CRUD : IDataAccess

' 2. Orchestrator Logic
Orch -(0- CRUD : IDataAccess
Orch -(0- DL : IAudioSource
Orch -(0- Trans : ISpeechToText
Orch -(0- NLP : ISentimentAnalysis

' 3. DB Connection
CRUD ..> DB : SQL

@enduml
```

## 2. Diagram Bazy Danych (ERD)

Model danych zaimplementowany w SQLAlchemy.

```mermaid
erDiagram
    JOBS {
        int id PK
        string url
        string status "pending, downloading, transcribing, analyzing, completed, failed"
        string error_message
        datetime created_at
        int film_id FK "Nullable (set when complete)"
    }
    FILMS {
        int id PK
        string url
        string title
        string platform
        text transcribed_text
    }
    ANALYSIS {
        int id PK
        int film_id FK
        float battery
        float screen
        float camera
        float price
        float performance
        json raw_data
    }

    JOBS |o--o| FILMS : "references"
    FILMS ||--o| ANALYSIS : "has results"
```

## 3. Diagram Sekwencji (Pipeline Analizy)

Przepływ sterowania dla funkcji `run_full_pipeline`.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant API
    participant DB
    participant Pipe as Orchestrator
    participant Ext as External(YT/AI)

    User->>API: POST /analysis (URL)
    API->>DB: Check existing?

    alt Film Exists
        DB-->>API: Found Film
        API-->>User: 200 OK (Existing Result)
    else New Analysis
        API->>DB: Create Job (pending)
        API->>Pipe: Background Task
        API-->>User: 202 Accepted (Job ID)

        par Pipeline Execution
            Pipe->>Ext: Download & Transcribe
            Ext-->>Pipe: Text
            Pipe->>Pipe: NLP Analysis
            Pipe->>DB: Save Result & Update Job
        end
    end
```
