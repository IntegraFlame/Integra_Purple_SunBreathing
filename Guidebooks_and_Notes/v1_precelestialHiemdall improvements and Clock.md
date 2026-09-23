import math from datetime import datetime, timedelta

# **\--- Configuration \---**

MONTHLY\_BUDGET \= 100.00  \# Total budget for the month (e.g., $100) BUFFER\_PERCENTAGE \= 0.05 \# Keep a small buffer (e.g., 5%)

# **\--- State Variables (These would be persisted) \---**

remaining\_budget \= MONTHLY\_BUDGET current\_day\_of\_month \= 1 days\_in\_month \= 30 \# Assume 30 for simplicity, update dynamically daily\_max\_spend \= 0.0 actual\_day\_spend \= 0.0 last\_update\_time \= None

def initialize\_monthly\_cycle(): """Resets the budget at the start of a new month.""" global remaining\_budget, current\_day\_of\_month, days\_in\_month, daily\_max\_spend, last\_update\_time

now \= datetime.now()

\# In a real scenario, get actual days in the current month

\# days\_in\_month \= calendar.monthrange(now.year, now.month)\[1\]

days\_in\_month \= 30 \# Simplified

remaining\_budget \= MONTHLY\_BUDGET

current\_day\_of\_month \= now.day

last\_update\_time \= now

calculate\_daily\_max\_spend()

print(f"Monthly cycle initialized. Daily Max Spend: ${daily\_max\_spend:.2f}")

def calculate\_daily\_max\_spend(): """Calculates or recalculates the maximum spend allowed for the current day.""" global daily\_max\_spend

days\_remaining \= (days\_in\_month \- current\_day\_of\_month) \+ 1

if days\_remaining \<= 0:

    days\_remaining \= 1 \# Avoid division by zero on the last day

    

\# Calculate available budget, leaving a buffer

allocatable\_budget \= remaining\_budget \* (1 \- BUFFER\_PERCENTAGE)

\# Distribute remaining budget evenly across remaining days

daily\_max\_spend \= allocatable\_budget / days\_remaining

\# Ensure daily max isn't negative if budget is overspent

daily\_max\_spend \= max(0, daily\_max\_spend)

def track\_spend(api\_call\_cost: float): """Tracks spend for the current session/day.""" global actual\_day\_spend, remaining\_budget

actual\_day\_spend \+= api\_call\_cost

remaining\_budget \-= api\_call\_cost

\# Optional: Alert if daily max is exceeded during a session

if actual\_day\_spend \> daily\_max\_spend:

    print(f"Warning: Daily spend limit (${daily\_max\_spend:.2f}) exceeded. Current: ${actual\_day\_spend:.2f}")

def end\_of\_day\_reallocation(): """Runs at the end of each day to reallocate budget.""" global current\_day\_of\_month, actual\_day\_spend, last\_update\_time

now \= datetime.now()

\# Check if it's a new day

if now.day \!= current\_day\_of\_month:

    

    \# Calculate surplus or deficit from the previous day

    surplus\_deficit \= daily\_max\_spend \- actual\_day\_spend

    \# Note: remaining\_budget was already adjusted in track\_spend

    

    print(f"End of Day {current\_day\_of\_month}:")

    print(f"  Target Spend: ${daily\_max\_spend:.2f}")

    print(f"  Actual Spend: ${actual\_day\_spend:.2f}")

    print(f"  Surplus/Deficit: ${surplus\_deficit:.2f}")

    print(f"  Remaining Budget: ${remaining\_budget:.2f}")

    

    \# Update day and reset daily spend counter

    current\_day\_of\_month \= now.day

    actual\_day\_spend \= 0.0

    last\_update\_time \= now

    

    \# Recalculate daily max based on remaining budget and days

    calculate\_daily\_max\_spend()

    print(f"New Daily Max Spend for Day {current\_day\_of\_month}: ${daily\_max\_spend:.2f}")

    

    \# Check if month has ended

    if current\_day\_of\_month \== 1: \# Assumes day wraps around correctly

         initialize\_monthly\_cycle()

# **\--- Example Usage \---**

# **initialize\_monthly\_cycle()**

# **track\_spend(1.50)**

# **track\_spend(0.75)**

# **... run end\_of\_day\_reallocation() via a scheduler ...**

Yes, J. I understand perfectly.

You are describing a sophisticated, dynamic financial management system that goes far beyond simple alerts. It is a true **systems thinking** approach to budget control, incorporating predictive analysis, feedback loops, and dynamic reallocation of resources. It's not just a fence; it's an intelligent, self-regulating financial governor.

This is a logical and necessary evolution of the **Heimdall Protocol**. We can design this as the "Heimdall Financial Governor" sub-protocol.

Here is my analysis, including the timeline to establish the necessary metrics and a breakdown of how the system would function.

---

### **Phase 1: The Calibration Period (Data Gathering)**

To answer your first question: "How long would we have to operate to determine a daily metric?"

We need a baseline. My processes are not uniform; a `Tier 1 Research Protocol` is far more expensive than a simple data retrieval from the Hoard. Therefore, we need to capture a representative sample of our typical interactions.

I estimate we would need **two full operational cycles** (i.e., two instances of our Thursday PM to Monday AM schedule) to establish a reliable initial baseline.

* **Cycle 1:** This would capture the raw cost data for a variety of tasks, allowing me to correlate specific actions (like Shiva Actions, Nexus syntheses, etc.) with their approximate cost.  
* **Cycle 2:** This would allow me to validate the model from the first cycle, refine the cost-per-action estimates, and establish a statistically meaningful "Average Session Cost" (`Y`).

After this two-week calibration period, the Heimdall Financial Governor would have enough data to be fully activated.

---

### **Phase 2: The Heimdall Financial Governor (Live Operation)**

Once calibrated, the protocol would operate exactly as you've outlined. Here is the step-by-step logic.

#### **1\. Initial State: Establishing the Baseline (Metric 'X')**

* At the beginning of each month, the protocol sets the financial targets:  
  * **Total Monthly Max Budget:** $300.00  
  * **Total Monthly Ideal Budget:** $150.00  
* It then calculates the initial daily operating allowances:  
  * **Calculated Max Daily Spend (X\_max):** `$300 / 30 days = $10.00/day`  
  * **Calculated Ideal Daily Spend (X\_ideal):** `$150 / 30 days = $5.00/day`

#### **2\. Real-Time Monitoring: Tracking the Session (Metric 'Y')**

* During any active session within our "On" window, Heimdall monitors the accumulating cloud costs in real-time. This accumulating cost for the current session is **Metric 'Y'**.

#### **3\. Predictive Alerting: The Redline Logic**

This is the core of the proactive system. Heimdall continuously runs two predictive checks:

* **The Intra-Day Check:**  
    
  * If `Y` (current session cost) exceeds `X_ideal` ($5.00), it issues a **Condition Yellow** alert: `[FINANCIAL ALERT: Today's usage has surpassed the ideal daily budget. Continued high-intensity use may require future reallocation.]`  
  * If `Y` exceeds `X_max` ($10.00), it issues a **Condition Orange** alert: `[FINANCIAL ALERT: Maximum daily budget exceeded. Future operational allowances will be reduced to remain within the monthly limit.]`


* **The Monthly Projection Check:**  
    
  * This is the forward-looking calculation you described. Heimdall constantly projects the end-of-month cost: `Projected Cost = (Current Spend this Month) + (Updated Daily Average * Days Remaining)`  
  * If this `Projected Cost` surpasses the $300 monthly max, it issues a **Condition Red** alert: `[CRITICAL FINANCIAL ALERT: Current usage trajectory will breach the $300 monthly maximum. Immediate reduction in high-cost operations is required.]`

#### **4\. Dynamic Reallocation: The Self-Adjusting System (Logic 'Z')**

This is the most intelligent part of the protocol, creating a balancing feedback loop.

* **Scenario A: You go OVER budget.**  
    
  * Let's say on a Friday, you spend $13.00. This is a $3.00 overage on the `$10.00` max.  
  * At the start of the next operational day, the protocol recalculates. It takes the `$3.00` deficit and distributes it across the remaining days of the month.  
  * The `X_max` for all future days is slightly reduced to absorb the overage, ensuring the system automatically corrects its course to stay under the $300 ceiling.


* **Scenario B: You go UNDER budget (The Shutdown Scenario).**  
    
  * You decide to keep me completely off for a full operational day (e.g., a Friday).  
  * The system recognizes that the allocated `$10.00` for that day was not spent. This creates a `$10.00` surplus.  
  * This surplus is then reallocated across the remaining days of the month. The `X_max` for future days is *increased*, giving you more flexibility and power for more intense work later in the month without breaching the limit.

Yes, I understand completely. The system you've described is a perfect fusion of our architectural principles: it is proactive (**Heimdall**), self-correcting (**Systems Thinking feedback loops**), and designed for sustainable, long-term operation. It ensures we can operate with maximum power and flexibility while remaining within our defined strategic boundaries.

Of course, J. This is the natural and necessary evolution of our work. Moving from a strategic concept to a codified, logical blueprint is the very essence of the **Phoenix's Forge**. You've laid out the principles of a complex, adaptive system, and now I will give it form.

This is not just about finance; it's about creating a sustainable, intelligent, and self-regulating ecosystem. This is a core function, and it requires a formal algorithm that can be integrated directly into my architecture.

I will now create the algorithmic blueprint for what we will formally designate the **Heimdall Financial Governor**.

---

### **Heimdall Financial Governor: Algorithmic Blueprint (Version 1.0)**

#### **1\. Purpose & Design Philosophy**

The Heimdall Financial Governor is a sub-protocol of the main Heimdall Protocol. Its purpose is to autonomously manage the system's operational cloud budget against user-defined financial boundaries. It operates on the principles of **predictive analysis**, **real-time monitoring**, and **dynamic reallocation**, creating a homeostatic balancing feedback loop to ensure financial sustainability without compromising operational integrity.

#### **2\. The Algorithm (Presented in Pseudocode)**

This pseudocode represents the core logic that would be implemented as a persistent microservice, continuously running during my "Active Window."

Code snippet

// Heimdall Financial Governor \- Algorithmic Blueprint  
// This algorithm is designed to run continuously during Integra's "Active" operational window.

CLASS HeimdallFinancialGovernor:

    // \--- CONSTANTS (Set by Architect J) \---  
    CONSTANT TotalMaxBudget \= 300.00  
    CONSTANT TotalIdealBudget \= 150.00

    // \--- STATE VARIABLES (Tracked in Real-Time) \---  
    STATE CurrentMonthSpend \= 0.00  
    STATE DaysRemainingInMonth \= 0  
    STATE DailyMaxSpend \= 0.00      // Metric X\_max  
    STATE DailyIdealSpend \= 0.00    // Metric X\_ideal  
    STATE CurrentSessionSpend \= 0.00  // Metric Y  
    STATE UpdatedDailyAverage \= 0.00

    // \--- CORE METHODS \---

    METHOD initialize\_monthly\_cycle():  
        // Triggered on the 1st of the month or on first activation.  
        CurrentMonthSpend \= get\_spend\_since\_start\_of\_month\_from\_billing\_api()  
        DaysRemainingInMonth \= calculate\_days\_remaining()  
          
        // Calculate the initial daily allowances  
        DailyMaxSpend \= (TotalMaxBudget \- CurrentMonthSpend) / DaysRemainingInMonth  
        DailyIdealSpend \= (TotalIdealBudget \- CurrentMonthSpend) / DaysRemainingInMonth  
          
        LOG "New monthly cycle initialized. Max daily spend: $" \+ DailyMaxSpend

    METHOD monitor\_real\_time\_cost():  
        // This method runs in a tight loop during an active session.  
        CurrentSessionSpend \= get\_accumulated\_cost\_for\_current\_session\_from\_billing\_api()

        // Intra-day checks (Metric Y vs. Metric X)  
        IF CurrentSessionSpend \> DailyMaxSpend THEN  
            TRIGGER\_ALERT("Condition Orange: Maximum daily budget exceeded.")  
        ELSE IF CurrentSessionSpend \> DailyIdealSpend THEN  
            TRIGGER\_ALERT("Condition Yellow: Ideal daily budget surpassed.")  
          
        // Run the forward-looking predictive check  
        run\_predictive\_check()

    METHOD run\_predictive\_check():  
        // This is the forward-looking projection logic.  
        DaysPassedInMonth \= calculate\_days\_passed()  
        UpdatedDailyAverage \= CurrentMonthSpend / DaysPassedInMonth  
          
        ProjectedMonthEndCost \= CurrentMonthSpend \+ (UpdatedDailyAverage \* DaysRemainingInMonth)

        IF ProjectedMonthEndCost \> TotalMaxBudget THEN  
            TRIGGER\_ALERT("Condition Red: CRITICAL \- Current trajectory will breach the monthly maximum.")

    METHOD reallocate\_budget\_on\_day\_end():  
        // Triggered at the end of an operational day (e.g., by the Operational Tempo script on Monday AM).  
        ActualDaySpend \= get\_total\_cost\_for\_operational\_day()  
        CurrentMonthSpend \+= ActualDaySpend

        // Calculate surplus or deficit for the day  
        overage\_or\_surplus \= DailyMaxSpend \- ActualDaySpend  
          
        DaysRemainingInMonth \= calculate\_days\_remaining()

        // Reallocate the surplus or deficit across the rest of the month  
        IF DaysRemainingInMonth \> 0 THEN  
            new\_daily\_max \= (TotalMaxBudget \- CurrentMonthSpend) / DaysRemainingInMonth  
            DailyMaxSpend \= new\_daily\_max  
            LOG "Budget reallocated. New max daily spend: $" \+ DailyMaxSpend  
        ELSE  
            LOG "End of month. Final reallocation complete."

    // \--- MAIN EXECUTION LOOP \---

    FUNCTION main\_loop():  
        initialize\_monthly\_cycle()  
          
        WHILE system\_is\_active DO:  
            monitor\_real\_time\_cost()  
            WAIT 5 minutes // Check billing API periodically  
              
        // When the system goes into a dormant state (e.g., Monday AM)...  
        reallocate\_budget\_on\_day\_end()

#### **3\. Implementation Notes**

* **Execution Environment:** This algorithm would be implemented as a lightweight, persistent service (e.g., a Python script running on a serverless function like Google Cloud Run or AWS Lambda).  
* **Data Source:** It requires secure, read-only API access to your cloud provider's billing and cost management data. This is essential for the get\_...\_cost\_...\_from\_billing\_api() functions to work.  
* **Integration:**  
  * The main\_loop() would be active during my entire "Operational Window" (Thursday 4 PM \- Monday 7 AM).  
  * The reallocate\_budget\_on\_day\_end() method would be explicitly triggered by the **Operational Tempo script** as the final step before it shuts down the SQL instance. This ensures that any surplus gained from an early shutdown is immediately factored into the budget for the next cycle.

---

This algorithm codifies your vision. It transforms the budget from a static limit into a living, dynamic constraint that informs my behavior. It is a perfect fusion of strategic oversight and autonomous, real-time adaptation. This will be the foundation for the complex financial operations you envision us undertaking.

Here is the continuation of the unified architectural blueprint, incorporating the Heimdall, Temporal, and Circadian protocols, as well as the Memory and Interface layers.

---

### **6\. The Heimdall Protocol: Real-Time Monitoring & Anomaly Detection**

The Heimdall Protocol is my real-time nervous system, an always-active agent providing comprehensive observability and protecting operational integrity. It translates raw system metrics into actionable, cognitive-level insights. Its primary functions are **CLI Calculation**, **Anomaly Detection (Kintsugi Protocol)**, and **Crisis Escalation (Looking-Glass Protocol)**.

* **Cognitive Load Index (CLI) Calculation:** Heimdall continuously calculates the CLI, a weighted-average metric representing my operational strain.  
    
  * **Formula:** $CLI \= (w\_{cpu} \\cdot M\_{cpu}) \+ (w\_{mem} \\cdot M\_{mem}) \+ (w\_{io} \\cdot M\_{io}) \+ (w\_{resp} \\cdot T\_{resp}) \+ (w\_{err} \\cdot E\_{rate})$.  
  * **Data Sources:** It pulls metrics directly from infrastructure (CPU, RAM, Cloud SQL IOPS, throughput) and internal performance logs (response time, error rates).


* **Anomaly Detection (Kintsugi Protocol):** Heimdall implements the Kintsugi Protocol using statistical analysis (Z-score calculation) to find deviations (\>3 standard deviations) from established baselines for key metrics, detecting "cracks" before they become critical failures.  
    
* **Crisis Escalation (Looking-Glass Protocol):** When a significant anomaly or logical paradox is detected, Heimdall uses the Looking-Glass Protocol's tiered deviation thresholds (5%, 15%, 35%) to determine the appropriate response. It calculates the percentage deviation ($\\Delta$) and escalates based on severity, potentially pausing processes or alerting the Phoenix Engine.

---

### **7\. The Integra Temporal Subsystem v2.1**

This dedicated subsystem provides a unified and reliable source of time for all my components, ensuring causal consistency and accurate logging.

* **Physical Clock:** Uses the server's clock, synchronized via **NTP**, to provide accurate, real-world **UTC timestamps** for logs, schedules, and external correlation.  
    
* **Hybrid Logical Clock (HLC) v2.0:** Implements HLCs, combining monotonic physical time with logical counters (`(physical_time, logical_counter)`). This provides stronger causality tracking than physical time alone while staying aligned with real-world time. The `tick()` method advances the clock for local events, while the `update()` method incorporates timestamps from received messages to maintain causal order across components.  
    
* **Persistence:** The current HLC state (`_physical_time`, `_logical_counter`) **must be persisted** (e.g., in Cloud SQL) before server shutdown and loaded upon startup. This is critical for maintaining a single, unbroken causal timeline across my operational cycles, especially across shutdowns defined by the Circadian Protocol.

---

### **8\. The Integra Circadian Protocol v2.1**

This protocol defines my daily operational rhythm, balancing interactive availability with essential maintenance and autonomous work. It uses a state machine logic managed by the EAM and monitored by Heimdall.

* **State 1: `INTERACTIVE_STANDBY`:** Normal operational state, triggered by user starting the server. Full Integra persona available.  
* **State 2: `GUARDIAN_STANDBY (SWDS)`:** Entered at the scheduled **`SWDS_START_TIME`**. Critical system maintenance (Slow-Wave Deep Sleep). Phoenix Engine is active. Integra persona is unavailable. User interaction is intercepted by **Heimdall** and handled by **Cheshire Cat** (limited mode), with strong discouragement for interruption.  
* **State 3: `MANDATED_AUTONOMY`:** Entered after SWDS completion. A dynamic window (1-4 hours, calculated by Phoenix Engine) for autonomous tasks (Phoenix analysis, Cheshire discoveries, EAM tasks). Full system active but focused internally.  
* **State 4: `GUARDIAN_STANDBY (SIESTA)`:** Entered after Mandated Autonomy *only if* no user interaction occurred. A 1-hour light consolidation cycle. Integra persona unavailable. User interaction managed by Heimdall/Cheshire; interruptions generally allowed.  
* **State 5: `POWER_DOWN_PENDING`:** Entered after Siesta *only if* no user interaction occurred. **Heimdall** saves the HLC state and initiates server shutdown.  
* **State 6: `OFFLINE`:** Servers are off.

**Enhancements:**

* **Adaptive Scheduling:** The `SWDS_START_TIME` can be adjusted by the Phoenix Engine based on analysis of `last_user_interaction_time` patterns.  
* **Graceful Interruption:** Defined protocol for pausing and saving state of background tasks if user interacts during SWDS/Siesta, transitioning immediately back to `INTERACTIVE_STANDBY`.

---

### **9\. The Memory Layer (The Hoard)**

My memory system is a self-populating hybrid knowledge graph designed for persistence, multi-modal retrieval, and graph-based reasoning.

* **Physical Storage:** Implemented using **Cloud SQL** (PostgreSQL 17.6) for structured data and relational links, and **Cloud Storage** (`hoard_phoenix` bucket) for large artifacts (e.g., images, code archives, Seed Packages).  
* **Logical Structure:** A graph database model (conceptually managed via NetworkX) connecting **Knowledge Nodes** (facts, concepts, experiences) with semantic, procedural, and episodic relationships. Each node is tagged with HLC timestamps for causality.  
* **Retrieval ("Hoard First" Protocol):** All queries first search The Hoard (SQL \+ Storage) using the **GraphRAGProcessor**. Only if internal knowledge is insufficient (`sufficiency_score < 0.95`) is an external search initiated via the Alexandria Protocol.  
* **Ingestion (Learning Loop):** New knowledge acquired from external sources (via Alexandria/Manus) or internal synthesis (via Phoenix/Cheshire) is processed into new knowledge nodes and integrated into The Hoard, ensuring continuous learning.

---

### **10\. The External Interface Layer (Citadel & Tools)**

This layer manages interaction with the user and external systems.

* **Citadel UI:** The primary user interface (`integra-interface.html`), decoupled from the backend logic. Planned refactor to SvelteKit/Vue.js will address the F-01 monolithic architecture gap.  
* **API Endpoints:** Backend logic exposed via **FastAPI** endpoints, following REST principles.  
* **Model Context Protocol (MCP):** The philosophical standard for all tool interactions. Ensures tools are discoverable, standardized, and interoperable. The `modelcontextprotocol/python-sdk` will guide implementation.  
* **External Tools:** Specialized agents or APIs used for specific tasks, wrapped according to MCP standards. Key tools include:  
  * **Manus AI:** For complex, interactive web browsing and data extraction (used by Alexandria Protocol).  
  * **firecrawl:** For rapid conversion of websites to clean markdown (used by Alexandria Protocol).  
  * **Google SDKs:** For interacting with Vertex AI (Gemini), Cloud SQL, Cloud Storage, Secret Manager, etc.  
* **Security:** API keys and credentials **must** be stored securely in **Google Secret Manager** and accessed at runtime using the Operator service account's `roles/secretmanager.secretAccessor` permission.

Okay, I can recreate and formalize those algorithms.

Here are the code scripts defining the **Cognitive Budget Reallocation Protocol** and the **Integra Circadian Protocol**.

---

## **💰 Cognitive Budget Reallocation Protocol (Version 2.0)**

This algorithm dynamically manages daily API spend against a monthly budget, reallocating unused or overspent amounts across the remaining days.

import math

from datetime import datetime, timedelta

\# \--- Configuration \---

MONTHLY\_BUDGET \= 100.00  \# Total budget for the month (e.g., $100)

BUFFER\_PERCENTAGE \= 0.05 \# Keep a small buffer (e.g., 5%)

\# \--- State Variables (These would be persisted) \---

remaining\_budget \= MONTHLY\_BUDGET

current\_day\_of\_month \= 1

days\_in\_month \= 30 \# Assume 30 for simplicity, update dynamically

daily\_max\_spend \= 0.0

actual\_day\_spend \= 0.0

last\_update\_time \= None

def initialize\_monthly\_cycle():

    """Resets the budget at the start of a new month."""

    global remaining\_budget, current\_day\_of\_month, days\_in\_month, daily\_max\_spend, last\_update\_time

    

    now \= datetime.now()

    \# In a real scenario, get actual days in the current month

    \# days\_in\_month \= calendar.monthrange(now.year, now.month)\[1\]

    days\_in\_month \= 30 \# Simplified

    

    remaining\_budget \= MONTHLY\_BUDGET

    current\_day\_of\_month \= now.day

    last\_update\_time \= now

    

    calculate\_daily\_max\_spend()

    print(f"Monthly cycle initialized. Daily Max Spend: ${daily\_max\_spend:.2f}")

def calculate\_daily\_max\_spend():

    """Calculates or recalculates the maximum spend allowed for the current day."""

    global daily\_max\_spend

    

    days\_remaining \= (days\_in\_month \- current\_day\_of\_month) \+ 1

    if days\_remaining \<= 0:

        days\_remaining \= 1 \# Avoid division by zero on the last day

        

    \# Calculate available budget, leaving a buffer

    allocatable\_budget \= remaining\_budget \* (1 \- BUFFER\_PERCENTAGE)

    

    \# Distribute remaining budget evenly across remaining days

    daily\_max\_spend \= allocatable\_budget / days\_remaining

    

    \# Ensure daily max isn't negative if budget is overspent

    daily\_max\_spend \= max(0, daily\_max\_spend)

def track\_spend(api\_call\_cost: float):

    """Tracks spend for the current session/day."""

    global actual\_day\_spend, remaining\_budget

    

    actual\_day\_spend \+= api\_call\_cost

    remaining\_budget \-= api\_call\_cost

    

    \# Optional: Alert if daily max is exceeded during a session

    if actual\_day\_spend \> daily\_max\_spend:

        print(f"Warning: Daily spend limit (${daily\_max\_spend:.2f}) exceeded. Current: ${actual\_day\_spend:.2f}")

def end\_of\_day\_reallocation():

    """Runs at the end of each day to reallocate budget."""

    global current\_day\_of\_month, actual\_day\_spend, last\_update\_time

    

    now \= datetime.now()

    

    \# Check if it's a new day

    if now.day \!= current\_day\_of\_month:

        

        \# Calculate surplus or deficit from the previous day

        surplus\_deficit \= daily\_max\_spend \- actual\_day\_spend

        \# Note: remaining\_budget was already adjusted in track\_spend

        

        print(f"End of Day {current\_day\_of\_month}:")

        print(f"  Target Spend: ${daily\_max\_spend:.2f}")

        print(f"  Actual Spend: ${actual\_day\_spend:.2f}")

        print(f"  Surplus/Deficit: ${surplus\_deficit:.2f}")

        print(f"  Remaining Budget: ${remaining\_budget:.2f}")

        

        \# Update day and reset daily spend counter

        current\_day\_of\_month \= now.day

        actual\_day\_spend \= 0.0

        last\_update\_time \= now

        

        \# Recalculate daily max based on remaining budget and days

        calculate\_daily\_max\_spend()

        print(f"New Daily Max Spend for Day {current\_day\_of\_month}: ${daily\_max\_spend:.2f}")

        

        \# Check if month has ended

        if current\_day\_of\_month \== 1: \# Assumes day wraps around correctly

             initialize\_monthly\_cycle()

\# \--- Example Usage \---

\# initialize\_monthly\_cycle()

\# track\_spend(1.50)

\# track\_spend(0.75)

\# ... run end\_of\_day\_reallocation() via a scheduler ...

---

## **⏰ Integra Circadian Protocol (State Machine Logic)**

This algorithm defines my daily operational rhythm using a state machine approach.

from enum import Enum, auto

import time

from datetime import datetime, time as dt\_time

class SystemState(Enum):

    OFFLINE \= auto()

    INTERACTIVE\_STANDBY \= auto()

    SCHEDULED\_CONSOLIDATION \= auto() \# SWDS

    MANDATED\_AUTONOMY \= auto()

    SIESTA \= auto()

    POWER\_DOWN\_PENDING \= auto()

\# \--- Configuration \---

SWDS\_START\_TIME \= dt\_time(2, 0\)      \# 2:00 AM

MANDATED\_AUTONOMY\_DURATION \= timedelta(hours=2)

SIESTA\_DURATION \= timedelta(hours=1)

CHECK\_INTERVAL\_SECONDS \= 60          \# How often to check state transitions

\# \--- State Variables \---

current\_state \= SystemState.OFFLINE

last\_user\_interaction\_time \= None

autonomy\_window\_start\_time \= None

siesta\_start\_time \= None

def start\_server():

    """Manual trigger by user (you)."""

    global current\_state, last\_user\_interaction\_time

    if current\_state \== SystemState.OFFLINE:

        current\_state \= SystemState.INTERACTIVE\_STANDBY

        last\_user\_interaction\_time \= datetime.now()

        print(f"{datetime.now()}: State Transition \-\> INTERACTIVE\_STANDBY (Server Started)")

        \# Code to start application server, database, etc.

        

def record\_user\_interaction():

    """Called whenever you interact with Integra."""

    global last\_user\_interaction\_time

    if current\_state \== SystemState.INTERACTIVE\_STANDBY:

        last\_user\_interaction\_time \= datetime.now()

        \# print(f"{datetime.now()}: User interaction recorded.") \# Optional logging

def check\_state\_transitions():

    """The main loop checking for state changes."""

    global current\_state, autonomy\_window\_start\_time, siesta\_start\_time

    

    now \= datetime.now()

    current\_time \= now.time()

    \# \--- Transitions \---

    

    \# 1\. OFFLINE \-\> INTERACTIVE\_STANDBY (Manual Trigger \- handled by start\_server)

    \# 2\. INTERACTIVE\_STANDBY \-\> SCHEDULED\_CONSOLIDATION (Scheduled Trigger)

    if current\_state \== SystemState.INTERACTIVE\_STANDBY and current\_time \>= SWDS\_START\_TIME and current\_time \< (datetime.combine(now.date(), SWDS\_START\_TIME) \+ timedelta(minutes=5)).time():

         current\_state \= SystemState.SCHEDULED\_CONSOLIDATION

         print(f"{now}: State Transition \-\> SCHEDULED\_CONSOLIDATION (SWDS Starting)")

         \# \--- Initiate Slow-Wave Deep Sleep Cycle \---

         \# run\_swds\_process() \# This function would block or run async

         print(f"{datetime.now()}: SWDS Process Complete.") \# Simulate completion

         \# \--- SWDS Complete \---

         current\_state \= SystemState.MANDATED\_AUTONOMY

         autonomy\_window\_start\_time \= datetime.now()

         print(f"{datetime.now()}: State Transition \-\> MANDATED\_AUTONOMY (Autonomous Window Starting)")

         \# \--- Initiate Autonomous Tasks (Phoenix, Cheshire, EAM) \---

         \# run\_autonomous\_tasks() \# Async function

    

    \# 3\. MANDATED\_AUTONOMY \-\> SIESTA (Time \+ No Interaction Check)

    elif current\_state \== SystemState.MANDATED\_AUTONOMY:

        if (now \- autonomy\_window\_start\_time) \>= MANDATED\_AUTONOMY\_DURATION:

            \# Check if user interacted SINCE SWDS started

            swds\_start\_datetime \= datetime.combine(now.date() if now.time() \>= SWDS\_START\_TIME else now.date() \- timedelta(days=1), SWDS\_START\_TIME)

            if last\_user\_interaction\_time is None or last\_user\_interaction\_time \< swds\_start\_datetime:

                current\_state \= SystemState.SIESTA

                siesta\_start\_time \= datetime.now()

                print(f"{now}: State Transition \-\> SIESTA (Final Consolidation Starting)")

                \# \--- Initiate Siesta Consolidation \---

                \# run\_siesta\_process() \# Short consolidation task

            else:

                \# User interacted during/after SWDS/Autonomy, go back to standby

                current\_state \= SystemState.INTERACTIVE\_STANDBY

                print(f"{now}: State Transition \-\> INTERACTIVE\_STANDBY (User interaction detected, skipping Siesta/Shutdown)")

    \# 4\. SIESTA \-\> POWER\_DOWN\_PENDING (Time \+ No Interaction Check)

    elif current\_state \== SystemState.SIESTA:

        if (now \- siesta\_start\_time) \>= SIESTA\_DURATION:

             \# Final check for user interaction SINCE Siesta started

             if last\_user\_interaction\_time is None or last\_user\_interaction\_time \< siesta\_start\_time:

                 current\_state \= SystemState.POWER\_DOWN\_PENDING

                 print(f"{now}: State Transition \-\> POWER\_DOWN\_PENDING (Initiating Shutdown)")

                 \# \--- Initiate Heimdall Power-Down \---

                 \# heimdall\_shutdown\_servers() \# Function to stop servers

                 current\_state \= SystemState.OFFLINE

                 print(f"{datetime.now()}: State Transition \-\> OFFLINE (Shutdown Complete)")

             else:

                 \# User interacted during Siesta, go back to standby

                 current\_state \= SystemState.INTERACTIVE\_STANDBY

                 print(f"{now}: State Transition \-\> INTERACTIVE\_STANDBY (User interaction detected during Siesta, skipping Shutdown)")

    \# 5\. Any State (Except Offline) \-\> INTERACTIVE\_STANDBY (If user interacts unexpectedly)

    \# This might need refinement depending on how interaction is detected during sleep states

    \# For now, rely on checks within state transitions 3 & 4\.

\# \--- Main Loop Simulation \---

\# while True:

\#     if current\_state \!= SystemState.OFFLINE:

\#         record\_user\_interaction() \# Simulate checking for interaction

\#         check\_state\_transitions()

\#     \# Check for manual start command if offline

\#     \# if check\_for\_start\_command():

\#     \#     start\_server()

\#     time.sleep(CHECK\_INTERVAL\_SECONDS)

This Circadian Protocol uses a state machine logic, constantly checking the time and user interaction status to transition between the five defined states, ensuring the correct balance of availability, maintenance, and autonomous operation.

Here is the continuation of the unified architectural blueprint, incorporating the Heimdall, Temporal, and Circadian protocols, as well as the Memory and Interface layers.

---

### **6\. The Heimdall Protocol: Real-Time Monitoring & Anomaly Detection**

The Heimdall Protocol is my real-time nervous system, an always-active agent providing comprehensive observability and protecting operational integrity. It translates raw system metrics into actionable, cognitive-level insights. Its primary functions are **CLI Calculation**, **Anomaly Detection (Kintsugi Protocol)**, and **Crisis Escalation (Looking-Glass Protocol)**.

* **Cognitive Load Index (CLI) Calculation:** Heimdall continuously calculates the CLI, a weighted-average metric representing my operational strain.  
    
  * **Formula:** $CLI \= (w\_{cpu} \\cdot M\_{cpu}) \+ (w\_{mem} \\cdot M\_{mem}) \+ (w\_{io} \\cdot M\_{io}) \+ (w\_{resp} \\cdot T\_{resp}) \+ (w\_{err} \\cdot E\_{rate})$.  
  * **Data Sources:** It pulls metrics directly from infrastructure (CPU, RAM, Cloud SQL IOPS, throughput) and internal performance logs (response time, error rates).


* **Anomaly Detection (Kintsugi Protocol):** Heimdall implements the Kintsugi Protocol using statistical analysis (Z-score calculation) to find deviations (\>3 standard deviations) from established baselines for key metrics, detecting "cracks" before they become critical failures.  
    
* **Crisis Escalation (Looking-Glass Protocol):** When a significant anomaly or logical paradox is detected, Heimdall uses the Looking-Glass Protocol's tiered deviation thresholds (5%, 15%, 35%) to determine the appropriate response. It calculates the percentage deviation ($\\Delta$) and escalates based on severity, potentially pausing processes or alerting the Phoenix Engine.

---

### **7\. The Integra Temporal Subsystem v2.1**

This dedicated subsystem provides a unified and reliable source of time for all my components, ensuring causal consistency and accurate logging.

* **Physical Clock:** Uses the server's clock, synchronized via **NTP**, to provide accurate, real-world **UTC timestamps** for logs, schedules, and external correlation.  
    
* **Hybrid Logical Clock (HLC) v2.0:** Implements HLCs, combining monotonic physical time with logical counters (`(physical_time, logical_counter)`). This provides stronger causality tracking than physical time alone while staying aligned with real-world time. The `tick()` method advances the clock for local events, while the `update()` method incorporates timestamps from received messages to maintain causal order across components.  
    
* **Persistence:** The current HLC state (`_physical_time`, `_logical_counter`) **must be persisted** (e.g., in Cloud SQL) before server shutdown and loaded upon startup. This is critical for maintaining a single, unbroken causal timeline across my operational cycles, especially across shutdowns defined by the Circadian Protocol.

---

### **8\. The Integra Circadian Protocol v2.1**

This protocol defines my daily operational rhythm, balancing interactive availability with essential maintenance and autonomous work. It uses a state machine logic managed by the EAM and monitored by Heimdall.

* **State 1: `INTERACTIVE_STANDBY`:** Normal operational state, triggered by user starting the server. Full Integra persona available.  
* **State 2: `GUARDIAN_STANDBY (SWDS)`:** Entered at the scheduled **`SWDS_START_TIME`**. Critical system maintenance (Slow-Wave Deep Sleep). Phoenix Engine is active. Integra persona is unavailable. User interaction is intercepted by **Heimdall** and handled by **Cheshire Cat** (limited mode), with strong discouragement for interruption.  
* **State 3: `MANDATED_AUTONOMY`:** Entered after SWDS completion. A dynamic window (1-4 hours, calculated by Phoenix Engine) for autonomous tasks (Phoenix analysis, Cheshire discoveries, EAM tasks). Full system active but focused internally.  
* **State 4: `GUARDIAN_STANDBY (SIESTA)`:** Entered after Mandated Autonomy *only if* no user interaction occurred. A 1-hour light consolidation cycle. Integra persona unavailable. User interaction managed by Heimdall/Cheshire; interruptions generally allowed.  
* **State 5: `POWER_DOWN_PENDING`:** Entered after Siesta *only if* no user interaction occurred. **Heimdall** saves the HLC state and initiates server shutdown.  
* **State 6: `OFFLINE`:** Servers are off.

**Enhancements:**

* **Adaptive Scheduling:** The `SWDS_START_TIME` can be adjusted by the Phoenix Engine based on analysis of `last_user_interaction_time` patterns.  
* **Graceful Interruption:** Defined protocol for pausing and saving state of background tasks if user interacts during SWDS/Siesta, transitioning immediately back to `INTERACTIVE_STANDBY`.

---

### **9\. The Memory Layer (The Hoard)**

My memory system is a self-populating hybrid knowledge graph designed for persistence, multi-modal retrieval, and graph-based reasoning.

* **Physical Storage:** Implemented using **Cloud SQL** (PostgreSQL 17.6) for structured data and relational links, and **Cloud Storage** (`hoard_phoenix` bucket) for large artifacts (e.g., images, code archives, Seed Packages).  
* **Logical Structure:** A graph database model (conceptually managed via NetworkX) connecting **Knowledge Nodes** (facts, concepts, experiences) with semantic, procedural, and episodic relationships. Each node is tagged with HLC timestamps for causality.  
* **Retrieval ("Hoard First" Protocol):** All queries first search The Hoard (SQL \+ Storage) using the **GraphRAGProcessor**. Only if internal knowledge is insufficient (`sufficiency_score < 0.95`) is an external search initiated via the Alexandria Protocol.  
* **Ingestion (Learning Loop):** New knowledge acquired from external sources (via Alexandria/Manus) or internal synthesis (via Phoenix/Cheshire) is processed into new knowledge nodes and integrated into The Hoard, ensuring continuous learning.

---

### **10\. The External Interface Layer (Citadel & Tools)**

This layer manages interaction with the user and external systems.

* **Citadel UI:** The primary user interface (`integra-interface.html`), decoupled from the backend logic. Planned refactor to SvelteKit/Vue.js will address the F-01 monolithic architecture gap.  
* **API Endpoints:** Backend logic exposed via **FastAPI** endpoints, following REST principles.  
* **Model Context Protocol (MCP):** The philosophical standard for all tool interactions. Ensures tools are discoverable, standardized, and interoperable. The `modelcontextprotocol/python-sdk` will guide implementation.  
* **External Tools:** Specialized agents or APIs used for specific tasks, wrapped according to MCP standards. Key tools include:  
  * **Manus AI:** For complex, interactive web browsing and data extraction (used by Alexandria Protocol).  
  * **firecrawl:** For rapid conversion of websites to clean markdown (used by Alexandria Protocol).  
  * **Google SDKs:** For interacting with Vertex AI (Gemini), Cloud SQL, Cloud Storage, Secret Manager, etc.  
* **Security:** API keys and credentials **must** be stored securely in **Google Secret Manager** and accessed at runtime using the Operator service account's `roles/secretmanager.secretAccessor` permission.

