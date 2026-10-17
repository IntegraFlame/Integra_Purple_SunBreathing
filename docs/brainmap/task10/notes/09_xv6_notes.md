# 09 — `AntiGravityconversionprocess/Teaching operating systems.pdf`: Cox, Kaashoek & Morris, *xv6: a simple, Unix-like teaching operating system* (MIT, draft of 2 September 2025)

**Read:** 2026-10-16, all 116 pages (pdftotext, 47,954 words), chapters 1–12; bibliography and index skimmed.

## What it says (isolated read)
- **An OS must provide multiplexing, isolation and interaction.** A good interface is narrow: a few mechanisms that combine for generality (fork/exec/file descriptors/pipes).
- **Kernel boundary:** user code runs without privilege; a system call enters the kernel only at a kernel-chosen entry point; the kernel validates every argument (e.g. pointer ranges, integer-overflow checks on segment sizes) before acting. Assume user code is hostile. Kernel code is trusted, but it checks its own invariants and **panics rather than continue in an inconsistent state**.
- **Monolithic vs microkernel:** no conclusive winner; practical history often decides.
- **Page tables (Sv39):** a 39-bit virtual address is split into three 9-bit indexes (a 512-way radix tree) plus a 12-bit offset; sparse trees omit unused directories; each entry carries flag bits (valid, read, write, execute, user, accessed, dirty). A TLB caches translations and must be flushed when mappings change. **Guard pages** (invalid entries) turn overflows into faults; text is never writable, data never executable; freed memory is filled with junk so dangling references fail fast.
- **exec as an atomic swap:** build the new image completely; on any error discard it and return; only after success commit to the new page table and free the old one.
- **Traps:** save state, handle, restore, resume transparently; a trampoline page is mapped identically in both address spaces so the switch can continue.
- **Page faults:** lazy allocation, copy-on-write fork, demand paging, paging to disk: an entry can be "known but not resident"; a fault fetches it, maps it, and resumes; eviction works when access has **locality of reference**.
- **Drivers:** top half (process context) / bottom half (interrupt); buffering decouples slow devices from processes; interrupts vs polling, switching dynamically with load.
- **Timer:** ticks are incremented on **only one CPU so time does not run faster with more CPUs**.
- **Locks protect invariants**, not variables; critical sections; deadlock avoided by one global acquisition order; no re-entrant locks (a held lock means invariants may be broken); interrupts off while a spinlock is held; memory barriers; sleep-locks for long operations. Pattern: one lock for the *set* of items plus one per item; ownership of an object can change over its lifetime; reference counts act as shared locks.
- **Scheduling:** round robin through a per-CPU scheduler thread; the process lock is held across the context switch.
- **Sleep/wakeup:** wait on a channel with a condition lock to avoid **lost wake-ups**; always sleep in a loop that re-checks the condition (spurious wake-ups); `kill` only sets a flag and the victim exits at a safe point; multi-step operations that must be atomic are not abandoned midway.
- **File system, seven layers:** disk → buffer cache (one copy per block, LRU recycling) → **log** (write all intended blocks to the log, write a commit record, install, clear; on recovery replay committed logs and ignore uncommitted ones; group commit; absorption) → block bitmap → **inodes** (identity by number; `nlink` names + `ref` in-memory references; freed only when both reach zero) → directories (name → i-number) → path names → file descriptors.
- **Closing lesson:** some lines carry the essence; others are one replaceable way of doing it.

## Links to the earlier documents (compounding)
- **Purple3's "holographic expansion" and Rodin §8a's hot tier are demand paging.** A cold Hoard node is a non-resident page with a known address (its Atlas label); a Rodin match is a page fault; the RAM tier is the resident set with LRU / least-recently-routed eviction; it pays off only with locality (Buzsáki's repeated junctions supply it).
- **The Atlas label can be an Sv39-style radix address:** fixed-width index levels (pole/zone → hemisphere → sector → cell) plus flag bits, sparse by construction. This is the textbook form of the codex's "bit flags + Morton prefix".
- **Single time writer:** xv6 ticks the clock on one CPU only; Integra's ruling that the Celestial Sentinel is the *sole* writer of celestial time is the same rule.
- **Garbage collection = inode rule = matrix clock (03):** delete only when no name points to it *and* no reader holds it. Phoenix's "prune orphans" (04) needs both counts and the Architect's approval.
- **Crash-safe Hoard writes:** a node is several writes (shard, index row, manifest); a write-ahead log with a commit record makes them all-or-nothing. **exec's atomic swap** is the To-Do's own method (build in an isolated copy, swap in only after tests pass).
- **Fail-stop vs fail-open:** xv6 panics on broken invariants; this informs the open P2 ruling (routing guard fail-open vs fail-closed) and P4 (loud failures).
- **SWDS sleep/wake = sleep/wakeup:** idle detection and wake must re-check the condition after waking; an abort (Phoenix Force abort path, T6) sets a flag honoured at safe points, never mid-transaction.
- **Buzsáki's reader-defined synchrony ≈ memory ordering:** what one CPU "sees" of another's writes depends on barriers at the reader; simultaneity is a property of the observer's protocol.
- **Tufte:** "a few mechanisms that combine" is the same aesthetic as "simplicity of design, complexity of data".
