# Mermaid Diagrams for 5G Scheduler Simulation Presentation

This document contains Mermaid code for generating flow diagrams, sequence diagrams, and architecture diagrams for presentation materials.

---

## 1. Overall System Architecture

```mermaid
graph TB
    subgraph "5G Base Station System"
        BS[Base Station]
        SCH[Scheduler<br/>RR or PF]
        RB[Resource Blocks<br/>50 RBs]
    end
    
    subgraph "Users"
        U1[User 1<br/>CQI: 12]
        U2[User 2<br/>CQI: 8]
        U3[User 3<br/>CQI: 15]
        U4[User N<br/>CQI: 5]
    end
    
    BS --> SCH
    SCH --> RB
    RB --> U1
    RB --> U2
    RB --> U3
    RB --> U4
    
    U1 -.CQI Feedback.-> BS
    U2 -.CQI Feedback.-> BS
    U3 -.CQI Feedback.-> BS
    U4 -.CQI Feedback.-> BS
    
    style BS fill:#4A90E2
    style SCH fill:#F5A623
    style RB fill:#7ED321
```

---

## 2. Simulation Methodology Flow

```mermaid
flowchart TD
    START([Start Simulation]) --> INIT[Initialize System<br/>Users, RBs, Scheduler]
    INIT --> LOOP{For Each TTI<br/>1 to 1000}
    
    LOOP -->|Next TTI| UPDATE[Update Channel<br/>CQI Values]
    UPDATE --> CALC[Calculate Instantaneous<br/>Throughput]
    CALC --> SCHED[Run Scheduler<br/>Allocate RBs]
    SCHED --> RECORD[Record Metrics<br/>Throughput, Fairness]
    RECORD --> LOOP
    
    LOOP -->|Done| SUMMARY[Calculate Summary<br/>Statistics]
    SUMMARY --> EXPORT[Export to CSV]
    EXPORT --> VIZ[Generate<br/>Visualizations]
    VIZ --> END([End])
    
    style START fill:#50E3C2
    style END fill:#50E3C2
    style SCHED fill:#F5A623
```

---

## 3. Round Robin Scheduler Flow

```mermaid
flowchart LR
    START([Start RR]) --> INIT[User Pointer = 0]
    INIT --> LOOP{More RBs?}
    
    LOOP -->|Yes| ASSIGN[Assign RB to<br/>Current User]
    ASSIGN --> NEXT[Move to<br/>Next User]
    NEXT --> WRAP{Last User?}
    WRAP -->|Yes| RESET[Reset to<br/>User 0]
    WRAP -->|No| LOOP
    RESET --> LOOP
    
    LOOP -->|No| END([Done])
    
    style START fill:#50E3C2
    style END fill:#50E3C2
    style ASSIGN fill:#4A90E2
```

---

## 4. Proportional Fair Scheduler Flow

```mermaid
flowchart TD
    START([Start PF]) --> LOOP{More RBs?}
    
    LOOP -->|Yes| CALC[Calculate PF Metric<br/>for All Users]
    CALC --> METRIC[PF = Instant_Tput /<br/>Avg_Tput]
    METRIC --> SELECT[Select User with<br/>Highest PF Metric]
    SELECT --> ALLOC[Allocate RB<br/>to Selected User]
    ALLOC --> UPDATE[Update User's<br/>Avg Throughput]
    UPDATE --> LOOP
    
    LOOP -->|No| END([Done])
    
    style START fill:#50E3C2
    style END fill:#50E3C2
    style SELECT fill:#F5A623
    style UPDATE fill:#7ED321
```

---

## 5. TTI Execution Sequence

```mermaid
sequenceDiagram
    participant SYS as System
    participant SCH as Scheduler
    participant U1 as User 1
    participant U2 as User 2
    participant U3 as User N
    
    SYS->>SYS: Start TTI
    SYS->>U1: Update CQI
    SYS->>U2: Update CQI
    SYS->>U3: Update CQI
    
    SYS->>U1: Get Instant Throughput
    U1-->>SYS: 5.5 Mbps
    SYS->>U2: Get Instant Throughput
    U2-->>SYS: 2.4 Mbps
    SYS->>U3: Get Instant Throughput
    U3-->>SYS: 1.2 Mbps
    
    SYS->>SCH: Schedule 50 RBs
    
    loop For Each RB
        SCH->>SCH: Select User
        SCH->>U1: Allocate RB
        U1-->>SCH: Acknowledged
    end
    
    SCH-->>SYS: Allocations Complete
    SYS->>SYS: Record Metrics
    SYS->>SYS: End TTI
```

---

## 6. Round Robin vs Proportional Fair Comparison

```mermaid
graph LR
    subgraph "Round Robin"
        RR_IN[All Users] --> RR_PROC[Sequential<br/>Allocation]
        RR_PROC --> RR_OUT[Equal RBs<br/>per User]
    end
    
    subgraph "Proportional Fair"
        PF_IN[All Users +<br/>CQI Info] --> PF_PROC[PF Metric<br/>Calculation]
        PF_PROC --> PF_OUT[Adaptive RB<br/>Allocation]
    end
    
    RR_OUT -.vs.-> PF_OUT
    
    style RR_PROC fill:#4A90E2
    style PF_PROC fill:#F5A623
```

---

## 7. CQI to Throughput Mapping

```mermaid
graph LR
    CQI[CQI Value<br/>1-15] --> MAP{CQI Mapping}
    
    MAP -->|CQI 1-5| LOW[Low Throughput<br/>0.15-0.88 Mbps]
    MAP -->|CQI 6-10| MED[Medium Throughput<br/>1.18-2.73 Mbps]
    MAP -->|CQI 11-15| HIGH[High Throughput<br/>3.32-5.55 Mbps]
    
    LOW --> USER[User Instant<br/>Throughput]
    MED --> USER
    HIGH --> USER
    
    style CQI fill:#50E3C2
    style USER fill:#7ED321
```

---

## 8. Metrics Calculation Flow

```mermaid
flowchart TD
    START([TTI Complete]) --> COLLECT[Collect User<br/>Throughputs]
    
    COLLECT --> TOTAL[Calculate Total<br/>System Throughput]
    COLLECT --> FAIR[Calculate Jain's<br/>Fairness Index]
    COLLECT --> UTIL[Calculate RB<br/>Utilization]
    
    TOTAL --> STORE[Store Metrics]
    FAIR --> STORE
    UTIL --> STORE
    
    STORE --> NEXT{More TTIs?}
    NEXT -->|Yes| CONTINUE([Continue])
    NEXT -->|No| SUMMARY[Generate Summary<br/>Statistics]
    
    SUMMARY --> END([Export Results])
    
    style START fill:#50E3C2
    style END fill:#50E3C2
    style FAIR fill:#F5A623
```

---

## 9. PF Metric Calculation Detail

```mermaid
flowchart LR
    subgraph "User State"
        INST[Instantaneous<br/>Throughput<br/>5.5 Mbps]
        AVG[Average<br/>Throughput<br/>2.2 Mbps]
    end
    
    subgraph "Calculation"
        INST --> DIV[Divide]
        AVG --> DIV
        DIV --> RESULT[PF Metric<br/>2.5]
    end
    
    subgraph "Decision"
        RESULT --> COMP[Compare with<br/>Other Users]
        COMP --> SELECT{Highest?}
        SELECT -->|Yes| ALLOC[Allocate RB]
        SELECT -->|No| SKIP[Skip]
    end
    
    style RESULT fill:#F5A623
    style ALLOC fill:#7ED321
```

---

## 10. Data Export and Visualization Pipeline

```mermaid
flowchart TD
    SIM[Simulation Results] --> PROC[Process Data]
    
    PROC --> CSV1[Per-TTI Results<br/>CSV]
    PROC --> CSV2[Summary Stats<br/>CSV]
    
    PROC --> VIZ[Visualization Engine]
    
    VIZ --> PLOT1[Throughput<br/>Comparison]
    VIZ --> PLOT2[System Throughput<br/>Over Time]
    VIZ --> PLOT3[Fairness<br/>Comparison]
    VIZ --> PLOT4[RB Allocation<br/>Heatmap]
    VIZ --> PLOT5[Summary<br/>Metrics]
    
    CSV1 --> OUTPUT[Output Folder]
    CSV2 --> OUTPUT
    PLOT1 --> OUTPUT
    PLOT2 --> OUTPUT
    PLOT3 --> OUTPUT
    PLOT4 --> OUTPUT
    PLOT5 --> OUTPUT
    
    style SIM fill:#4A90E2
    style OUTPUT fill:#7ED321
```

---

## 11. Class Diagram

```mermaid
classDiagram
    class User {
        +int user_id
        +int cqi
        +float instantaneous_throughput
        +float average_throughput
        +float total_data
        +allocate_rb()
        +get_pf_metric()
        +update_average_throughput()
    }
    
    class BaseScheduler {
        <<abstract>>
        +string name
        +schedule()*
    }
    
    class RoundRobinScheduler {
        +int last_user_index
        +schedule()
    }
    
    class ProportionalFairScheduler {
        +float alpha
        +schedule()
    }
    
    class System {
        +int num_users
        +int num_rbs
        +List~User~ users
        +Scheduler scheduler
        +run_tti()
        +run_simulation()
        +get_summary_statistics()
    }
    
    BaseScheduler <|-- RoundRobinScheduler
    BaseScheduler <|-- ProportionalFairScheduler
    System o-- User
    System o-- BaseScheduler
```

---

## 12. Fairness vs Throughput Trade-off

```mermaid
graph TD
    START[Scheduling Goal] --> CHOICE{Priority?}
    
    CHOICE -->|Fairness| RR[Round Robin]
    CHOICE -->|Throughput| MT[Max Throughput]
    CHOICE -->|Balance| PF[Proportional Fair]
    
    RR --> RR_OUT[Equal RBs<br/>Lower Total Tput<br/>High Fairness]
    MT --> MT_OUT[Unequal RBs<br/>Max Total Tput<br/>Low Fairness]
    PF --> PF_OUT[Adaptive RBs<br/>High Total Tput<br/>Good Fairness]
    
    style RR fill:#4A90E2
    style MT fill:#E74C3C
    style PF fill:#F5A623
    style PF_OUT fill:#7ED321
```

---

## Usage Instructions

To use these diagrams in presentations:

1. **Online Editors:**
   - Copy the code blocks to https://mermaid.live/
   - Export as PNG or SVG

2. **Markdown Renderers:**
   - GitHub, GitLab, and many markdown editors support Mermaid natively
   - Just paste the code blocks in your markdown files

3. **PowerPoint/Google Slides:**
   - Generate images from mermaid.live
   - Insert as images in your presentation

4. **Documentation:**
   - Use in README.md, technical docs, or wiki pages
   - Most modern platforms render Mermaid automatically

---

## Customization Tips

- Change colors: Add `style NodeName fill:#HEXCOLOR`
- Adjust layout: Modify `TB` (top-bottom), `LR` (left-right), `TD` (top-down)
- Add notes: Use `note right of NodeName: Your note`
- Simplify: Remove nodes or connections for simpler diagrams
- Combine: Merge multiple diagrams for comprehensive views

---
