"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "voice_studio",
 "domain": "voice",
 "desc": "VoiceStudio（debpalash · AGPL-3.0 · 只蒸馏思想不搬代码）**两层面**。① **桥接面**（要上游后端在线）：status/capabilities/transcribe/plan/mcp_info/where —— 上游 Local API 现读**只给「听」不给「说」**（/v1/audio/transcriptions + WS 流式 + MCP，**没有 TTS 端点**，合成在 Electron 应用本体里）⇒ 要出声走 `voice`(SAPI) 或 `hf_voice`(云)，要克隆得上游装应用且声纹需主人授权。② **三工作流面**（AI 短剧/电影/音乐 · **纯本地、零引擎、零出网**）：`cast` 角色↔音色台账（state/voice-cast.json，三工作流共用的音色一致性根）· `align` 音频节奏测绘（ffmpeg→20ms 帧能量→门限切段→每句 start/end/dur，**切不出就报 0 段不编时间轴**）· `fit` 台词→时长预算（CJK 按字/西文按词，给每行秒数与建议语速）· `subtitle` 段+行→SRT（**行数≠段数就拒**，绝不硬配）· `say` 台词→音频（engine=edge 云端 / sapi 本机 / upstream 转发；缺网或缺引擎如实报，音色名不对先拒不去撞网）· `timeline` 每句一音频件→按**实测时长累加**出精确边界与 SRT（`wrap` 按标点折行）· `brief` 三工作流各自的语音配方。写面自收窄在 state/ 与 projects·outputs·.scratch（只有 cast 的 set/rm 与 subtitle 落盘会写，落盘限 projects·outputs·.scratch）。",
 "handler": "voice_studio",
 "safe": true,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "status",
  "capabilities",
  "transcribe",
  "plan",
  "mcp_info",
  "where"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
