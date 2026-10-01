<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/header-light.svg">
  <img alt="Deepak Skandh. AI × Systems × Engineering. Not done yet." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/header-dark.svg" width="100%">
</picture>

<br><br>

<img alt="A terminal session: whoami prints deepak skandh, then underneath --list maps each abstraction to what lies beneath it." src="https://raw.githubusercontent.com/DeepakSkandh/DeepakSkandh/main/assets/terminal.svg" width="86%">

<p>
  <img src="./assets_old/data-code.gif" width="420">
</p>

<br><br>


<a href="#interests"><kbd>&nbsp;interests&nbsp;</kbd></a>&nbsp;
<a href="#exploring"><kbd>&nbsp;exploring&nbsp;</kbd></a>&nbsp;
<a href="#activity"><kbd>&nbsp;activity&nbsp;</kbd></a>&nbsp;
<a href="#connect"><kbd>&nbsp;connect&nbsp;</kbd></a>

</div>



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
  2026-10-01  push     diabetic-retinopathy-feat…  main
  2026-09-30  push     diabetic-retinopathy-feat…  main
  2026-09-24  push     amazon-ml-hackathon-2026    main
  2026-09-23  push     diabetic-retinopathy-feat…  main
  2026-09-22  push     diabetic-retinopathy-feat…  main
  2026-09-18  push     flask                       main
  2026-09-16  issue    Nithinsaim/Digital-Rheolo…  #1 opened
  2026-09-16  star     DS-AI-GATE/dsai-gate        starred
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
