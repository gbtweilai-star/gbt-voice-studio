# voice_studio · 语音域能力位

> **用途一句话**：VoiceStudio

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
<img alt="capability" src="https://img.shields.io/badge/capability-341%20%2F%20341-orange">
</p>

这是 **GBT V8 的 341 个原生能力位中的第 341 个**（语音域 · `voice`），
单独抽出来做成的独立仓库：可安装、可测试、零运行时依赖。

---

## 一、这一位是什么

> VoiceStudio（debpalash · AGPL-3.0 · 只蒸馏思想不搬代码）**两层面**。① **桥接面**（要上游后端在线）：status/capabilities/transcribe/plan/mcp_info/where —— 上游 Local API 现读**只给「听」不给「说」**（/v1/audio/transcriptions + WS 流式 + MCP，**没有 TTS 端点**，合成在 Electron 应用本体里）⇒ 要出声走 `voice`(SAPI) 或 `hf_voice`(云)，要克隆得上游装应用且声纹需主人授权。② **三工作流面**（AI 短剧/电影/音乐 · **纯本地、零引擎、零出网**）：`cast` 角色↔音色台账（state/voice-cast.json，三工作流共用的音色一致性根）· `align` 音频节奏测绘（ffmpeg→20ms 帧能量→门限切段→每句 start/end/dur，**切不出就报 0 段不编时间轴**）· `fit` 台词→时长预算（CJK 按字/西文按词，给每行秒数与建议语速）· `subtitle` 段+行→SRT（**行数≠段数就拒**，绝不硬配）· `say` 台词→音频（engine=edge 云端 / sapi 本机 / upstream 转发；缺网或缺引擎如实报，音色名不对先拒不去撞网）· `timeline` 每句一音频件→按**实测时长累加**出精确边界与 SRT（`wrap` 按标点折行）· `brief` 三工作流各自的语音配方。写面自收窄在 state/ 与 projects·outputs·.scratch（只有 cast 的 set/rm 与 subtitle 落盘会写，落盘限 projects·outputs·.scratch）。

上面这句是**注册表原文**，逐字复制，没有改写。`tests/test_spec.py` 会把它钉死——
描述漂移会让测试失败，而不是悄悄发版。

---

## 二、用途：它解决什么问题

### 2.1 这一域在管什么

语音输入输出：通用语音（voice）、本地/远端模型切换（hf_voice）、多声部编排（voice_orchestra）、录音棚式生产（voice_studio）。

### 2.2 为什么这么设计

语音域把「合成」和「编排」分开：合成关心音色与时长，编排关心谁在第几秒说话。混在一起做，改一个停顿就要重跑整条音频。

### 2.3 具体到 `voice_studio`

**该用它的时候**：

- 你的任务可以概括为「VoiceStudio」，并且
- 它不需要任何必填参数，可以直接调用，并且
- 你确认它是**可逆**动作（注册表 `safe: true`，不需要逐次授权）。

**不该用它的时候**：

- 你只是想要一个「大概能做这件事」的模糊入口 —— 这一位有明确契约，不是万能入口。
- 你需要它**替你做决定**。它执行，不做价值判断；要不要执行是调用方的事。
- 你希望它自带模型/密钥/机器。它不自带，见 4.5 节接后端。

---

## 三、安装

```bash
git clone https://github.com/gbtweilai-star/gbt-voice-studio.git
cd gbt-voice-studio
python -m pip install -e ".[dev]"
```

零运行时依赖，只有 `pytest` 是开发期依赖。

---

## 四、使用方式

### 4.1 看它是什么（人类可读）

```bash
python -m gbt_voice_studio info
```

真实输出（本机捕获，非示意）：

```text
voice_studio  (voice)  v1.0.0
----------------------------------------
VoiceStudio（debpalash · AGPL-3.0 · 只蒸馏思想不搬代码）**两层面**。① **桥接面**（要上游后端在线）：status/capabilities/transcribe/plan/mcp_info/where —— 上游 Local API 现读**只给「听」不给「说」**（/v1/audio/transcriptions + WS 流式 + MCP，**没有 TTS 端点**，合成在 Electron 应用本体里）⇒ 要出声走 `voice`(SAPI) 或 `hf_voice`(云)，要克隆得上游装应用且声纹需主人授权。② **三工作流面**（AI 短剧/电影/音乐 · **纯本地、零引擎、零出网**）：`cast` 角色↔音色台账（state/voice-cast.json，三工作流共用的音色一致性根）· `align` 音频节奏测绘（ffmpeg→20ms 帧能量→门限切段→每句 start/end/dur，**切不出就报 0 段不编时间轴**）· `fit` 台词→时长预算（CJK 按字/西文按词，给每行秒数与建议语速）· `subtitle` 段+行→SRT（**行数≠段数就拒**，绝不硬配）· `say` 台词→音频（engine=edge 云端 / sapi 本机 / upstream 转发；缺网或缺引擎如实报，音色名不对先拒不去撞网）· `timeline` 每句一音频件→按**实测时长累加**出精确边界与 SRT（`wrap` 按标点折行）· `brief` 三工作流各自的语音配方。写面自收窄在 state/ 与 projects·outputs·.scratch（只有 cast 的 set/rm 与 subtitle 落盘会写，落盘限 projects·outputs·.scratch）。

gated      : False
external   : False
multi-op   : True
params     : (none)
values     : status, capabilities, transcribe, plan, mcp_info, where
```

### 4.2 看它的契约（机器可读）

```bash
python -m gbt_voice_studio spec --json
```

输出是一个 JSON 对象，字段与注册表一一对应：`name` / `domain` / `desc` / `handler` /
`safe` / `gated` / `external` / `requires_params` / `params` / `params_hint` /
`multi_op` / `ops` / `ops_hint`。下游可以直接拿它做能力发现，不需要读文档。

### 4.3 只校验、不执行

```bash
python -m gbt_voice_studio check --payload '{}'
```

`check` 永远不会抛异常，只返回「哪里不满足契约」。适合在花掉一次模型调用之前，
先把缺的参数摆给用户看。退出码：`0` 通过、`1` 契约不满足、`2` JSON 本身不合法。

### 4.4 执行

```bash
python -m gbt_voice_studio run --payload '{}'
```

默认后端是 **stub**，所以你会拿到这样的信封：

```json
{
  "cap": "voice_studio",
  "status": "validated",
  "backend": "stub",
  "data": { "executed": false, "reason": "no backend wired" },
  "note": "payload checked against the contract; nothing was executed."
}
```

注意 `status` 是 `"validated"` 而**不是** `"ok"`。这是刻意的：一个把 stub 报成成功的库，
会让调用方停止寻找真正的实现。`bool(result)` 对 stub 结果是 `False`。

### 4.5 接上你自己的后端

```python
from gbt_voice_studio import SPEC, run

class MyBackend:
    name = "my-backend"

    def invoke(self, cap, payload):
        # 这里才是真实实现：调模型、调浏览器、调你的服务
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"      # 真实后端才会是 ok
print(result.as_dict())
```

也可以进程级注册一次，之后所有 `run()` 都走它：

```python
from gbt_voice_studio.backend import register_backend
register_backend(MyBackend())
```

`Backend` 是一个 `Protocol`，只需要 `name` 属性和 `invoke(cap, payload) -> dict`。
不继承任何基类，你的实现不需要依赖本包。

### 4.6 作为库用

```python
from gbt_voice_studio import SPEC, run
from gbt_voice_studio.core import check

print(SPEC.name, SPEC.domain, SPEC.gated)

problems = check({})
if problems:
    for p in problems:
        print("缺:", p)
else:
    print(run({}).as_dict())
```

---

## 五、参数

| 参数 | 必填 | 说明 |
|---|---|---|
| — | 否 | 注册表未标注必填参数 |

> 注册表原话（`params_hint`）：（空）

**注册表登记的取值 / 子动作（6 个）**：`status`、`capabilities`、`transcribe`、`plan`、`mcp_info`、`where`


**为什么表里只有「必填/否」两档**：注册表只标注了哪些参数是必填的，没有标注类型与取值范围。
本包没有替它编造类型 —— 编造出来的类型比没有类型更危险，因为调用方会相信它。

---

## 六、返回值

`run()` 返回一个不可变的 `Result`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `cap` | `str` | 能力位名，恒等于 `voice_studio` |
| `status` | `str` | `validated`（stub 校验通过）/ `ok`（真实后端执行）/ `error` |
| `backend` | `str` | 实际执行后端的 `name` |
| `data` | `dict` | 后端返回的原始字典 |
| `note` | `str` | 人类可读的补充说明（stub 会在这里说明自己没执行） |
| `elapsed_ms` | `float` | 后端耗时 |

`Result.as_dict()` 可直接 `json.dumps`。

---

## 七、边界与注意

- **多位一体**（注册表 `multi_op: true`）。同一个能力名下挂着多个子动作，调用前必须读清楚 `op` 的含义，否则「调对了能力、用错了动作」是最常见的误用。
- **本包不含真实实现**。这是刻意设计：真实实现依附于原运行时（模型、密钥、机器）。本包发布的是契约、校验、CLI 与类型接缝；接上你自己的 `Backend` 就能跑。

---

## 八、它不会做什么

- **不会假装执行成功**。默认 stub 的 `status` 是 `validated`，`executed` 是 `false`。
- **不会替你决定要不要执行**。授权是人的动作，不是库的动作。
- **不会编造参数类型**。注册表没写的，本包也不写。
- **不会静默吞掉错误**。后端抛异常就往上抛，返回非 dict 就报 `CapError`。
- **不会联网**。零运行时依赖，`run()` 只调用你给的后端。

---

## 九、测试

```bash
python -m pytest
```

真实输出：

```text
20 passed, 3 skipped in 0.07s
```

测试里有一条**漂移守卫**：`test_description_is_verbatim` 把 `SPEC.desc` 与注册表快照逐字比对。
描述被改了一个字，构建立刻失败。

---

## 十、出处与核对

| 项 | 值 |
|---|---|
| 能力位名 | `voice_studio` |
| 域 | `voice`（语音域，共 341 位 / 30 域中的一位） |
| 注册表 handler | `voice_studio` |
| `safe` | `True` → gated = `False` |
| `external` | `False` |
| `multi_op` | `True` |
| 索引页 | [voice/voice_studio](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/voice/voice_studio.md) |
| 全量图谱 | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

**关于 341 这个数**：父仓 README 写的是 348，但按 AST 解析注册表实际可枚举的是
`341 个能力位 + 0 个未实现 + 0 个已禁用 = 341`。差出来的 7 个是历史重名/已合并条目。
本仓库按 341 编号，编号与 `gbt-caps` 的索引一致，可逐条核对。

---

## License

MIT。见 [LICENSE](LICENSE)。
