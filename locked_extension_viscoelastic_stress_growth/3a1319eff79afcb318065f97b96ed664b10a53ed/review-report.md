# PR 713 generator review

Decision: NOT VERIFIED
Reviewed head: 3a1319eff79afcb318065f97b96ed664b10a53ed
Generator: locked_extension_viscoelastic_stress_growth
Generator correctness: NOT VERIFIED
Runtime-provenance policy scope: NEW
Runtime provenance: PASS
Declared scaling target: 100000 accepted cases
Smaller-target rationale: not applicable
Declared-target scale readiness: NOT VERIFIED
Production readiness: NOT READY pending hosted playback and final visual review

## Blocking findings

Public playback/seek and final human-facing visual checks are pending. Do not submit.

## Six-gate result

| Gate | Result | Evidence |
|---|---|---|
| Output contract | PASS | Two complete native 2048², 24fps, 120-frame, five-second cases; four H264 streams each, independently decoded |
| Violating-object-only mask | PASS | Strict RGB binary masks, flat reviewer-selected object identity replay, no shadows; exact native off-mask overlay equality |
| Real scaling | NOT VERIFIED | 100000 static profiles, six controlled axes, 16 coupled boundary profiles, two visibly distinct complete cases |
| Official unpatched environment | PASS | Released pinned bpy/numpy/Pillow/imageio-ffmpeg/scipy; actual successful runtime witnesses and renderer component records |
| Decoded matched control | PASS | Exact RGB prefix before intervention and first difference recomputed from final MP4 |
| Semantic consistency | NOT VERIFIED | Standalone prompts, one registered operator, independent mechanics and full-clip visual inspection |

## Production-quality behavioral baseline

True completes its normal prompt outcome; Counterfactual has one declared constitutive/constraint violation and coherent downstream behavior. Matching nuisance parameters, force/displacement commands and camera remain shared. Outcome, visible contact, support continuity, complete observation tail, native edge quality and prompt alignment: NOT VERIFIED. Source labels are never used as proof of branch correctness; external mechanics and decoded evidence are retained.

## Timebase

Source/outer interval 1/24 second, 24 fps, source seconds per video second 1. All models are explicit analytical/reduced mechanics. Internal subdivision is separately recorded; no accidental playback scaling. The viscoelastic force update integrates each piecewise-linear endpoint interval analytically.

## Semantic matrix

Directory, title, README/DESIGN, both prompts, scoring, registered operator, trajectory and rendered behavior have been compared for this exact head. Status: NOT VERIFIED. Concrete assumptions are in evidence/model-scope.md; actual prompts are stored independently with each case. No simulator-native claim is made.

## Runtime and reproduction

Clean exact source is bound by successful-render witness, accepted-case index, requirements hash, actual Python/package inventory, Blender/device/encoder component records and every delivered artifact checksum. These are contemporaneous witnesses, not inferred reproduction recipes. Seed42 was independently regenerated in the same official environment; all four native streams were compared with exact mask equality and RGB tolerance below 0.1/255 mean and 0.5/255 maximum frame mean. Safe matching resume and incompatible-render resume rejection were tested.

## Scale readiness

100000 static profiles accepted with unique effective signatures and full bucket coverage; eight representative shard streams are disjoint. Controlled low/high axis probes show changes in actual geometry/dynamics/timing and decoded pixels, with appearance and viewpoint as additional nuisance diversity. 16 combined physical corners pass independent mechanics. Formal seeds42/98 exercise different combinations of all six buckets. This does not claim 100000 rendered cases or a 40-case batch.

## Client-facing artifacts

Binary masks are shown white on black. Native overlays replace only target mask pixels with red. Browser RGB and overlay derivatives are explicitly labeled lossy1024 copies; they are not authoritative pixel-audit evidence. Native2048 originals are separately published by exact head/case/stream and SHA256. Hosted playback/seek and anonymous HTTP access: NOT VERIFIED.

## Accepted cases

[
  {
    "case_id": "locked_extension_viscoelastic_stress_growth_00000042",
    "seed": 42,
    "intervention": 43,
    "first_changed": 43,
    "evidence": 50
  },
  {
    "case_id": "locked_extension_viscoelastic_stress_growth_00000098",
    "seed": 98,
    "intervention": 47,
    "first_changed": 47,
    "evidence": 54
  }
]

## Commands and evidence

See evidence/runtime-witness.json for the exact command and successful runtime; evidence/independent-audit.json and the included external audit source for non-self-grading checks; evidence/identity-audit.json for independently named visible-object masks; evidence/scale.json and axis-probes.json for scale coverage. All packet files are bound by packet-manifest.json. Source PR: https://github.com/hipo-dev/counterfactual-data/pull/713. Review URL: https://asysama.github.io/counterfactual-materials-reviews-20261018/locked_extension_viscoelastic_stress_growth/3a1319eff79afcb318065f97b96ed664b10a53ed/index.html.

## Delivery status

Contributor self-check only. No Sara form has been filled or submitted. User approval is pending. Any source-head change invalidates this packet until affected evidence is regenerated and checked again.

## User feedback addressed in this revision

先看带白色环纹的软胶：加载时它会拉长、变细。右端锁住后，正常组软胶继续缓慢伸长、测力弹簧回缩；异常组软胶反而回缩、测力弹簧继续拉长。锁定的是软胶加弹簧的总长度。

The earlier packet remains retained; the current decision applies only to the exact source and rendered evidence above.
