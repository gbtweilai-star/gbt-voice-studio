# voice_studio

**One capability bit from GBT V8, packaged standalone.** No. 341 of 341,
`voice` domain (Voice).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> VoiceStudio（debpalash · AGPL-3.0 · 只蒸馏思想不搬代码）**两层面**。① **桥接面**（要上游后端在线）：status/capabilities/transcribe/plan/mcp_info/where —— 上游 Local API 现读**只给「听」不给「说」**（/v1/audio/transcriptions + WS 流式 + MCP，**没有 TTS 端点**，合成在 Electron 应用本体里）⇒ 要出声走 `voice`(SAPI) 或 `hf_voice`(云)，要克隆得上游装应用且声纹需主人授权。② **三工作流面**（AI 短剧/电影/音乐 · **纯本地、零引擎、零出网**）：`cast` 角色↔音色台账（state/voice-cast.json，三工作流共用的音色一致性根）· `align` 音频节奏测绘（ffmpeg→20ms 帧能量→门限切段→每句 start/end/dur，**切不出就报 0 段不编时间轴**）· `fit` 台词→时长预算（CJK 按字/西文按词，给每行秒数与建议语速）· `subtitle` 段+行→SRT（**行数≠段数就拒**，绝不硬配）· `say` 台词→音频（engine=edge 云端 / sapi 本机 / upstream 转发；缺网或缺引擎如实报，音色名不对先拒不去撞网）· `timeline` 每句一音频件→按**实测时长累加**出精确边界与 SRT（`wrap` 按标点折行）· `brief` 三工作流各自的语音配方。写面自收窄在 state/ 与 projects·outputs·.scratch（只有 cast 的 set/rm 与 subtitle 落盘会写，落盘限 projects·outputs·.scratch）。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-voice-studio.git
cd gbt-voice-studio
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_voice_studio info                  # capability card
python -m gbt_voice_studio spec --json           # machine-readable contract
python -m gbt_voice_studio check --payload '{}'
python -m gbt_voice_studio run   --payload '{}'
```

Real `info` output from this machine:

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

Wire a real implementation:

```python
from gbt_voice_studio import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（6 个）**：`status`、`capabilities`、`transcribe`、`plan`、`mcp_info`、`where`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Not gated: the registry marks this bit `safe: true`.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.07s
```

## Provenance

| field | value |
|---|---|
| capability | `voice_studio` |
| domain | `voice` |
| handler | `voice_studio` |
| safe | `True` (gated = `False`) |
| external | `False` |
| atlas page | [voice/voice_studio](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/voice/voice_studio.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
