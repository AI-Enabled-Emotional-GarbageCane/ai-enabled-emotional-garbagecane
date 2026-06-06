# 2026-06-04-vision-agx-l515-model-records

## Metadata

| Field | Value |
|---|---|
| Date | 2026-06-04 |
| Author / Agent | Codex |
| Related repo(s) | `firmware`, `vision`, `ai-enabled-emotional-garbagecane` |
| Contract version | v0.3 |
| Status | implemented |

## Goal

Run AGX + Intel RealSense L515 firmware/vision integration, record the model behavior, and create a durable record for all curated vision model exports without changing the public v0.3 queue contract.

## Scope

In scope:

- L515 depth trigger from `firmware` via `q_detected` / `user_detected`.
- L515 RGB capture and ONNX model inference in `vision`.
- `recognition_result` payload emission into `q_result`.
- Vision model export documentation and AGX L515 candy-wrapper observation.
- Harness-level trace because the work touches cross-repo handoff.

Out of scope:

- No change to `contracts/contract.v0.3.json`.
- No change to `user_detected` or `recognition_result` required payload fields.
- No `display` implementation changes.
- No production TensorRT conversion yet.

## Starting Context

- Center contract v0.3 defines `firmware -> vision` as `q_detected` / `user_detected` and `vision -> display` as `q_result` / `recognition_result`.
- L515 was visible at USB/V4L2 level on AGX, but the apt `librealsense` runtime could not enumerate it and Python lacked `pyrealsense2`.
- `vision` already contained curated exports under `vision/exports/`, but the AGX environment lacked ONNX Runtime.
- Public model baseline was trained on TrashNet + RealWaste and did not yet include a real L515 demo-angle acceptance set.

## Implementation Steps

1. Built a user-local RealSense RSUSB stack for L515 and verified `pyrealsense2` can enumerate the camera.
2. Updated firmware L515 defaults to tolerate AGX/L515 startup timing: shorter warmup frame count and longer frame timeout.
3. Verified firmware `run_distance_trigger_loop` can process real L515 depth frames.
4. Installed user-site `onnxruntime==1.23.2` for AGX CPU inference without upgrading NumPy.
5. Updated `vision/src/runtime.py` so `L515ColorCamera` waits for RGB warmup frames before taking the model snapshot.
6. Ran `vision` runtime with a fake `user_detected` event and verified it emits a valid `recognition_result`.
7. Ran a firmware-to-vision handoff using L515 depth to produce `user_detected`, then L515 RGB + ONNX to produce `recognition_result`.
8. Tested the candy-wrapper/flexible-plastic L515 snapshot against all curated ONNX exports.
9. Added `vision/docs/model-registry.md` to record every curated export, metrics, hashes, and AGX L515 candy-wrapper result.
10. Added `vision/docs/agx-l515-vision-integration-20260604.md` for the implementation/model issue record.

## Decisions and Tradeoffs

- Kept v0.3 payloads unchanged. The observed model issue is a data/model-label problem, not a contract problem.
- Used ONNX Runtime CPU provider for the AGX smoke test because TensorRT conversion is not yet required for integration proof.
- Kept model export details in `vision`, following the AGENTS boundary that child repo model internals do not belong in the center Fact Map.
- Added this trace because queue handoff and model runtime verification affect cross-repo integration context.
- Clarified that flexible plastic packaging may be `accept` when product policy treats it as general waste; recyclable rigid plastic remains `reject`.

## Problems Encountered

- Apt `librealsense 2.58.1` could not enumerate L515 on this AGX setup; user-local RSUSB build was used instead.
- `v2.58.1` source did not provide working L515 support for this device path; `v2.54.1` RSUSB successfully enumerated L515.
- No sudo password was available, so the SDK fix was installed under the user home directory.
- L515 RGB frames were black during initial startup; `vision` now warms up 30 frames before inference snapshots.
- Default firmware central depth ROI sometimes saw zero valid depth if the object was off-center; integration testing used a wider ROI only to force a handoff event.
- Both available ONNX exports classified the candy-wrapper/flexible-plastic sample as high-confidence `reject`, while the demo expectation is `accept` if this item is general waste.

## Files Changed

- `firmware/firmware_l515/realsense_l515.py`
- `vision/src/runtime.py`
- `vision/tests/test_runtime_integration.py`
- `vision/docs/vision-spec.md`
- `vision/docs/agx-l515-vision-integration-20260604.md`
- `vision/docs/model-registry.md`
- `vision/README.md`
- `ai-enabled-emotional-garbagecane/docs/implementation-traces/2026-06-04-vision-agx-l515-model-records.md`

## Verification

```text
command:
LD_LIBRARY_PATH=/home/dla_test/.local/realsense-l515-rsusb/lib:$LD_LIBRARY_PATH /home/dla_test/.local/realsense-l515-rsusb/bin/rs-enumerate-devices -s
result:
PASS - Intel RealSense L515 serial f1272157, firmware 1.5.8.1 enumerated.
notes:
Uses user-local RSUSB SDK, not the system apt librealsense binary.
```

```text
command:
cd firmware && ./validate.sh
result:
PASS - contract check and 16 tests passed.
notes:
Firmware public API and `user_detected` payload unchanged.
```

```text
command:
firmware run_distance_trigger_loop(q_detected, max_frames=120)
result:
PASS - processed 120 real L515 depth frames with default firmware camera config.
notes:
LED stayed idle when the central ROI did not meet the 30cm trigger condition.
```

```text
command:
cd vision && ./validate.sh
result:
PASS - contract/spec checks, stub inference, accept gate, runtime integration, and baseline metrics checks passed.
notes:
The runtime warmup test is included in `tests/test_runtime_integration.py`.
```

```text
command:
vision process_user_detected_event(...) with L515ColorCamera and default ONNX classifier
result:
PASS - emitted recognition_result class=reject confidence=0.9855062961578369 snapshot_path=/home/dla_test/DLA_Final/vision/snapshots/l515-20260604T011500.jpg.
notes:
Snapshot was a visible L515 RGB image after warmup.
```

```text
command:
Run all curated ONNX exports on /home/dla_test/DLA_Final/vision/snapshots/l515-20260604T011500.jpg
result:
PASS - both models executed; both predicted high-confidence reject.
notes:
This is a model failure if candy-wrapper flexible plastic should be accepted as general waste.
```

## Follow-up

- Resolve the label policy explicitly: flexible plastic wrappers and dirty/mixed-material film packaging should be `accept` if the bin is for general waste, while recyclable rigid plastic remains `reject`.
- Collect L515 demo-angle training/validation images for both flexible-wrapper accept samples and rigid-plastic reject samples.
- Retrain or fine-tune YOLOv11n after label cleanup; keep current models as integration baselines only.
- Add a launcher-level smoke test once the process supervisor for firmware, vision, and display exists.
- Consider TensorRT export only after the model label issue is fixed.

## Rollback Notes

- To revert runtime behavior, restore `vision/src/runtime.py` `L515ColorCamera` defaults and remove RGB warmup logic.
- To revert documentation only, remove `vision/docs/model-registry.md`, `vision/docs/agx-l515-vision-integration-20260604.md`, and this trace.
- No contract lock rollback is needed because no public v0.3 payload fields changed.

## Revision Notes

- Initial trace created after AGX L515 firmware/vision integration and all current vision model export records were documented.
