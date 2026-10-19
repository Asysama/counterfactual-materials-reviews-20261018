# PR 715 generator review

Decision: PASS
Reviewed head: 5b7b1eb2f4b9cda3e66b8d040a9473e0e18de280
Generator: adhesive_tape_peel_angle_order_reversal
Generator correctness: PASS
Runtime-provenance policy scope: NEW
Runtime provenance: PASS
Declared scaling target: 100000 accepted cases
Smaller-target rationale: not applicable
Declared-target scale readiness: PASS
Production readiness: PRODUCTION READY within the declared reduced-model contract; human approval pending

## Blocking findings

None found within the completed self-check scope. User and Sara approval remain separate.

## Six-gate result

| Gate | Result | Evidence |
|---|---|---|
| Output contract | PASS | Two complete native 2048², 24fps, 120-frame, five-second cases; four H264 streams each, independently decoded |
| Violating-object-only mask | PASS | Strict RGB binary masks, flat reviewer-selected object identity replay, no shadows; exact native off-mask overlay equality |
| Real scaling | PASS | 100000 static profiles, six controlled axes, 16 coupled boundary profiles, two visibly distinct complete cases |
| Official unpatched environment | PASS | Released pinned bpy/numpy/Pillow/imageio-ffmpeg/scipy; actual successful runtime witnesses and renderer component records |
| Decoded matched control | PASS | Exact RGB prefix before intervention and first difference recomputed from final MP4 |
| Semantic consistency | PASS | Standalone prompts, one registered operator, independent mechanics and full-clip visual inspection |

## Production-quality behavioral baseline

True completes its normal prompt outcome; Counterfactual has one declared constitutive/constraint violation and coherent downstream behavior. Matching nuisance parameters, force/displacement commands and camera remain shared. Outcome, visible contact, support continuity, complete observation tail, native edge quality and prompt alignment: PASS. Source labels are never used as proof of branch correctness; external mechanics and decoded evidence are retained.

## Timebase

Source/outer interval 1/24 second, 24 fps, source seconds per video second 1. All models are explicit analytical/reduced mechanics. Internal subdivision is separately recorded; no accidental playback scaling. The fixed 0–40 N gauges display the actual matched force. Smooth 24-frame loading and unloading ramps keep needle motion continuous. Both tapes peel before intervention; only the low-angle interface response is modified after that time.

## Semantic matrix

Directory, title, README/DESIGN, both prompts, scoring, registered operator, trajectory and rendered behavior have been compared for this exact head. Status: PASS. Concrete assumptions are in evidence/model-scope.md; actual prompts are stored independently with each case. No simulator-native claim is made.

## Runtime and reproduction

Clean exact source is bound by successful-render witness, accepted-case index, requirements hash, actual Python/package inventory, Blender/device/encoder component records and every delivered artifact checksum. These are contemporaneous witnesses, not inferred reproduction recipes. Seed42 was independently regenerated in the same official environment; all four native streams were compared with exact mask equality and RGB tolerance below 0.1/255 mean and 0.5/255 maximum frame mean. Safe matching resume and incompatible-render resume rejection were tested.

## Scale readiness

100000 static profiles accepted with unique effective signatures and full bucket coverage; eight representative shard streams are disjoint. Controlled low/high axis probes show changes in actual geometry/dynamics/timing and decoded pixels, with appearance and viewpoint as additional nuisance diversity. 16 combined physical corners pass independent mechanics. Formal seeds42/98 exercise different combinations of all six buckets. This does not claim 100000 rendered cases or a 40-case batch.

## Client-facing artifacts

Binary masks are shown white on black. Native overlays replace only target mask pixels with red. Browser RGB and overlay derivatives are explicitly labeled lossy1024 copies; they are not authoritative pixel-audit evidence. Native2048 originals are separately published by exact head/case/stream and SHA256. Hosted playback/seek and anonymous HTTP access: PASS.

## Accepted cases

[
  {
    "case_id": "adhesive_tape_peel_angle_order_reversal_00000042",
    "seed": 42,
    "intervention": 52,
    "first_changed": 52,
    "evidence": 73
  },
  {
    "case_id": "adhesive_tape_peel_angle_order_reversal_00000098",
    "seed": 98,
    "intervention": 56,
    "first_changed": 56,
    "evidence": 75
  }
]

## Commands and evidence

See evidence/runtime-witness.json for the exact command and successful runtime; evidence/independent-audit.json and the included external audit source for non-self-grading checks; evidence/identity-audit.json for independently named visible-object masks; evidence/scale.json and axis-probes.json for scale coverage. All packet files are bound by packet-manifest.json. Source PR: https://github.com/hipo-dev/counterfactual-data/pull/715. Review URL: https://asysama.github.io/counterfactual-materials-reviews-20261018/adhesive_tape_peel_angle_order_reversal/5b7b1eb2f4b9cda3e66b8d040a9473e0e18de280/index.html.

## Delivery status

Contributor self-check only. No Sara form has been filled or submitted. User approval is pending. Any source-head change invalidates this packet until affected evidence is regenerated and checked again.

## User feedback addressed in this revision

每段视频左侧是高角度，右侧是低角度。正常组两条胶带都被拉开：高角度沿底板剥得更多，低角度也有清楚可见的剥离。反事实组先正常剥离，随后低角度侧加快，最终剥离距离反而超过高角度。两只相同的 0–40 N 测力表始终同步，表示两侧拉力相同；卸载后都停止剥离。看底板刻度和胶带与底板的交界处，不要只比较夹头高度。

The earlier packet remains retained; the current decision applies only to the exact source and rendered evidence above.
