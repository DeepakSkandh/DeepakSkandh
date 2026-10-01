<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/header-light.svg">
  <img alt="Deepak Skandh. AI × Systems × Engineering. Every abstraction is a promise. I read the fine print." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/header-dark.svg" width="100%">
</picture>

<br><br>

<img alt="A terminal session: whoami prints deepak skandh, then underneath --list maps each abstraction to what lies beneath it." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/terminal.svg" width="86%">

<p>
  <img src="./assets_old/data-code.gif" width="420">
</p>

<br><br>

<a href="#mindset"><kbd>&nbsp;mindset&nbsp;</kbd></a>&nbsp;
<a href="#interests"><kbd>&nbsp;interests&nbsp;</kbd></a>&nbsp;
<a href="#learning"><kbd>&nbsp;learning&nbsp;</kbd></a>&nbsp;
<a href="#from-scratch"><kbd>&nbsp;from scratch&nbsp;</kbd></a>&nbsp;
<a href="#philosophy"><kbd>&nbsp;philosophy&nbsp;</kbd></a>&nbsp;
<a href="#stack"><kbd>&nbsp;stack&nbsp;</kbd></a>&nbsp;
<a href="#exploring"><kbd>&nbsp;exploring&nbsp;</kbd></a>&nbsp;
<a href="#activity"><kbd>&nbsp;activity&nbsp;</kbd></a>&nbsp;
<a href="#connect"><kbd>&nbsp;connect&nbsp;</kbd></a>

</div>

<br>

## `~/mindset`

> [!IMPORTANT]
> **Don't just use the abstraction. Understand what's underneath it.**

Most of what I learn starts with a question an abstraction politely refuses to answer. Why is this query slow? Where does this tensor actually live? What happens between a request arriving and a response leaving? Every abstraction leaks eventually,[^leaky] and when it does, I want to already know what's underneath.

| when I use | I want to understand |
| :-- | :-- |
| a framework | its implementation |
| an API | the protocol beneath it |
| a database | its query engine |
| a model | its architecture, and how it is optimized |
| a library | the algorithm inside |
| any abstraction | the system it hides |

### one line, all the way down

<sub>Open a line to follow it through the layers.</sub>

<details>
<summary><code>SELECT name FROM users WHERE id = 42;</code></summary>
<br>

```mermaid
sequenceDiagram
    autonumber
    participant C as client
    participant P as parser
    participant O as planner + optimizer
    participant E as executor
    participant B as buffer pool
    participant D as disk
    C->>P: SELECT name FROM users WHERE id = 42
    P->>O: syntax tree
    O->>O: index scan or sequential scan?
    O->>E: physical plan (index scan on users_pkey)
    E->>B: B+ tree pages for id = 42
    alt page already in memory
        B-->>E: page
    else cache miss
        B->>D: read page
        D-->>B: page
        B-->>E: page
    end
    E-->>C: (1 row)
```

</details>

<details>
<summary><code>loss.backward()</code></summary>
<br>

Reverse-mode autodiff walks the computation graph backwards and multiplies local derivatives along the way:

$$
\frac{\partial \mathcal{L}}{\partial \theta} = \frac{\partial \mathcal{L}}{\partial y} \cdot \frac{\partial y}{\partial h} \cdot \frac{\partial h}{\partial \theta}
$$

```text
loss.backward()
 └─ traverse the autograd graph in reverse topological order
    └─ each op's backward() applies its local derivative
       └─ gradients accumulate into every leaf tensor's .grad
          └─ kernels launch on the GPU
             └─ often limited by memory bandwidth, not FLOPs
```

</details>

<details>
<summary><code>softmax(QKᵀ / √dₖ) V</code></summary>
<br>

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V
$$

For a sequence of length $n$, the score matrix $QK^{\top}$ is $n \times n$, so naive attention costs $O(n^2 d)$ time and $O(n^2)$ memory. FlashAttention computes the exact same result in tiles that never write the full matrix to GPU memory, which is one reason long context windows became practical.

</details>

<details>
<summary><code>printf("hello\n");</code></summary>
<br>

```text
printf("hello\n");
 └─ formatted into a user-space stdio buffer
    └─ the newline flushes it: write(1, "hello\n", 6)
       └─ system call traps into the kernel
          └─ file descriptor 1 → tty driver
             └─ characters on a terminal
```

</details>

<br>

## `~/interests`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/interests-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/interests-light.svg">
  <img alt="Intelligence (why does it generalize?): artificial intelligence, machine learning, deep learning, LLMs and generative AI, NLP, computer vision. Systems (where does the time go?): backend engineering, database systems, distributed systems, HPC, systems engineering, automation. Foundations (what does it cost?): algorithms, data structures, competitive programming, probability, statistics. Science (what does the data say?): data science, computational biology, research, experimentation." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/interests-dark.svg" width="100%">
</picture>

<br>

## `~/learning`

> [!NOTE]
> Every branch is open and nothing is merged. This is a record of direction, not a list of things I've finished.

```mermaid
%%{init: {'theme': 'base', 'gitGraph': {'mainBranchName': 'fundamentals', 'showCommitLabel': true}, 'themeVariables': {'git0': '#8b949e', 'git1': '#22a6c7', 'git2': '#6d8cf5', 'git3': '#8b5cf6', 'git4': '#e0952f', 'gitBranchLabel0': '#ffffff', 'gitBranchLabel1': '#ffffff', 'gitBranchLabel2': '#ffffff', 'gitBranchLabel3': '#ffffff', 'gitBranchLabel4': '#ffffff', 'commitLabelColor': '#ffffff', 'commitLabelBackground': '#59636e', 'commitLabelFontSize': '11px'}}}%%
gitGraph
    commit id: "start"
    branch algorithms
    commit id: "data structures"
    commit id: "algorithms"
    commit id: "problem solving"
    commit id: "competitive programming" type: HIGHLIGHT
    checkout fundamentals
    branch systems
    commit id: "c++"
    commit id: "operating systems"
    commit id: "networks"
    commit id: "database internals"
    commit id: "systems programming" type: HIGHLIGHT
    checkout fundamentals
    branch ai
    commit id: "deep learning"
    commit id: "transformers"
    commit id: "llms"
    commit id: "nlp"
    commit id: "computer vision"
    commit id: "ml engineering" type: HIGHLIGHT
    checkout fundamentals
    branch mathematics
    commit id: "probability"
    commit id: "statistics"
    commit id: "linear algebra"
    commit id: "optimization" type: HIGHLIGHT
```

<br>

## `~/from-scratch`

Things I want to build from scratch, because building something is the fastest way to find out what I didn't understand about it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/pipeline-light.svg">
  <img alt="minidb, a database engine built one layer at a time: parser, query planner, optimizer, execution engine, storage engine, indexes, transactions, concurrency control, recovery." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/pipeline-dark.svg" width="100%">
</picture>

### the build list

<sub>Each box gets checked and linked to its repo when it ships.</sub>

- [ ] **minidb**: a database engine, from the parser down to crash recovery
- [ ] **autograd engine**: to see how backprop actually flows
- [ ] **transformer, no libraries**: to see what attention is really computing
- [ ] **memory allocator**: to see what `malloc` hides
- [ ] **HTTP server on raw sockets**: to see what a framework does per request
- [ ] **LSM-tree key-value store**: to see why writes are cheap and reads aren't
- [ ] **Raft**: to see how machines agree
- [ ] **thread pool**: to see what concurrency costs

### rules of engagement

```diff
- consume the system
+ build the system

- memorize the API
+ understand the implementation

- assume it's fast
+ benchmark it

- guess
+ debug

- stop at "it works"
+ ask why it works
```

<br>

## `~/philosophy`

```mermaid
flowchart LR
    learn([learn]) --> build([build]) --> brk([break]) --> debug([debug]) --> understand([understand]) --> rebuild([rebuild]) --> ship([ship])
    ship -. next problem .-> learn
    classDef surface stroke:#22a6c7,stroke-width:1.5px
    classDef middle stroke:#8b5cf6,stroke-width:1.5px
    classDef core stroke:#e0952f,stroke-width:1.5px
    class learn,build surface
    class brk,debug,understand middle
    class rebuild,ship core
```

> **Understand** before abstracting.
>
> **Measure** before optimizing.
>
> **Build** before overengineering.
>
> **Read the source** when the abstraction stops making sense.

<br>

## `~/stack`

| layer | tools |
| :-- | :-- |
| **languages** | <img src="https://skillicons.dev/icons?i=python,cpp,c,java&theme=dark" height="34" alt="Python, C++, C, Java"> &nbsp; `SQL` `MATLAB` |
| **ai / ml** | <img src="https://skillicons.dev/icons?i=pytorch,tensorflow,sklearn,opencv&theme=dark" height="34" alt="PyTorch, TensorFlow, scikit-learn, OpenCV"> &nbsp; `Keras` `Hugging Face` |
| **data** | `NumPy` `Pandas` `SciPy` `Matplotlib` `Seaborn` `RDKit` |
| **databases** | <img src="https://skillicons.dev/icons?i=postgres,mysql,sqlite&theme=dark" height="34" alt="PostgreSQL, MySQL, SQLite"> |
| **tooling** | <img src="https://skillicons.dev/icons?i=linux,git,github,vscode&theme=dark" height="34" alt="Linux, Git, GitHub, VS Code"> |

<br>

## `~/exploring`

```text
$ ps -eo pid,stat,cmd --sort=curiosity

  PID  STAT  CMD
  101  R     cpp-systems          --memory-model --performance
  102  R     database-internals   --storage --query-execution
  103  R     distributed-systems  --consensus --replication
  104  R     llm-engineering      --inference --evaluation
  105  R     competitive-prog     --contests --upsolving
  106  R     backend-engineering  --apis --concurrency
  107  R     hpc                  --parallelism --cache-locality
  108  R     ml-systems           --training --serving
```

<br>

## `~/activity`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/generated/stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/generated/stats-light.svg">
  <img alt="GitHub activity over the past year: contributions, streaks, public repositories, weekly activity and languages." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/generated/stats-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/generated/snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/generated/snake-light.svg">
  <img alt="A snake eating the contribution graph." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/generated/snake-dark.svg" width="100%">
</picture>

### `~/log`

<sub>Recent public activity, rewritten daily by a workflow in this repo.</sub>

<!-- LOG:START -->
```text
$ git log --author="DeepakSkandh" --all --oneline -n 8
  (waiting for the first sync)
```
<!-- LOG:END -->

<br>

## `~/connect`

<div align="center">

<a href="https://github.com/DeepakSkandh"><kbd>&nbsp;github&nbsp;</kbd></a>&nbsp;
<a href="mailto:deepakskandh"><kbd>&nbsp;email&nbsp;</kbd></a>&nbsp;


<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/footer-light.svg">
  <img alt="still compiling." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/footer-dark.svg" width="100%">
</picture>

<img src="https://komarev.com/ghpvc/?username=DeepakSkandh&style=flat-square&color=6d8cf5&label=visitors" alt="profile visitors">

</div>

[^leaky]: Joel Spolsky named this the Law of Leaky Abstractions in 2002: every non-trivial abstraction eventually exposes some of the detail it was built to hide.
